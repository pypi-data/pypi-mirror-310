"""
Module: eumdac.futures

This module defines classes for managing a custom thread pool executor with cooperative function handling.

Classes:
- EumdacFutureFunc: Represents a callable function with cooperative handling.
- EumdacThreadPoolExecutor: Extends ThreadPoolExecutor to manage cooperative function execution.

Usage:
1. Create instances of EumdacFutureFunc to define callable functions with cooperative handling.
2. Use EumdacThreadPoolExecutor to submit functions to a thread pool with cooperative handling.
"""

import concurrent.futures
import sys
from typing import Any, List
from eumdac.logging import logger


class EumdacFutureFunc:
    def __init__(self) -> None:
        """
        Initialize the EumdacFutureFunc object.
        """
        self.aborted = False

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Placeholder for the callable function. Must be implemented in subclasses.

        Raises:
        - NotImplementedError: If the method is called directly without being implemented in a subclass.
        """
        raise NotImplementedError()

    def abort(self) -> None:
        """
        Set the 'aborted' flag to True, indicating that the function has been aborted.
        This needs to be handled cooperatively in the Subclasses
        """
        logger.debug(f"{self} abort request received")
        self.aborted = True


class EumdacThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the EumdacThreadPoolExecutor object.

        Attributes:
        - functors (List[EumdacFutureFunc]): List to store EumdacFutureFunc instances.
        """
        self.functors: List[EumdacFutureFunc] = []
        super().__init__(*args, **kwargs)

    def pool_shutdown(self) -> None:
        """
        Abort all functions in the 'functors' list and ask them to gracefully shut down.
        """
        logger.debug(f"{self} pool_shutdown issued")
        for f in self.functors:
            logger.debug(f"{self} aborting {f}")
            f.abort()
        if sys.version_info >= (3, 9):
            return super().shutdown(wait=True, cancel_futures=True)
        else:
            return super().shutdown(wait=True)

    def pool_submit(
        self, fn: EumdacFutureFunc, *args: Any, **kwargs: Any
    ) -> "concurrent.futures.Future[Any]":
        """
        Submit a function to the thread pool executor and add it to the 'functors' list.

        Args:
        - fn (EumdacFutureFunc): The function to be submitted.
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.

        Returns:
        - concurrent.futures.Future[Any]: A Future object representing the execution of the submitted function.
        """
        self.functors.append(fn)
        return super().submit(fn, *args, **kwargs)
