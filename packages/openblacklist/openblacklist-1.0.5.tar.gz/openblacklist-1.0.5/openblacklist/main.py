from fastapi import Body, FastAPI
import uvicorn
from typing import Optional, Dict, List, Callable
import aiohttp
from .method.Model import UserBlacklist, User, Reason, UserBlacklistWebhook

class OpenBlacklistClient:
    def __init__(self, api_key: str, url='https://openbl.clarty.org/api/v1/', webhook_url: Optional[str] = None):
        self.url = url
        self.api_key = api_key
        self.webhook_url = webhook_url
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.app = FastAPI()

        # Configure l'endpoint pour les webhooks
        if webhook_url:
            self.setup_webhook_endpoint()

    async def check_user(self, user_id: int) -> UserBlacklist:
        """Vérifie si un utilisateur est blacklisté."""
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(
                self.url + f"/user/{user_id}", headers={"Authorization": self.api_key}
            ) as resp:
                return await resp.json()
        return UserBlacklist(**data)

    async def handle_webhook(self, data: dict):
        """Gère les données reçues via webhook et déclenche des événements spécifiques."""
        user = User(**data['user'])
        reason = Reason(**data['reasons'])
        metadata = data['metadata']
        webhook_event = UserBlacklistWebhook(user=user, reason=reason, metadata=metadata)

        # Détermine l'événement à déclencher en fonction de metadata
        event_name = metadata.get("event")  # Exemple : "add" ou "remove"
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                await handler(webhook_event)
        
        return webhook_event

    def event(self, event_name: str):
        """Décorateur pour enregistrer un gestionnaire d'événements."""
        def decorator(func):
            if event_name not in self.event_handlers:
                self.event_handlers[event_name] = []
            self.event_handlers[event_name].append(func)
            return func
        return decorator

    def setup_webhook_endpoint(self):
        """Ajoute un endpoint webhook à l'application FastAPI."""
        @self.app.post(f"/{self.webhook_url}")
        async def webhook_listener(data: dict = Body(...)):
            await self.handle_webhook(data)
            return {"status": "success"}

    def listen(self, host: str = "0.0.0.0", port: int = 5000):
        """Démarre le serveur pour écouter les événements webhook."""
        uvicorn.run(self.app, host=host, port=port,log_config=None)
