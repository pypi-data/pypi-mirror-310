
# Slack Python SDK

## Overview
One way to interact with the Slack platform is its HTTP RPC-based Web API, a collection of methods requiring OAuth 2.0-based user, bot, or workspace tokens blessed with related OAuth scopes.

### Synchronous Client

```python
from simple_slack_gen import Client
from os import getenv

client = Client(oauth_token=getenv("API_TOKEN"))
```

### Asynchronous Client

```python
from simple_slack_gen import AsyncClient
from os import getenv

client = AsyncClient(oauth_token=getenv("API_TOKEN"))
```

## Module Documentation and Snippets

### [chat](simple_slack_gen/resources/chat/README.md)

* [post_message](simple_slack_gen/resources/chat/README.md#post_message) - 

### [conversations](simple_slack_gen/resources/conversations/README.md)

* [list](simple_slack_gen/resources/conversations/README.md#list) - 

<!-- MODULE DOCS END -->
