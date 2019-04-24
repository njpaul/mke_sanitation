import re
import requests
from datetime import date, datetime
from .addr import *
from .util import case_insensitive_lookup, strip_html_tags


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


# Returns datetime.date on success
# Raises UnknownCollectionType if the collection type cannot be interpreted
# Raises AddrError if the address cannot be interpreted
# TODO: Could the result of this be saved in a session to avoid having to
# query again?
def get_collection_date(coll_type_str, addr_str):
    coll_type = CollectionType.from_text(coll_type_str)
    addr_parts = AddrParts.from_text(addr_str)

    try:
        response_text = _make_request(addr_parts)
    except requests.exceptions.HTTPError as ex:
        raise CollectionResponseError from ex
    print(response_text)
    if coll_type == CollectionType.GARBAGE:
        return _read_garbage_date(response_text)
    else:
        return _read_recycling_date(response_text)


def _make_request(addr):
    URL = "https://itmdapps.milwaukee.gov/DPWServletsPublic/garbage_day"
    PARAMS = {"embed": "Y"}
    data = {
        "laddr": addr.st_num,
        "sdir": addr.st_dir,
        "sname": addr.st_name,
        "stype": addr.st_suffix,
        "embed": "Y",
        "Submit": "Submit"
    }
    resp = requests.post(URL, params=PARAMS, data=data)
    resp.raise_for_status()
    return resp.text

# TODO: Remove the duplication of the next two functions

# Returns a datetime.date on success
# Raises UnknownCollectionDate if the garbage date could not be determined
# Raises CollectionResponseError if the response cannot be interpreted


def _read_garbage_date(response_text):
    text = strip_html_tags(response_text)
    garbage_day = _match_garbage_day(text)
    if garbage_day is None:
        if _match_garbage_day_undetermined(text):
            raise UnknownCollectionDate
        else:
            raise CollectionResponseError
    return garbage_day


# Returns a datetime.date on success
# Raises UnknownCollectionDate if the recycling date could not be determined
# Raises CollectionResponseError if the response cannot be interpreted
def _read_recycling_date(response_text):
    text = strip_html_tags(response_text)
    recycling_day = _match_recycling_day(text)
    if recycling_day is None:
        if _match_recycling_day_undetermined(text):
            raise UnknownCollectionDate
        else:
            raise CollectionResponseError
    return recycling_day


# Try to find the garbage day by matching known text.
# Returns a datetime.date if the garbage day is found, otherwise None
def _match_garbage_day(text):
    prog = re.compile(r"The next garbage collection pickup for this location "
                      r"is: \w+ (\w+) (\d+), (\d+)")
    match = prog.search(text)
    if match is None:
        return None

    date_str = "{} {:0>2} {}".format(*match.groups())
    try:
        # TODO: Might run into a locale bug here. Better to set locale
        # explicitly to en_US. Should add a test for this.
        return datetime.strptime(date_str, "%B %d %Y").date()
    except ValueError:
        return None


# Try to see if the garbage day could not be determined by matching known text.
# Returns True if garbage day could not be determined, False otherwise
def _match_garbage_day_undetermined(text):
    return text.find("Your garbage collection schedule could not be determined") != -1


# Try to find the recycling day by matching known text.
# Returns a datetime.date if the recycling day is found, otherwise None
def _match_recycling_day(text):
    # TODO: Remove duplication with garbage day
    prog = re.compile(r"The next recycling collection pickup for this location "
                      r"is: \w+ (\w+) (\d+), (\d+)")
    match = prog.search(text)
    if match is None:
        return None

    date_str = "{} {:0>2} {}".format(*match.groups())
    try:
        # TODO: Might run into a locale bug here. Better to set locale
        # explicitly to en_US. Should add a test for this.
        return datetime.strptime(date_str, "%B %d %Y").date()
    except ValueError:
        return None


# Try to see if the recycling day could not be determined.
# Currently there is no text returned that describes the inability to
# determine the recycling date, so we can't determine this directly.
# We can, however, sense it through the garbage date, which will return
# undetermined in this case as well. This assumes that we will never be
# able to find one date without also finding the other.
# Returns True if recycling day could not be determined, False otherwise
def _match_recycling_day_undetermined(text):
    return _match_garbage_day_undetermined(text)
