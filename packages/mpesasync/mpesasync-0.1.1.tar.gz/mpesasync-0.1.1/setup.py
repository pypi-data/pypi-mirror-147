# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mpesasync', 'mpesasync.contracts', 'mpesasync.mpesa_business']

package_data = \
{'': ['*'], 'mpesasync': ['certificates/*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'cryptography>=36.0.1,<37.0.0',
 'httpx>=0.19.0,<0.20.0',
 'pydantic>=1.8.2,<2.0.0',
 'ujson>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'mpesasync',
    'version': '0.1.1',
    'description': 'A Mpesa Daraja API library to quickly get started sending and receiving money from mpesa ',
    'long_description': '# Mpesasync\n\nA asynchronous python library to the Mpesa Daraja API.\n[Latest Release](https://pypi.org/project/mpesasync/)\n\n# Features\nThis includes the following:\n1. A python library to accept send and receive MPESA payments in less than 10 lines of code.\n2. A sample implementation of the library in fast api.\n# Installation\n`$ pip install mpesasync`\n# Development\n* Create a virtual environment `python -m venv venv`\n* Activate your virtual environment `$source venv\\bin\\activate` or in windows `> venv\\scripts\\activate`\n* Install Poetry `pip install poetry`\n* Install project `poetry install`\n* Run tests `pytest`\n\n# Getting started\n\nTo get started you need the following from the [Mpesa Daraja Portal](https://developer.safaricom.co.ke/)\n\n[STK PUSH]\n1. Your consumer key.\n2. Your consumer secret.\n3. The business shortcode.\n\n[B2C/B2B]\n\n5. Your organisation shortcode\n6. Initiator name \n7. Security credential\n8. QueueTimeOutURL\n9. Result url => This has to be a publicly accessible callback that mpesa will send transaction results to.\n\nFor testing purposes, you can get test credentials [here](https://developer.safaricom.co.ke/MyApps).\nOn the sandbox portal, create an new app and use the provided credentials.\n\n# Using the library\n## STK Push\n\n1. Initialise and authenticate the STKPush sdk\n\n```python\nfrom mpesasync import Mpesa, MpesaEnvironment\nfrom mpesasync.lipa_na_mpesa import STKPush\nmpesa_app = STKPush(\n        Environment=MpesaEnvironment.production, # use sandbox to authenticate with sandbox credentials\n        BusinessShortCode=1234, \n        CallBackURL="https://mydomain.com/path",\n        PassKey="" # use the passkey obtained from the daraja portal\n    )\nawait mpesa_app.authorize(consumer_key="YOUR CONSUMER KEY",\n                              consumer_secret="YOUR CONSUMER SECRET")\n```\n2. Send an STKPush prompt\n```python\nawait mpesa_app.stk_push(\n        amount=1.0, phone_number="phone number"\n    )\n```\n\n_The phone number can be any of +254XXXXXXXXX, 254XXXXXXXXX, 0XXXXXXXXX, the SDK will sanitise the phone numbers for you._\n\nIf the transaction is sucessfull, mpesa will send a confirmation to your configured callback url.\nYou can also use the library to parse the json data.\nA callback implemented in [FastAPI](https://fastapi.tiangolo.com/) could look like.\n```python\n## main.py\n\nfrom mpesasync.contracts import STKPushResult\n\nfrom typing import Optional\n\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("stkpush/callback")\ndef stk_push_callback(data: STKPushResult):\n    ## do your zing\n    print(data)\n    return {"OK"}\n\n```\nStart the server\n\n`$ uvicorn main:app --reload`\n\n',
    'author': 'Pius Dan',
    'author_email': 'npiusdan@gmail.com',
    'maintainer': 'Pius Dan(darklotus)',
    'maintainer_email': 'npiusdan@gmail.com',
    'url': 'https://github.com/Piusdan/mpesasync',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
