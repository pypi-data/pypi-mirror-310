import os
import time
from functools import partial

import requests
from onoffice.actions import Action
from onoffice.cryptography import create_hmac
from onoffice.parameters import CreateParameter, Data, Parameter, ReadParameter
from onoffice.resources import Resource


class API:
    def __init__(self, token: str | None = None, secret: str | None = None):
        self.token = token if token else os.environ.get("ONOFFICE_TOKEN", None)
        self.secret = secret if secret else os.environ.get("ONOFFICE_SECRET", None)
        self.endpoint = "https://api.onoffice.de/api/stable/api.php"

    def get_hmac_and_timestamp(self, resource: Resource, action: Action) -> tuple[str, int]:
        assert (
            self.token and self.secret
        ), "You need to either set the token and secret on initialization or with environment variables."
        timestamp = int(time.time())
        hmac = create_hmac(self.token, self.secret, timestamp, resource, action)

        return hmac, timestamp

    def get_action(
        self, resource: Resource, action: Action, parameter: Parameter, resource_id: int | None = None
    ) -> dict:
        hmac, timestamp = self.get_hmac_and_timestamp(resource, action)
        return {
            "actionid": action.value,
            "resourceid": "" if not resource_id else resource_id,
            "resourcetype": resource.value,
            "identifier": "",
            "timestamp": timestamp,
            "hmac_version": "2",
            "hmac": hmac,
            "parameters": parameter.serialize(),
        }

    def read_resource(self, resource: Resource, parameter: ReadParameter):
        response = self.request([self.get_action(resource, Action.READ, parameter)])
        last_item = (parameter.page + 1) * parameter.limit
        count = response.get("count")
        if last_item < count:
            parameter.page += 1
            next_func = partial(self.read_resource, resource=resource, parameter=parameter)
            return response, next_func

        return response, None

    def create_resource(self, resource: Resource, data: Data):
        return self.request([self.get_action(resource, Action.CREATE, CreateParameter(data=data))])

    def edit_resource(self, resource: Resource, resource_id: int, data: Data):
        return self.request([self.get_action(resource, Action.EDIT, CreateParameter(data=data), resource_id)])

    def request(self, actions: list[dict]):
        data = {"token": self.token, "request": {"actions": actions}}
        response = requests.get(self.endpoint, json=data)
        json_response = response.json()
        if json_response["status"]["code"] == 500:
            return json_response["response"]["results"][0]["status"]

        data = json_response["response"]["results"][0]["data"]
        return {"count": data["meta"]["cntabsolute"], "data": data["records"]}

