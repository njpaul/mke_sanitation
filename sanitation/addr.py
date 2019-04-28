from .util import case_insensitive_lookup


class AddrError(Exception):
    pass


class AddrDir:
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"

    _MAPPING = {
        "n": NORTH,
        "north": NORTH,
        "s": SOUTH,
        "south": SOUTH,
        "e": EAST,
        "east": EAST,
        "w": WEST,
        "west": WEST
    }

    @staticmethod
    def from_text(text):
        return case_insensitive_lookup(AddrDir._MAPPING, text)


class AddrSuffix:
    AVE = "AV"
    BLVD = "BL"
    CIRCLE = "CR"
    COURT = "CT"
    DRIVE = "DR"
    LANE = "LN"
    PARK = "PK"
    PLACE = "PL"
    ROAD = "RD"
    SQUARE = "SQ"
    STREET = "ST"
    TERRACE = "TR"
    WAY = "WA"

    _MAPPING = {
        "ave": AVE,
        "avenue": AVE,
        "boulevard": BLVD,
        "circle": CIRCLE,
        "court": COURT,
        "drive": DRIVE,
        "lane": LANE,
        "park": PARK,
        "parkway": PARK,
        "place": PLACE,
        "pl": PLACE,
        "road": ROAD,
        "square": SQUARE,
        "street": STREET,
        "terrace": TERRACE,
        "way": WAY
    }

    @staticmethod
    def from_text(text):
        return case_insensitive_lookup(AddrSuffix._MAPPING, text)


class AddrParts:
    # Don't call this externally from the module. Use from_text instead.
    def __init__(self, st_num, st_dir, st_name, st_suffix):
        self.st_num = st_num
        self.st_dir = st_dir
        self.st_name = st_name
        self.st_suffix = st_suffix

    # Raises AddrError when the address cannot be interperted
    @staticmethod
    def from_text(text):
        try:
            return _parse_addr(text)
        except Exception as ex:
            raise AddrError from ex


def _parse_addr(text):
    # Take advantage of the fact that the suffix is always a single word, so
    # we can easily just split based on spaces instead of tokenizing
    text_parts = str.split(text)
    st_num = _parse_street_num(text_parts[0])
    st_dir = AddrDir.from_text(text_parts[1])
    st_name = _parse_street_name(text_parts[2:-1])
    st_suffix = AddrSuffix.from_text(text_parts[-1])

    return AddrParts(st_num, st_dir, st_name, st_suffix)


def _parse_street_num(text):
    return int(text)


def _parse_street_name(parts):
    st_name = " ".join(parts).upper()
    if not st_name:
        raise AddrError

    # Alexa doesn't always hear the suffix of a numbered street, so
    # we'll try to correct that here.
    try:
        suffix = _get_num_suffix(st_name)
        st_name += suffix
    except ValueError:
        # Not a number, just return what we heard
        pass

    return st_name


# Returns the uppercase suffix of a number, how it would be spoken.
# Raises ValueError if 'num' is not a number
def _get_num_suffix(num):
    num = int(num)

    # Although we should only have to deal with 10s and 100s street names,
    # we this is generic across all numbers by reducing to a value in the
    # <= 100 range.
    while num > 100:
        num -= 100

    if 11 <= num <= 19:
        suffix = "TH"
    else:
        # All other numbers are based off the last digit.
        num %= 10
        if num == 1:
            suffix = "ST"
        elif num == 2:
            suffix = "ND"
        elif num == 3:
            suffix = "RD"
        else:
            suffix = "TH"

    return suffix
