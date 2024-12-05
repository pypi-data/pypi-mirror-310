import logging
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry_plugin_openfund.command import OpenfundCommand


logger = logging.getLogger(__name__)


def factory():
    return OpenfundCommand()


class OpenfundApplicationPlugin(ApplicationPlugin):
    def __init__(self) -> None:
        logger.debug("------- OpenfundApplicationPlugin init ...")
        super().__init__()

    def activate(self, application):
        logger.debug("------- OpenfundApplicationPlugin activate ...")
        application.command_loader.register_factory("openfund", factory)
