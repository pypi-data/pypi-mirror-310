from __future__ import annotations

import logging

from typing import TYPE_CHECKING
from typing import Any

from cleo.exceptions import CleoValueError

from poetry.console.commands.command import Command as BaseCommand

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from collections.abc import Callable


class OpenfundCommand(BaseCommand):

    name = "openfund"

    def __init__(self) -> None:
        logger.debug("------- OpenfundCommand init ...")
        super().__init__()

    def handle(self) -> int:
        from poetry.utils._compat import metadata

        logger.debug("------- OpenfundCommand handle ...")
        # The metadata.version that we import for Python 3.7 is untyped, work around
        # that.
        version: Callable[[str], str] = metadata.version

        self.line(
            f"""\
        <info>Openfund - Funder for Python

        Version: {version('poetry_plugin_openfund')}
        """
        )

        return 0
