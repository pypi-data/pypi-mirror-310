"""
Rust support for nmk
"""

from importlib.metadata import version

from nmk_base.version import VersionResolver

__title__ = "nmk-rust"
try:
    __version__ = version(__title__)
except Exception:  # pragma: no cover
    __version__ = "unknown"


class NmkRustVersionResolver(VersionResolver):
    """Plugin version resolver"""

    def get_version(self) -> str:
        """Returns nmk-rust plugin version"""
        return __version__
