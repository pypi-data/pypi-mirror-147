## Convert_ms

- Use this package for converting units of time to seconds.
#
## What is it?

```py
from convert_ms import ms, check

ms("1m") # return 60
ms("1h") # return 3600
ms("1d") # return 86400

check("1m") # return True
check("1o") # return False
```
#
## How to use ?
```py
from convert_ms import ms, check
import asyncio

duration = "1h"

if check(query=duration):
    await asyncio.sleep(ms(query=duration))
else:
    print("you have entered a non-existent unit of time")
```
#
### Formats
```
seconds, secs, s, m, min, minute, h, hour, d, day, w, week, mon, month, y, year
```
#
### Find a bug?
Report [here](https://github.com/Forzy8/convert_ms/issues)