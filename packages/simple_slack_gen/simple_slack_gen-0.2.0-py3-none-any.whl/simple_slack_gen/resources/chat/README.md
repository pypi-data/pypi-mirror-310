
### post_message <a name="post_message"></a>


Sends a message to a channel.

**API Endpoint**: `POST /chat.postMessage`

#### Synchronous Client

```python
from simple_slack_gen import Client
from os import getenv

client = Client(oauth_token=getenv("API_TOKEN"))
res = client.chat.post_message(
    data={
        "as_user": "string",
        "attachments": "string",
        "blocks": "string",
        "channel": "channel_id",
        "icon_emoji": "string",
        "icon_url": "string",
        "link_names": True,
        "mrkdwn": True,
        "parse": "string",
        "reply_broadcast": True,
        "text": "Hello World!",
        "thread_ts": "string",
        "unfurl_links": True,
        "unfurl_media": True,
        "username": "string",
    }
)
```

#### Asynchronous Client

```python
from simple_slack_gen import AsyncClient
from os import getenv

client = AsyncClient(oauth_token=getenv("API_TOKEN"))
res = await client.chat.post_message(
    data={
        "as_user": "string",
        "attachments": "string",
        "blocks": "string",
        "channel": "channel_id",
        "icon_emoji": "string",
        "icon_url": "string",
        "link_names": True,
        "mrkdwn": True,
        "parse": "string",
        "reply_broadcast": True,
        "text": "Hello World!",
        "thread_ts": "string",
        "unfurl_links": True,
        "unfurl_media": True,
        "username": "string",
    }
)
```
