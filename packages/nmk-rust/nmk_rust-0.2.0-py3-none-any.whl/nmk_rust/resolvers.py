"""
Resolvers logic for rust plugin
"""

from pathlib import Path

from nmk.model.resolver import NmkListConfigResolver


class RustSourcesResolver(NmkListConfigResolver):
    """
    Rust source files finder
    """

    def get_value(self, name: str, folder: str) -> list[Path]:
        """
        Find all rust source files in specified source folder

        :param name: config item name
        :param folder: root rust source folder
        :return: list of input rust files
        """

        # Iterate on source paths, and find all rust files
        return list(filter(lambda f: f.is_file(), Path(folder).rglob("*.rs")))
