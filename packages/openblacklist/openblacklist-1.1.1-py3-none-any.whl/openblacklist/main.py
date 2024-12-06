import aiohttp
from fastapi import Body, FastAPI
import uvicorn
from typing import Optional, Dict, List, Callable
from .method.Model import UserBlacklist, User, Reason, UserBlacklistWebhook

class BlacklistClient:
    def __init__(self, api_key: str=None, url='https://openbl.clarty.org/api/v1/', webhook_url: Optional[str] = None,webhook_pass: str=None):
        """
        Initializes the OpenBlacklistClient.

        Args:
            api_key (str): The API key for authentication.
            url (str, optional): The base URL for the API. Defaults to 'https://openbl.clarty.org/api/v1/'.
            webhook_url (Optional[str], optional): The URL for the webhook endpoint. Defaults to None.
            webhook_pass (str): The password for the webhook endpoint.
        """
        self.url = url
        self.api_key = api_key
        self.webhook_url = webhook_url
        self.webhook_pass = webhook_pass
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.app = FastAPI()

        if webhook_url:
            self._setup_webhook_endpoint()

    async def check_user(self, user_id: int) -> UserBlacklist:
        """
        Checks if a user is blacklisted.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            UserBlacklist: The blacklist information of the user.
        """
        if not self.api_key:
            raise ValueError("API key is required to check user blacklist status")
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(
                self.url + f"/user/{user_id}", headers={"Authorization": self.api_key}
            ) as resp:
                data = await resp.json()
                if data.get("isBlacklisted"):
                    return UserBlacklist(**data)
                else:
                    return UserBlacklist(isBlacklisted=False, user=User(id=user_id, username="",blacklisted_reasons=Reason(fr_fr="", en_gb="", es_sp="")))
    async def _handle_webhook(self, data: dict):
        """
        Handles data received via webhook and triggers specific events.

        Args:
            data (dict): The data received from the webhook.

        Returns:
            UserBlacklistWebhook: The webhook event data.
        """
        user = User(**data['user'])
        reason = Reason(**data['reasons'])
        metadata = data['metadata']
        if metadata.get("pass") != self.webhook_pass:
            return
        webhook_event = UserBlacklistWebhook(user=user, reason=reason, metadata=metadata)

        event_name = metadata.get("event")
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                await handler(webhook_event)

        return webhook_event

    def _event(self, event_name: str): 
        """
        Decorator to register an event handler.

        Args:
            event_name (str): The name of the event to handle.

        Returns:
            Callable: The decorator function.
        """
        def decorator(func):
            if event_name not in self.event_handlers:
                self.event_handlers[event_name] = []
            self.event_handlers[event_name].append(func)
            return func
        return decorator

    def _setup_webhook_endpoint(self):
        """
        Adds a webhook endpoint to the FastAPI application.
        """
        @self.app.post(f"/{self.webhook_url}")
        async def webhook_listener(data: dict = Body(...)):
            await self._handle_webhook(data)
            return {"status": "success"}

    def listen(self, host: str = "0.0.0.0", port: int = 5000):
        """
        Starts the server to listen for webhook events.

        Args:
            host (str, optional): The host to bind to. Defaults to "0.0.0.0".
            port (int, optional): The port to bind to. Defaults to 5000.
        """
        uvicorn.run(self.app, host=host, port=port, log_config=None)
