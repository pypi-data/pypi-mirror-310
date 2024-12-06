```sh
pip install openblacklist
```

# OpenBlacklist

Official client for the OpenBlacklist API.

## Description

OpenBlacklist is a Python client library for interacting with the OpenBlacklist API. It allows you to check if a user is blacklisted, handle webhooks, and trigger specific events based on webhook data.

## Installation

You can install the library using Poetry:

```sh
poetry add openblacklist
```

Or

````sh
pip install openblacklist
```

## Usage

```py
from openblacklist import OpenBlacklistClient

api_key = "your_api_key"
client = OpenBlacklistClient(api_key)
```

### Check if user is blacklisted

```py
import asyncio

async def check_user():
    user_id = 12345
    user_blacklist = await client.check_user(user_id)
    print(user_blacklist)

asyncio.run(check_user())
```

### Handling Webhooks
To handle webhooks, you need to set up an endpoint and define event handlers.

```py
@client.event("add")
async def handle_add_event(event):
    print(f"User added: {event.user}")

@client.event("remove")
async def handle_remove_event(event):
    print(f"User removed: {event.user}")

client.listen()
```

### Running the server

```py
client.listen(host="0.0.0.0", port=5000)
```

### Configuration
```py
client = OpenBlacklistClient(api_key, url="https://openbl.clarty.org/api/v1/", webhook_url="your_webhook_url")
```

## License

This project is licensed under the MIT License.
