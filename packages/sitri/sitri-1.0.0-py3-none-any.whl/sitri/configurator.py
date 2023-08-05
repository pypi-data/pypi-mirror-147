"""
.. module:: configurator
   :synopsis: General Sitri class
.. moduleauthor:: Aleksander Lavrov <github.com/egnod>
"""


import typing

from sitri.logger import get_default_logger
from sitri.providers.base import ConfigProvider
from sitri.strategy.base import BaseStrategy
from sitri.strategy.single import SingleStrategy


class SitriProviderConfigurator:
    """Class for unite config provider."""

    def __init__(
        self, config_provider: typing.Union[ConfigProvider, BaseStrategy], logger: typing.Optional[typing.Any] = None
    ):
        """
        :param config_provider: object of config provider
        """

        self.config = None

        if not logger:
            logger = get_default_logger()

        self.logger = logger

        if isinstance(config_provider, BaseStrategy):
            self.config = config_provider

        elif config_provider:
            self.config = SingleStrategy(config_provider)

    def get(self, key: str, default: typing.Any = None, **kwargs) -> typing.Union[typing.Any, None]:
        """Get value from config provider.

        :param key: key for config provider
        :param default: if provider return None
        """
        if not self.config:
            self.logger.info("No config provider")
            return None

        variable = self.config.get(key, **kwargs)

        return variable if variable else default
