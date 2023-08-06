"""Base plugin class."""
# Copyright © 2022 Appropriate Solutions, Inc. All rights reserved.

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Generator, cast


def split_commas(data: str | list, make_int: bool = False) -> list[int | str]:
    """
    Create list from comma-delimited string (or list).

    If make_int is True, ensure final list contents are integers.

    Args:
        data:
            String or list of data to process.

        make_int:
            True if final list must contain only integers.

    Returns:
        list

    """
    if not data:
        # Don't mess with empty strings.
        return []

    if isinstance(data, str):
        data = data.split(",")

    if make_int:
        return [int(x) for x in data]
    # Yes, we know it is a list[str]...
    # Without cast mypy thinks we're returning list[Any].
    return cast(list[int | str], data)


class SheetData:
    """All information required to display a worksheet."""

    def __init__(
        self,
        *,
        sheet_name: str,
        header_row: list[str],
        data_rows: list[list],
        column_widths: list[int],
    ) -> None:
        """Gather all necessary information."""
        self.sheet_name = sheet_name
        self.header_row = header_row
        self.data_rows = data_rows
        self.column_widths = column_widths


class BasePlugin(ABC):
    """Base of all plugins."""

    def __init__(
        self,
        display_name: str,
        field_names: str,
        column_widths: str | list[int],
    ) -> None:
        """
        Initialize base plugin.

        field_names:
            Comma-delimited list of fields to obtain.
            Also used for the sheet's header row.

        column_widths:
            Comma-delimited list of sheet column widths.

        """
        self.display_name: str = display_name
        self.field_names: list[str] = cast(list[str], split_commas(field_names))
        self.column_widths: list[int] = cast(
            list[int], split_commas(column_widths, make_int=True)
        )

    @abstractmethod
    def run(self, pfsense: OrderedDict) -> Generator[SheetData, None, None]:
        """
        Run plugin.

        Args:
            pfsense:
                Root of the XML configuration file parsed to dictionary.

        Returns:
            List of rows to write to spreadsheet.

        """
        raise NotImplementedError
