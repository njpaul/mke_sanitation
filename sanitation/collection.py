from .addr import *
from .util import case_insensitive_lookup


class UnknownCollectionType(Exception):
    pass


class CollectionType:
    GARBAGE = 0
    RECYCLING = 1

    _MAPPING = {
        "garbage": GARBAGE,
        "recycling": RECYCLING
    }

    # Raises UnknownCollectionType when the text cannot be mapped
    # to a known type
    @staticmethod
    def from_text(text):
        try:
            return case_insensitive_lookup(CollectionType._MAPPING, text)
        except KeyError as ex:
            raise UnknownCollectionType from ex


class CollectionDate:
    def __init__(self, addr_parts, coll_date):
        self.addr_parts = addr_parts
        self.coll_date = coll_date


# Returns CollectionDate on success
# Raises UnknownCollectionType if the collection type cannot be interpreted
# Raises AddrError if the address cannot be interpreted
def get_collection_date(coll_type_str, addr_str):
    coll_type = CollectionType.from_text(coll_type_str)
    addr_parts = AddrParts.from_text(addr_str)
    return _get_collection_date_impl(coll_type, addr_parts)


def _get_collection_date_impl(coll_type, addr_parts):
    pass


def _parse_collection_type(text):
    return
