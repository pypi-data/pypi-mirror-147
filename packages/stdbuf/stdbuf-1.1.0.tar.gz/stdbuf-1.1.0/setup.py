# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stdbuf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stdbuf',
    'version': '1.1.0',
    'description': 'Size and time aware deduplicated asynchronous buffer.',
    'long_description': '# Stdbuf\n\n[![CI][ci-image]][ci-url]\n[![codecov][codecov-image]][codecov-url]\n\n[ci-url]: https://github.com/dikuchan/stdbuf/actions/workflows/ci.yaml\n[ci-image]: https://github.com/dikuchan/stdbuf/actions/workflows/ci.yaml/badge.svg\n\n[codecov-url]: https://codecov.io/gh/dikuchan/stdbuf\n[codecov-image]: https://codecov.io/gh/dikuchan/stdbuf/branch/master/graph/badge.svg?token=EWNC1RJZOK\n\nSize and time bounded asynchronous buffer with deduplication. \n\nBuffer\'s content is flushed when either maximum size or time since\nthe first insertion reaches the specified limits.\n\nInspired by [ClickHouse buffer engine](https://clickhouse.com/docs/en/engines/table-engines/special/buffer/). Used for\nthe same purpose.\n\n### Note\n\nMultiple concurrent consumers are not supported.\n\n### Usage\n\n```python\nimport asyncio\nimport time\n\nfrom stdbuf import Stdbuf\n\n\nasync def produce(buf: Stdbuf[int]):\n    for i in range(2 ** 16):\n        await buf.put(i)\n        # Duplicates are ignored.\n        await buf.put(i)\n\n\nasync def consume(buf: Stdbuf[int]):\n    while True:\n        start = time.perf_counter()\n        # Get data at least every 2 seconds.\n        # May return earlier if full.\n        data = await buf.get()\n        elapsed = time.perf_counter() - start\n        assert len(data) <= 16\n        assert elapsed <= 0.5 + 1e-2\n\n\nasync def main():\n    with Stdbuf(16, 0.5, True) as buf:\n        done, pending = await asyncio.wait({\n            asyncio.create_task(produce(buf)),\n            asyncio.create_task(consume(buf)),\n        },\n            return_when=asyncio.FIRST_COMPLETED,\n        )\n        for task in pending:\n            task.cancel()\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```',
    'author': 'dikuchan',
    'author_email': 'dikuchan@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dikuchan/stdbuf.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
