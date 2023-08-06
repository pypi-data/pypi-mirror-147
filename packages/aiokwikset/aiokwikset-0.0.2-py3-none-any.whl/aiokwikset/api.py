import json
from datetime import datetime, timedelta, time
from typing import Optional

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError, ClientResponseError, ClientConnectorError, ServerConnectionError, ClientPayloadError

from .errors import RequestError
from .device import Device
from .user import User

from aiokwikset.aws_kwikset import AWSKWIKSET

from aiokwikset.const import (
    POOL_ID,
    CLIENT_ID,
    POOL_REGION,
    LOGGER
)

class API(object):
    def __init__(self, username: str, password: str, *, session: Optional[ClientSession] = None
    ) -> None:
        self._username: str = username
        self._password: str = password
        self._session: ClientSession = session
        self.token = {}

        self.device: Optional[Device] = None
        self.user: Optional[User] = None

    async def _request(self, method: str, url: str, **kwargs) -> dict:
        """Make a request against the API."""

        if self.token.get('expires_at') and datetime.now() >= self.token.get('expires_at', 0):
            LOGGER.info("Requesting new access token to replace expired one")

            await self._refresh_token()

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=120))

        try:
            async with session.request(method, url, **kwargs) as resp:
                data: dict = await resp.json(content_type=None)
                resp.raise_for_status()
                return data

        except ClientResponseError as err:
            raise RequestError(f"There was a response error while requesting {url}: {err}") from err
        except ClientConnectorError as err:
            raise RequestError(f"There was a client connection error while requesting {url}: {err}") from err
        except ServerConnectionError as err:
            raise RequestError(f"There was a server connection error while requesting {url}: {err}") from err
        except ClientPayloadError as err:
            raise RequestError(f"There was a client payload error while requesting {url}: {err}") from err
        except ClientError as err:
            raise RequestError(f"There was the following error while requesting {url}: {err}") from err
        finally:
            if not use_running_session:
                await session.close()

    async def _get_initial_token(self) -> None:
        aws = AWSKWIKSET(username=self._username, password=self._password, pool_id=POOL_ID,
                         client_id=CLIENT_ID, pool_region=POOL_REGION)

        await self._store_token(await aws.authenticate_user())

        if not self.device:
            self.device = Device(self._request, self.token.get("IdToken"))

        if not self.user:
            self.user = User(self._request, self.token['IdToken'])

    async def _store_token(self, js):
        self.token = js['AuthenticationResult']
        assert 'AccessToken' in self.token, self.token
        assert 'ExpiresIn' in self.token, self.token
        assert 'IdToken' in self.token, self.token
        assert 'RefreshToken' in self.token, self.token
        self.token['expires_at'] = datetime.now() + timedelta(seconds=self.token['ExpiresIn'])
        LOGGER.debug(f'received token, expires {self.token["expires_at"]}')

    async def _refresh_token(self):
        """
        Sets a new access token on the User using the refresh token.
        """
        await self._store_token(await aws.refresh_auth_token(self.token['RefreshToken']))

async def async_get_api(
    username: str, password: str, *, session: Optional[ClientSession] = None
) -> API:
    ks = API(username,password)
    await ks._get_initial_token()
    return ks
