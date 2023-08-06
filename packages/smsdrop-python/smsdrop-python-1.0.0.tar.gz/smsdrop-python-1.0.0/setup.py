# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smsdrop']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0',
 'mkdocs-include-markdown-plugin>=3.3.0,<4.0.0',
 'mkdocs-material-extensions>=1.0.3,<2.0.0',
 'mkdocs-material>=8.2.9,<9.0.0',
 'mkdocs>=1.3.0,<2.0.0',
 'mkdocstrings>=0.18.1,<0.19.0',
 'tenacity>=8.0.1,<9.0.0']

extras_require = \
{'redis': ['redis==4.2.2']}

setup_kwargs = {
    'name': 'smsdrop-python',
    'version': '1.0.0',
    'description': 'A python sdk for the smsdrop.net platform',
    'long_description': '# Smsdrop-Python\n\n[![](https://img.shields.io/pypi/v/smsdrop-python.svg)](https://pypi.python.org/pypi/smsdrop-python)\n[![python](https://img.shields.io/pypi/pyversions/smsdrop-python)](https://github.com/EdevTech/smsdrop-python)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/EdevTech/smsdrop-python/blob/master/LICENSE)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n- Documentation: <a href="https://tobi-de.github.io/smsdrop-python/" target="_blank">https://tobi-de.github.io/smsdrop-python/</a>\n- Source Code: <a href="https://github.com/Tobi-De/smsdrop-python/" target="_blank">https://github.com/Tobi-De/smsdrop-python/</a>\n\nThe official python sdk for the [smsdrop](https://smsdrop.net) api.\n\n## Quickstart\n\n```python\nimport datetime\nimport logging\nimport time\n\nimport pytz\nfrom dotenv import dotenv_values\n\nfrom smsdrop import Campaign, Client, RedisStorage\n\n# Enable Debug Logging\n# This will og the API request and response data to the console:\nlogging.basicConfig(level=logging.DEBUG, format="%(message)s")\n\nconfig = dotenv_values(".env")\n\nTEST_EMAIL = config.get("TEST_EMAIL")\nTEST_PASSWORD = config.get("TEST_PASSWORD")\nMY_TIMEZONE = config.get("MY_TIMEZONE")\n\n\ndef main():\n    # Initialize the client\n    client = Client(\n        email=TEST_EMAIL, password=TEST_PASSWORD, storage=RedisStorage()\n    )\n    # Get your account profile information\n    print(client.get_profile())\n    # Get your subscription information\'s\n    print(client.get_subscription())\n    # Get your first 500 campaigns\n    print(client.get_campaigns(skip=0, limit=500))\n\n    # Send a simple sms\n    client.send_message(message="hi", sender="Max", phone="<phone>")\n\n    # Create a new Campaign\n    cp = Campaign(\n        title="Test Campaign",\n        message="Test campaign content",\n        sender="TestUser",\n        recipient_list=["<phone1>", "<phone2>", "<phone3>"],\n    )\n    client.launch(cp)\n    time.sleep(20)  # wait for 20 seconds for the campaign to proceed\n    client.refresh(cp)  # refresh your campaign data\n    print(cp.status)  # Output Example : COMPLETED\n\n    # create a scheduled campaign\n    naive_dispatch_date = datetime.datetime.now() + datetime.timedelta(hours=1)\n    aware_dispatch_date = pytz.timezone(MY_TIMEZONE).localize(\n        naive_dispatch_date\n    )\n    cp2 = Campaign(\n        title="Test Campaign 2",\n        message="Test campaign content 2",\n        sender="TestUser",\n        recipient_list=["<phone1>", "<phone2>", "<phone3>"],\n        # The date will automatically be sent in iso format with the timezone data\n        defer_until=aware_dispatch_date,\n    )\n    client.launch(cp2)\n    # If you check the status one hour from now it should return \'COMPLETED\'\n\n    # create another scheduled campaign using defer_by\n    cp3 = Campaign(\n        title="Test Campaign 3",\n        message="Test campaign content 3",\n        sender="TestUser",\n        recipient_list=["<phone1>", "<phone2>", "<phone3>"],\n        defer_by=120,\n    )\n    client.launch(cp3)\n    time.sleep(120)  # wait for 120 seconds for the campaign to proceed\n    client.refresh(cp3)  # refresh your campaign data\n    print(cp3.status)  # should output : COMPLETED\n    # If you get a \'SCHEDULED\' printed, you can wait 10 more seconds in case the network\n    # is a little slow or the server is busy\n\n\nif __name__ == "__main__":\n    main()\n```\n',
    'author': 'Tobi DEGNON',
    'author_email': 'tobidegnon@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tobi-De/smsdrop-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
