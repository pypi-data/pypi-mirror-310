from __future__ import annotations

import os
import logging
import requests

from pathlib import Path
from typing import TYPE_CHECKING

from openfund.core.factory import Factory
from openfund.core.binance_tools.binance_tools import BinanceTools

from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from openfund.core.pyopenfund import Openfund
    from tests.conftest import Config

logger = logging.getLogger(__name__)


def test_binance_get_accont_by_env_config(
    openfund: Openfund, mocker: MockerFixture
) -> None:
    logger.debug("------------ test_binance_get_accont_by_default ... -------------")

    resp = None
    try:
        resp = BinanceTools(openfund).get_account()
    except (requests.ConnectionError, requests.HTTPError) as e:
        raise HTTPError(e)
    finally:
        logger.warn("")

    logger.debug("------------ resp=%s ", resp)
    assert resp != None
