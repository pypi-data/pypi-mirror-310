
### list <a name="list"></a>


Lists channels in the workspace.

**API Endpoint**: `GET /conversations.list`

#### Synchronous Client

```python
from simple_slack_gen import Client
from os import getenv

client = Client(oauth_token=getenv("API_TOKEN"))
res = client.conversations.list(
    cursor="dXNlcjpVMDYxTkZUVDI=",
    exclude_archived=True,
    limit=10,
    team_id="T1234567890",
    types_query="public_channel,private_channel",
)
```

#### Asynchronous Client

```python
from simple_slack_gen import AsyncClient
from os import getenv

client = AsyncClient(oauth_token=getenv("API_TOKEN"))
res = await client.conversations.list(
    cursor="dXNlcjpVMDYxTkZUVDI=",
    exclude_archived=True,
    limit=10,
    team_id="T1234567890",
    types_query="public_channel,private_channel",
)
```
