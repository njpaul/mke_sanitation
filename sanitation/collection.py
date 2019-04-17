from .addr import *
from .util import case_insensitive_lookup


class UnknownCollectionType(Exception):
    pass


class UnknownCollectionDate(Exception):
    pass


class CollectionResponseError(Exception):
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
    def __init__(self, coll_type, addr_parts, coll_date):
        self.coll_type = coll_type
        self.addr_parts = addr_parts
        self.coll_date = coll_date


# Returns datetime.date on success
# Raises UnknownCollectionType if the collection type cannot be interpreted
# Raises AddrError if the address cannot be interpreted
# TODO: Could the result of this be saved in a session to avoid having to
# query again?
def get_collection_date(coll_type_str, addr_str):
    coll_type = CollectionType.from_text(coll_type_str)
    addr_parts = AddrParts.from_text(addr_str)
    # Make request and get response
    # response_text = ...
    # coll_date = _parse_response_text(response_text, coll_type)
    # return _get_collection_date_impl(coll_type, addr_parts)
    return None


# Returns a CollectionDate on success
# Raises UnknownResponse if the response cannot be interpreted
def _parse_response_text(response_text, coll_type):
    return None
