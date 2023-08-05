# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doujinapi',
 'doujinapi.book',
 'doujinapi.item',
 'doujinapi.typings',
 'doujinapi.utils']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'httpx>=0.22.0,<0.23.0',
 'python-dotenv[cli]>=0.19.0,<0.20.0',
 'single-source>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'doujinapi',
    'version': '0.1.0',
    'description': 'Doujinshi.org unofficial wrapper of official API',
    'long_description': '# DoujinAPI2-py\n\n[Doujinshi.org](https://www.doujinshi.org/) unofficial wrapper of [official API](https://www.doujinshi.org/API_MANUAL.txt)\n\n## Requirements\n* Poetry(>=1.16)\n* Python(>=3.8.x)\n* [Doujinshi.org API KEY](https://www.doujinshi.org/settings/)\n\n## Usage\n```bash\n(TODO: publish on pypi)\n```\n\n```python\nimport asyncio\nfrom doujinApi import DoujinApi\n\n# You can get api key from doujinshi.org easily.\nclient = DoujinApi("INPUT_YOUR_API_KEY")\n\nasync def main():\n    searchResult = await client.searchBookByName("魔法少女は深淵になにをみるか?")\n    return searchResult\n\nbooks = asyncio.run(main())\nprint(books)\n\n# And you\'ll get below\n[Book(\n    id=\'B868487\',\n    name_jp=\'魔法少女は深淵になにをみるか?\',\n    name_en=None,\n    name_r=None,\n    authors=[Author(\n        id=\'A109490\',\n        name_jp=\'彩電\',\n        name_en=None,\n        name_r=\'None\',\n        name_alt=[],\n        count=47\n    )],\n    circles=[Circle(\n        id=\'C69210\',\n        name_jp=\'こねこぼたん\',\n        name_en=None,\n        name_r=\'コネコボタン\',\n        name_alt=[],\n        count=41,\n        authors=[]\n    )],\n    parodies=[Parody(\n        id=\'P4828\',\n        name_jp=\'ご注文はうさぎですか?\',\n        name_en=\'Is the Order a Rabbit?\',\n        name_r=\'ゴチュウモンハウサギデスカ\',\n        name_alt=[\'Gochūmon wa Usagi Desu ka?\',\n        \'gochuumon wa usagi desu ka\'],\n        count=1944,\n        contents=[],\n        characters=[]\n    )],\n    characters=[\n        Character(\n            id=\'H23212\',\n            name_jp=\'香風智乃\',\n            name_en=\'Kafuu Chino\',\n            name_r=\'カフウチノ\',\n            name_alt=[\'チノ\'],\n            count=576,\n            sex=<Sex.FEMALE: 2>,\n            age=13,\n            contents=[]\n        ),\n        Character(\n            id=\'H23211\',\n            name_jp=\'保登心愛\',\n            name_en=\'Hoto Kokoa\',\n            name_r=\'ホトココア\',\n            name_alt=[\n                \'ココア\',\n                \'Cocoa\'\n            ],\n            count=400,\n            sex=<Sex.FEMALE: 2>,\n            age=None,\n            contents=[],\n        )\n    ],\n    contents=[Content(\n            name_jp=\'不詳\',\n            name_en=\'Unknown\',\n            name_r=None,\n            count=1601292,\n    )],\n    date_released=datetime.date(2015, 12, 29),\n    event=Convention(\n        id=\'N2386\',\n        name_jp=\'コミックマーケット 89\',\n        name_en=\'Comic Market 89\',\n        name_r=\'コミックマーケット89\',\n        name_alt=[\'コミックマーケット89\'],\n        count=16268,\n        date_start=datetime.date(2015,12,29),\n        date_end=datetime.date(2015,12,31)\n    ),\n    image=\'https://img.doujinshi.org/big/434/868487.jpg\',\n    url=\'https://www.doujinshi.org/book/868487\',\n    pages=28,\n    nsfw=False,\n    anthology=False,\n    copyshi=False,\n    magazine=False,\n    isbn=None,\n    language=<Language.JAPANESE: 3>\n)]\n\n# And you can parse the book as filename\nfilename = client.parseBookAsFilename(books[0])\nprint(filename)\n\n# And you\'ll see below\n(C89) [こねこぼたん (彩電)] 魔法少女は深淵になにをみるか? (ご注文はうさぎですか?)\n\n# Also you can search book by image\nasync def main2():\n    resp = await client.searchBookByImage("RELATIVE_PATH_TO_IMAGE")\n    return resp\n```\n\n## Note\nDoujinshi.org API is really complex for me.\nPlease make an issue if something is wrong.\n\nThis is rechallenge after 5 years past.\nDoes this code looks better than [before](https://github.com/Dosugamea/DoujinAPI-py)? XD\n\nSometimes doujinshi.org server goes down, but don\'t worry, the server will come back soon :v',
    'author': 'Dosugamea',
    'author_email': 'dsgamer777@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dosugamea/DoujinAPI2-py#readme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
