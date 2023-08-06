# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['convert_ms']
setup_kwargs = {
    'name': 'convert-ms',
    'version': '0.0.4',
    'description': 'Convert a time units to seconds',
    'long_description': '## Convert_ms\n\n- Use this package for converting units of time to seconds.\n#\n## What is it?\n\n```py\nfrom convert_ms import ms, check\n\nms("1m") # return 60\nms("1h") # return 3600\nms("1d") # return 86400\n\ncheck("1m") # return True\ncheck("1o") # return False\n```\n#\n## How to use ?\n```py\nfrom convert_ms import ms, check\nimport asyncio\n\nduration = "1h"\n\nif check(query=duration):\n    await asyncio.sleep(ms(query=duration))\nelse:\n    print("you have entered a non-existent unit of time")\n```\n#\n### Formats\n```\nseconds, secs, s, m, min, minute, h, hour, d, day, w, week, mon, month, y, year\n```\n#\n### Find a bug?\nReport [here](https://github.com/Forzy8/convert_ms/issues)',
    'author': 'Forzy',
    'author_email': 'nikita11tzby@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Forzy8/convert_ms',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
