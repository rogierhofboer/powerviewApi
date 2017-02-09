# Hunter Douglas PowereView blinds API

Initialize your pv instance:

```python
from powerview_api.powerview import PowerView

pv = PowerView("PowerView hub address")
scenedata = pv.get_scenes()
print(scenedata)
```

Or going for asyncio
```python
import aiohttp
import asyncio

from powerview_api.powerview_async import PowerViewAsync

loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)
pv = PowerViewAsync("192.168.2.4", session)


@asyncio.coroutine
def test(pv):
    # result = yield from pv.get_user_data()
    result = yield from pv.get_scenes()
    print(result)
    
loop.run_until_complete(test(pv))
session.close()
```