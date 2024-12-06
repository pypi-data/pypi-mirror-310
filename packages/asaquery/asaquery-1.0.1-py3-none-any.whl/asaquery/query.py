import base64
import datetime
from typing import Final

import aiohttp
import requests

from .response import AccessTokenResponse, QueryResponse, Session


class Query:
    "The class for querying to Epic Games API"

    endpoint: Final[str] = "https://api.epicgames.dev"

    clientId: Final[str] = "xyza7891muomRmynIIHaJB9COBKkwj6n"
    clientSecret: Final[str] = "PP5UGxysEieNfSrEicaD1N2Bb3TdXuD7xHYcsdUHZ7s"
    deploymentId: Final[str] = "ad9a8feffb3b4b2ca315546f038c3ae2"

    accessToken: str | None = None
    accessTokenExpiresAt: float = 0

    @property
    def authorization(self) -> str:
        return "Basic {}".format(
            base64.b64encode(f"{self.clientId}:{self.clientSecret}".encode()).decode()
        )

    def getAccessTokenSync(self) -> str:
        """
        Get access token and set it to self.accessToken
        """
        url = f"{self.endpoint}/auth/v1/oauth/token"
        body = {
            "grant_type": "client_credentials",
            "deployment_id": self.deploymentId,
        }
        headers = {
            "Authorization": self.authorization,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        httpResponse = requests.post(url, data=body, headers=headers)

        if httpResponse.status_code != 200:
            raise Exception("Failed to get access token")

        response: AccessTokenResponse = httpResponse.json()

        accessToken = response.get("access_token")
        if accessToken is None:
            raise Exception("Failed to get access token")

        self.accessToken = accessToken
        expires = response.get("expires_at")
        self.accessTokenExpiresAt = datetime.datetime.strptime(
            expires, "%Y-%m-%dT%H:%M:%S.%fZ"
        ).timestamp()

        return accessToken

    async def getAccessToken(self) -> str:
        """
        Get access token and set it to self.accessToken
        """
        url = f"{self.endpoint}/auth/v1/oauth/token"
        body = {
            "grant_type": "client_credentials",
            "deployment_id": self.deploymentId,
        }
        headers = {
            "Authorization": self.authorization,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=body, headers=headers) as httpResponse:
                if httpResponse.status != 200:
                    raise Exception("Failed to get access token")

                response: AccessTokenResponse = await httpResponse.json()

                accessToken = response.get("access_token")
                if accessToken is None:
                    raise Exception("Failed to get access token")

                self.accessToken = accessToken
                expires = response.get("expires_at")
                self.accessTokenExpiresAt = datetime.datetime.strptime(
                    expires, "%Y-%m-%dT%H:%M:%S.%fZ"
                ).timestamp()

                return accessToken

    def getQuerySync(self, address: str, port: int) -> QueryResponse:
        """
        Query to Epic Games API
        """
        if self.accessToken is None or self.accessTokenExpiresAt is None:
            self.getAccessTokenSync()

        if self.accessTokenExpiresAt < datetime.datetime.now().timestamp():
            self.getAccessTokenSync()

        url = f"{self.endpoint}/matchmaking/v1/{self.deploymentId}/filter"
        body = {
            "criteria": [
                {"key": "attributes.ADDRESS_s", "op": "EQUAL", "value": address}
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.accessToken}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        httpResponse = requests.post(url, json=body, headers=headers)

        if httpResponse.status_code != 200:
            raise Exception("Failed to query")

        response: QueryResponse = httpResponse.json()
        return response

    async def getQuery(self, address: str, port: int) -> QueryResponse:
        """
        Query to Epic Games API
        """
        if self.accessToken is None or self.accessTokenExpiresAt is None:
            await self.getAccessToken()

        if self.accessTokenExpiresAt < datetime.datetime.now().timestamp():
            await self.getAccessToken()

        url = f"{self.endpoint}/matchmaking/v1/{self.deploymentId}/filter"
        body = {
            "criteria": [
                {"key": "attributes.ADDRESS_s", "op": "EQUAL", "value": address}
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.accessToken}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as httpResponse:
                if httpResponse.status != 200:
                    raise Exception("Failed to query")

                response: QueryResponse = await httpResponse.json()
                return response

    def parseResponse(
        self, response: QueryResponse, address: str, port: int
    ) -> Session:
        count = response.get("count")
        if count == 0:
            raise Exception("No results")

        targetServer = next(
            filter(
                lambda x: x["attributes"].get("ADDRESSBOUND_s") == f"0.0.0.0:{port}"
                or x["attributes"].get("ADDRESSBOUND_s") == f"{address}:{port}"
                or x["attributes"].get("GAMESERVER_PORT_1") == port,
                response["sessions"],
            ),
            None,
        )

        if targetServer is None:
            raise Exception("No results")

        target = Session(
            name=targetServer["attributes"]["SESSIONNAME_s"],
            map=targetServer["attributes"]["MAPNAME_s"],
            password=targetServer["attributes"]["SERVERPASSWORD_b"],
            numplayers=targetServer["totalPlayers"],
            maxplayers=targetServer["settings"]["maxPublicPlayers"],
            players=[p.get("name") for p in targetServer["publicPlayers"]],
            version="{}.{}".format(
                targetServer["attributes"]["BUILDID_s"],
                targetServer["attributes"]["MINORBUILDID_s"],
            ),
            raw=targetServer,
        )

        return target

    def query(self, address: str, port: int) -> Session:
        response = self.getQuerySync(address, port)
        return self.parseResponse(response, address, port)

    async def queryAsync(self, address: str, port: int) -> Session:
        response = await self.getQuery(address, port)
        return self.parseResponse(response, address, port)
