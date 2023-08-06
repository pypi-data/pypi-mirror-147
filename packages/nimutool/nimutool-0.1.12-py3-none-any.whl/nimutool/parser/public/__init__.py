from .nordic_inertial_parser import NimuParser, NimuDebugParser, NimuGpsSyncParser
from .pacific_inertial_parser import PI48Parser

PARSERS = {
    'pi48': PI48Parser,
    'nimu': NimuParser,
    'nimudebug': NimuDebugParser,
    'nimusync': NimuGpsSyncParser
}
