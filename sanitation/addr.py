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
    st_name = " ".join(parts)
    if not st_name:
        raise AddrError
    return st_name
