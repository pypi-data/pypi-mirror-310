"""module containing the DownloadApp which will be used when using 
eumdac download **without** the --tailor argument."""

import concurrent
import datetime
import fnmatch
import logging
import shutil
import sys
import tempfile
import threading
import time
from hashlib import md5
from pathlib import Path
from typing import IO, Any, Generator, List, Mapping, Optional, Tuple

import eumdac.common
from eumdac.futures import EumdacFutureFunc, EumdacThreadPoolExecutor
from eumdac.job_id import JobIdentifier
from eumdac.logging import logger
from eumdac.order import Order
from eumdac.product import Product
import eumdac.product


def _divide_into_chunks(
    basedir: str, content_length: int, chunk_size: int
) -> Mapping[Path, Tuple[int, int]]:
    """
    Divides a products content into chunks and returns a mapping of file paths to chunk ranges.

    Each chunk is represented by a tuple specifying the start and end byte positions within the file.
    The function creates new paths for each chunk, using the base directory and product name as
    part of the path, and appends the chunk index to the file name.

    Args:
        basedir (str): The base directory where chunks will be stored.
        prodname (str): The product name that will be used as a subdirectory or file prefix.
        content_length (int): The total size of the content (in bytes) to be divided.
        chunk_size (int): The size of each chunk in bytes.

    Returns:
        Mapping[Path, Tuple[int, int]]: A dictionary where each key is a `Path` object pointing to
        a chunk file, and the value is a tuple indicating the start and end byte positions of the chunk.
        This is called chunk_dict in the code below.
    """
    ret = {
        Path(basedir) / f"chunk.{i}": (a, b)
        for i, (a, b) in enumerate(_chunk_ranges(content_length, chunk_size))
    }
    return ret


def _chunk_ranges(content_length: int, chunk_size: int) -> Generator[Tuple[int, int], None, None]:
    cur = 0
    while True:
        if cur + chunk_size > content_length:
            break
        yield (cur, cur + chunk_size)
        cur += chunk_size
    if cur != content_length:
        yield (cur, content_length)


def _mb_per_s(bytes_downloaded: int, elapsed_time: float) -> float:
    """
    Calculate the download speed in MB/s.
    """
    if elapsed_time > 0:
        return (
            bytes_downloaded / 1024 / 1024
        ) / elapsed_time  # Convert bytes to MB, then calculate MB/s
    return 0.0


def log(level: int, message: str) -> None:
    if (
        sys.stdout.isatty()
        and logger._progress_handler  # type: ignore
        and _download_speed_tracker.last_line_was_progress
    ):
        _download_speed_tracker.last_line_was_progress = False
        logger.log(level, "")
    logger.log(level, message)


class DownloadSpeedTracker:
    def __init__(self) -> None:
        self.total_bytes_downloaded = 0
        self.start_time = 0.0
        self.last_measured_speed = -1.0
        self.lock = threading.Lock()
        self.last_line_was_progress = False
        self.running = False

    def start(self) -> None:
        with self.lock:
            self.running = True
            self.start_time = time.time()
            self.last_update_time = self.start_time

    def stop(self) -> None:
        with self.lock:
            self.running = False

    def update(self, bytes_downloaded: int) -> None:
        if not self.running:
            return

        if self.start_time is None:
            raise RuntimeError("DownloadSpeedTracker has not been started. Call 'start()' first.")

        with self.lock:  # Ensure only one thread can update at a time
            self.total_bytes_downloaded += bytes_downloaded
            elapsed_time = time.time() - self.start_time
            mb_downloaded = self.total_bytes_downloaded / 1024 / 1024
            if elapsed_time > 0:
                self.last_measured_speed = mb_downloaded / elapsed_time

        self.last_line_was_progress = True
        logger.progress(  # type:ignore
            f"Elapsed time: {str(datetime.timedelta(seconds=round(elapsed_time)))}, {mb_downloaded} MB downloaded, current speed: {self.get_current_speed():.2f} MB/s"
        )

    def get_current_speed(self) -> float:
        if self.start_time is None:
            raise RuntimeError("DownloadSpeedTracker has not been started. Call 'start()' first.")

        with self.lock:  # Ensure consistent access to shared data
            return self.last_measured_speed


_download_speed_tracker = DownloadSpeedTracker()


class DownloadApp:
    def __init__(
        self,
        order: Order,
        datastore: Any,
        integrity: bool = False,
        download_threads: int = 3,
        chunk_size: Optional[int] = None,
    ) -> None:
        self.download_executor = EumdacThreadPoolExecutor(max_workers=download_threads)
        self.reassembling_executor = EumdacThreadPoolExecutor(max_workers=None)
        self.order = order
        self.datastore = datastore
        self.check_integrity = integrity
        num_jobs = len(list(self.order.iter_product_info()))
        self.job_identificator = JobIdentifier(num_jobs)
        self.num_download_threads = download_threads
        self.chunk_size = chunk_size

    def run(self) -> bool:
        log(logging.DEBUG, "Starting download(s)")
        return self._run_app()

    def shutdown(self) -> None:
        with self.order._lock:
            _download_speed_tracker.stop()
            self.reassembling_executor.pool_shutdown()
            self.download_executor.pool_shutdown()

    def _run_app(self) -> bool:
        with self.order.dict_from_file() as order_d:
            output_dir = order_d["output_dir"]
            output_dir = Path(output_dir).resolve()
            output_dir.mkdir(exist_ok=True, parents=True)
            dirs = order_d["dirs"]
            onedir = order_d["onedir"]

        (file_patterns,) = self.order.get_dict_entries("file_patterns")
        log(logging.INFO, f"Output directory: {output_dir}")

        success = True

        _download_speed_tracker.start()

        reassembling_futures = []
        for product in self.order.get_products(self.datastore):
            download_futures = []
            self.job_identificator.register(product)
            with self.order.dict_from_file() as order_d:
                state = order_d["products_to_process"][product._id]["server_state"]
            if state == "DONE":
                continue
            if file_patterns:
                entries = product.entries
                filtered_entries = []
                for pattern in file_patterns:
                    matches = fnmatch.filter(entries, pattern)
                    filtered_entries.extend(matches)
                entries = filtered_entries
            else:
                entries = [None]  # type: ignore

            for entry in entries:
                job_id = self.job_identificator.job_id_tuple(product)
                try:
                    with product.open(entry=entry) as fsrc:
                        fsrc_name = fsrc.name
                        content_size = _get_content_size(fsrc)
                except eumdac.product.ProductError as e:
                    logger.error(f"{_print_job_id_info(job_id)} Skipping download: {e}")
                    success = False
                    continue

                output = _compute_output_path(
                    product,
                    fsrc_name,
                    dirs,
                    onedir,
                    entry,
                    output_dir,
                )
                if _already_present(
                    product,
                    output,
                    job_id,
                    self.check_integrity,
                ):
                    continue
                funcs, chunk_dict = get_download_funcs(
                    product,
                    entry,
                    output,
                    content_size,
                    job_id,
                    self.num_download_threads,
                    self.chunk_size,
                )
                for func, args in funcs:
                    download_futures.append(self.download_executor.pool_submit(func, *args))
                reassembling_futures.append(
                    self.reassembling_executor.pool_submit(
                        ReassembleChunkFunc(),
                        download_futures,
                        chunk_dict,
                        product,
                        output,
                        self.check_integrity,
                        job_id,
                        self.order,
                    )
                )

        for f in concurrent.futures.as_completed(reassembling_futures):
            success = success and f.result()

        return success


def get_download_funcs(
    product: Product,
    entry: Optional[str],
    output: Path,
    content_size: Optional[int],
    job_id: Tuple[int, str],
    num_threads: int,
    chunk_size: Optional[int],
) -> Tuple[List[Any], Mapping[Path, Optional[Tuple[int, int]]]]:
    # download chunks
    with tempfile.TemporaryDirectory(dir=output.parent, suffix=".tmp") as tempdir:
        chunk_dict: Mapping[Path, Optional[Tuple[int, int]]]
        if content_size is None:
            chunk_dict = {Path(tempdir) / "chunk.0": None}
        else:
            if chunk_size is None:
                # At this point we know the content size and can do a chunk based download
                min_chunk_size = 1024 * 1024 * 100  # 100 MB
                chunk_size = max(content_size // (num_threads), min_chunk_size)

            chunk_dict = _divide_into_chunks(tempdir, content_size, chunk_size)

            log(
                logging.INFO,
                f"{_print_job_id_info(job_id)} Preparing download of {_print_product(product, output)}, splitting in {len(chunk_dict)} chunks.",
            )

            download_funcs = []
            chunk_range: Optional[Tuple[int, int]]
            for chunk_name, chunk_range in chunk_dict.items():
                if len(chunk_dict) == 1:
                    chunk_range = None
                download_fname = chunk_name
                download_fname.parent.mkdir(parents=True, exist_ok=True)
                log(
                    logging.DEBUG,
                    f"Scheduling DownloadChunkFunc fo {product}, with range {chunk_range} to {download_fname}",
                )
                download_funcs.append(
                    (
                        DownloadChunkFunc(),
                        (job_id, product, entry, download_fname, chunk_range),
                    )
                )
    return download_funcs, chunk_dict


class ReassembleChunkFunc(EumdacFutureFunc):
    def __call__(
        self,
        download_futures: List[concurrent.futures.Future],  # type: ignore
        chunk_dict: Mapping[Path, Tuple[int, int]],
        product: Product,
        output: Path,
        check_integrity: bool,
        job_id: Tuple[int, str],
        order: Order,
    ) -> bool:
        success = False

        # wait for all downloads to be completed
        while True:
            if self.aborted:
                # delete temp dir
                shutil.rmtree(list(chunk_dict)[0].parent)
                raise KeyboardInterrupt()
            if all(x.done() for x in download_futures):
                break
            time.sleep(0.1)

        # check if all chunks are present and have the expected size
        if not _check_chunks(chunk_dict, _print_job_id_info(job_id)):
            # avoid reporting errors when the process is interrupted
            if not self.aborted:
                log(
                    logging.ERROR,
                    f"{_print_job_id_info(job_id)} Could not verify all chunks from {product}",
                )
            success = False
        else:
            # reassemble the chunks into the outputfile
            _reassemble_from_chunks(chunk_dict, output)

            # delete temp dir
            shutil.rmtree(list(chunk_dict)[0].parent)

            if not check_integrity:
                success = True
            else:
                if product.md5 is None:
                    log(
                        logging.WARN,
                        f"{_print_job_id_info(job_id)} Skipping integrity check: no MD5 metadata found for {_print_product(product, output)}",
                    )
                    success = True
                elif not _md5_check(output, product.md5):
                    log(
                        logging.WARN,
                        f"{_print_job_id_info(job_id)} Integrity check failed for {_print_product(product, output)} with MD5:  {product.md5}",
                    )
                    success = False
                else:
                    log(
                        logging.INFO,
                        f"{_print_job_id_info(job_id)} Integrity check successful for {_print_product(product, output)} with MD5: {product.md5}",
                    )
                    success = True

        if success:
            order.update(None, product._id, "DONE")
            log(
                logging.INFO,
                f"{_print_job_id_info(job_id)} Download complete: {_print_product(product, output)}, current speed: {_download_speed_tracker.get_current_speed():.2f} MB/s",
            )
        else:
            order.update(None, product._id, "FAILED")
            log(logging.ERROR, f"{_print_job_id_info(job_id)} Download failure: {product}")

        return success


class DownloadChunkFunc(EumdacFutureFunc):
    def __call__(
        self,
        job_id: str,
        product: Product,
        entry: Optional[str],
        output: Path,
        chunk_range: Optional[Tuple[int, int]],
    ) -> None:
        output.parent.mkdir(exist_ok=True, parents=True)

        with output.open("wb") as outf:
            if chunk_range is not None:
                bytes_to_read = chunk_range[1] - chunk_range[0]
                log(
                    logging.DEBUG,
                    f"{job_id} Downloading {bytes_to_read} bytes of {output} [chunk-based]",
                )
            else:
                log(logging.DEBUG, f"{job_id} Downloading {output} [full-file]")
            if self.aborted:
                raise KeyboardInterrupt()
            modified_referer = f"{eumdac.common.headers['referer']} JobID: {job_id[1]}"
            with product.open(
                entry=entry,
                chunk=chunk_range,
                custom_headers={
                    "referer": modified_referer,
                },
            ) as fsrc:
                while True:
                    if self.aborted:
                        raise KeyboardInterrupt()
                    chunk = fsrc.read(1024 * 1024)  # type: ignore
                    _download_speed_tracker.update(1024 * 1024)
                    if not chunk:
                        break
                    outf.write(chunk)
        log(logging.DEBUG, f"{job_id} Download {output} finished")


def _get_content_size(fsrc: IO[bytes]) -> Optional[int]:
    if not hasattr(fsrc, "getheader"):
        return None
    content_size_header = fsrc.getheader("Content-Length")
    if not content_size_header:
        return None
    return int(content_size_header)


def _check_chunks(chunks: Mapping[Path, Tuple[int, int]], job_id: Optional[str] = "") -> bool:
    for fname, chunk_range in chunks.items():
        if not fname.exists():
            log(logging.ERROR, f"{job_id} Error checking chunk {fname}: file does not exist")
            return False
        expected_chunk_size = chunk_range[1] - chunk_range[0]
        if fname.stat().st_size != expected_chunk_size:
            log(
                logging.ERROR,
                f"{job_id} Error checking chunk {fname}: size mismatch, expected {expected_chunk_size}, got {fname.stat().st_size}",
            )
            return False

    return True


def _reassemble_from_chunks(chunks: Mapping[Path, Tuple[int, int]], output_fname: Path) -> Path:
    output_fname = Path(output_fname)
    chunkdir = list(chunks)[0].parent
    with output_fname.open("wb") as binfile:
        for i, _ in enumerate(chunks):
            chunk_file = chunkdir / f"chunk.{i}"
            with chunk_file.open("rb") as chunkfile:
                binfile.write(chunkfile.read())
    return output_fname


def _md5_check(file_to_check: Path, expected_md5: str) -> bool:
    md5sum = md5()
    with file_to_check.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5sum.update(chunk)
    return expected_md5 == md5sum.hexdigest()


def _compute_output_path(
    product: Product,
    fsrc_name: str,
    dirs: bool,
    onedir: bool,
    entry: Optional[str],
    output_dir: Path,
) -> Path:
    output = output_dir / fsrc_name
    if dirs or (entry and not onedir):
        # when the dirs or entry flags are used
        # a subdirectory is created
        # to avoid overwriting common files
        # unless the onedir flag has been provided
        output_subdir = output_dir / f"{product}"
        output_subdir.mkdir(exist_ok=True)
        output = output_subdir / fsrc_name
    return output


def _already_present(
    product: Product,
    output: Path,
    job_id: Tuple[int, str],
    check_integrity: bool,
) -> bool:
    if output.is_file():
        if check_integrity and product.md5 is not None:
            # md5 check
            md5sum = md5()
            with output.open("rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5sum.update(chunk)
            if product.md5 == md5sum.hexdigest():
                log(
                    logging.INFO,
                    f"{_print_job_id_info(job_id)} Skip {output.name}: file already exists and passes integrity check with MD5 (computed/expected): {md5sum.hexdigest()}/{product.md5}",
                )
                return True
            else:
                log(
                    logging.INFO,
                    f"{_print_job_id_info(job_id)} Found existing {output.name}, but failed integrity check with MD5 (computed/expected): {md5sum.hexdigest()}/{product.md5}",
                )
                return False
        else:
            if check_integrity:
                log(
                    logging.WARN,
                    f"{_print_job_id_info(job_id)} Skipping integrity check: no MD5 metadata found for {output.name}",
                )
            log(logging.INFO, f"{_print_job_id_info(job_id)} Skip {output}, file already exists")
            return True
    return False


def _print_product(product: Product, output: Path) -> str:
    return str(product) if output.name.find(str(product)) > -1 else str(f"{product}/{output.name}")


def _print_job_id_info(job_id: Tuple[int, str]) -> str:
    return f"Job {job_id[0]}:"
