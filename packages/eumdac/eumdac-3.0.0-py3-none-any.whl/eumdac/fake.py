# type: ignore
"""Fake DataStore, DataTailor and Product that will be used when adding the --test
option in favour of the real implementations. Only useful for unittests."""

import io
from contextlib import contextmanager


class FakeDataStore:
    """Fake DataStore for testing."""

    def get_collection(self, collection_id):
        """Return a FakeCollection with `collection_id`."""
        return FakeCollection(collection_id)

    def get_product(self, collection_id, product_id):
        """Return a FakeProduct with `product_id` from `collection_id`."""
        return FakeProduct(collection_id, product_id)


class FakeProduct:
    """FakeProduct for testing."""

    def __init__(self, collection_id, product_id):
        """Init from `collection_id` and `product_id`."""
        self._id = product_id
        self.collection = FakeCollection(collection_id)
        self.entries = ["entry1.nc", "entry2.nc"]

    def __str__(self):
        """Return the id as str representation"""
        return str(self._id)

    def open(self, entry=None, chunk=None, custom_headers=None):
        """Return a fake stream as the contents of the product."""
        if entry:
            return FakeStream(f"{self._id}-{entry}")

        return FakeStream(self._id)

    @property
    def md5(self):
        """Return the md5 of the fake stream returned on open."""
        import hashlib

        with self.open(None) as f:
            return hashlib.md5(f.read()).hexdigest()


class FakeStream:
    def __init__(self, name):
        self.decode_content = True
        self.name = name
        self.content = io.BytesIO(b"Content")

    def getheader(self, header):
        if header == "Content-Length":
            # Return a fixed length (7) for 'Content-Length' header.
            return 7
        return None

    def read(self, num=None):
        return self.content.read(num)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class FakeCollection:
    """Fake Collection for testing."""

    def __init__(self, collection_id):
        """Init from `collection_id`."""
        self._id = collection_id

    def __str__(self):
        """Return id as the str representation."""
        return str(self._id)

    def search(self, **query):
        """Return fake search results."""
        dtstart = query["dtstart"]
        dtend = query["dtend"]
        return [
            FakeProduct(self._id, f"prod_{dtstart.isoformat().strip().replace(':', '-')}"),
            FakeProduct(self._id, f"prod_{dtend.isoformat().strip().replace(':', '-')}"),
        ]


class FakeDataTailor:
    """Fake DataTailor for testing."""

    pass
