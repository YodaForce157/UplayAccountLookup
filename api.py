import requests
import base64
import json

class SessionRequest:
    URL = "https://public-ubiservices.ubi.com/v3/profiles/sessions"

    def __init__(self, email, password):
        self.email = email
        self.password = password

        self.token = base64.b64encode(f"{email}:{password}".encode("utf-8")).decode("utf-8")

    def send(self) -> str:
        headers = {
            "Ubi-AppId": "e3d5ea9e-50bd-43b7-88bf-39794f4e3d40",
            "Ubi-RequestedPlatformType": "uplay",
            "Authorization": "Basic " + self.token,
            "User-Agent": "UbiServices_SDK_2020.Release.58_PC64_ansi_static",
        }

        body = {
            "rememberMe": False
        }

        return json.loads(requests.post(url=self.URL, headers=headers, json=body).content)

class AccountLookupRequest:
    def __init__(self, uuid, token):
        self.uuid = uuid
        self.token = token

        self.URL = f"https://public-ubiservices.ubi.com/v3/users/{uuid}/profiles"

    def send(self) -> str:
        session = requests.Session()
        session.headers.clear()

        headers = {
            "Authorization": "Ubi_v1 t=" + self.token,
            "Ubi-AppId": "f68a4bb5-608a-4ff2-8123-be8ef797e0a6",
            "Host": "public-ubiservices.ubi.com",
        }

        session.headers.update(headers)

        return session.get(url=self.URL.replace("#", self.uuid)).content

class InventoryRequest:
    def __init__(self, sessionId, userId, token):
        self.sessionId = sessionId
        self.token = token
        spaceId = "0d2ae42d-4c27-4cb7-af6c-2099062302bb"
        self.URL = f"https://public-ubiservices.ubi.com/v1/profiles/{userId}/inventory?spaceId={spaceId}"

    def send(self) -> str:
        headers = {
            "Ubi-SessionId": self.sessionId,
            "Ubi-LocaleCode" : "en-US",
            "Ubi-AppId": "f68a4bb5-608a-4ff2-8123-be8ef797e0a6",
            "Authorization": "Ubi_v1 t=" + self.token,
        }

        return requests.get(url=self.URL, headers=headers).content

class NameToUUIDRequest:
    def __init__(self, token, name):
        self.token = token
        self.URL = f"https://public-ubiservices.ubi.com/v3/profiles?nameOnPlatform={name}&platformType=uplay"

    def send(self) -> str:
        headers = {
            "Authorization": "Ubi_v1 t=" + self.token,
            "Ubi-AppId": "f68a4bb5-608a-4ff2-8123-be8ef797e0a6"
        }

        res =  requests.get(url=self.URL, headers=headers).content
        print(res)
        return res