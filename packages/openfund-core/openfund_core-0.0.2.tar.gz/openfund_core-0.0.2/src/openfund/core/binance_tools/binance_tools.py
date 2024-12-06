from __future__ import annotations

import logging
from poetry.utils.authenticator import Authenticator

from typing import TYPE_CHECKING
from binance.spot import Spot as Client
from openfund.core.pyopenfund import Openfund


tools = "binance"
logger = logging.getLogger(__name__)


class BinanceTools:
    def __init__(self, openfund: Openfund) -> None:
        logger.debug("######## BinanceTools init ########")
        self._openfund: Openfund = openfund
        self._password_manager = Authenticator(
            self._openfund._poetry.config
        )._password_manager

    @property
    def api_key(self) -> str:
        return self._password_manager.get_http_auth(tools).get("username")

    @property
    def apk_secret(self) -> str:
        return self._password_manager.get_http_auth(tools).get("password")

    def get_time():
        client = Client()
        return client.time()

    def get_account(self):
        logger.debug("######## BinanceTools.get_account()  ########")
        logger.debug("######## BinanceTools api_key=%s  ########", self.api_key)
        client = Client(self.api_key, self.apk_secret)
        return client.account()
