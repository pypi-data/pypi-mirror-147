# Meroxa-py

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):

```
    $ pip install -U meroxa-py
```


## A Simple Example
```python
import asyncio

from meroxa import Meroxa
from pprint import pprint

auth="auth.token", 
url="https://api.staging.meroxa.io"

async def main():
    async with Meroxa(auth=auth, api_route=url) as m:
        resp = await m.users.me()
        pprint(resp)

asyncio.run(main())
```

To obtain a Meroxa Auth Token please see: [How to Obtain a Meroxa Access Token](https://docs.meroxa.com/guides/how-to-obtain-meroxa-access-token/)