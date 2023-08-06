# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qosic']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'polling2>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'qosic-sdk',
    'version': '4.0.0',
    'description': 'An unofficial python sdk for the QosIc platform.',
    'long_description': 'qosic-sdk\n=========\n\nAn unofficial python sdk for the `QosIC <https://www.qosic.com/>`__\nplatform. This platform provides an api to enable mobile money payments\nfor businesses in Africa.\n\n\n.. image:: https://img.shields.io/pypi/v/qosic-sdk.svg\n        :target: https://pypi.python.org/pypi/qosic-sdk\n\n.. image:: https://img.shields.io/pypi/pyversions/qosic-sdk\n        :target: https://github.com/Tobi-De/qosic-sdk\n\n.. image:: https://api.travis-ci.com/Tobi-De/qosic-sdk.svg\n        :target: https://travis-ci.com/Tobi-De/qosic-sdk\n\n.. image:: https://readthedocs.org/projects/qosic-sdk/badge/?version=latest\n        :target: https://qosic-sdk.readthedocs.io/en/latest/?version=latest\n        :alt: Documentation Status\n\n.. image:: https://img.shields.io/apm/l/atomic-design-ui.svg?\n        :target: https://github.com/Tobi-De/qosic-sdk/blob/master/LICENSE\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n        :target: https://github.com/psf/black\n\n----\n\n-  Free software: MIT license\n-  Documentation: https://qosic-sdk.readthedocs.io.\n\nFeatures\n--------\n\n-  Simple synchronous client to make your payment requests\n-  Cover 100% of Qosic public api\n-  Clean and meaningful exceptions\n-  100 % test coverage\n-  Configurable timeouts\n\nQuickstart\n----------\n\nFor those of you in a hurry, here’s a sample code to get you started.\n\n.. code:: shell\n\n       pip install qosic-sdk\n\n.. code:: python3\n\n\n       from dotenv import dotenv_values\n       from qosic import Client, MTN, MOOV\n\n       config = dotenv_values(".env")\n\n       moov_client_id = config.get("MOOV_CLIENT_ID")\n       mtn_client_id = config.get("MTN_CLIENT_ID")\n       server_login = config.get("SERVER_LOGIN")\n       server_pass = config.get("SERVER_PASSWORD")\n       # This is just for test purpose, you should directly pass the phone number\n       phone = config.get("PHONE_NUMBER")\n\n\n       def main():\n           client = Client(\n               login=server_login,\n               password=server_pass,\n               providers=[MTN(id=mtn_client_id), MOOV(id=moov_client_id)],\n           )\n           result = client.pay(phone=phone, amount=500, first_name="User", last_name="TEST")\n           print(result)\n           if result.success:\n               print(f"Everything went fine")\n\n           result = client.refund(reference=result.reference)\n           print(result)\n\n\n       if __name__ == "__main__":\n           main()\n\nCredits\n-------\n\nThis package was created with\n`Cookiecutter <https://github.com/audreyr/cookiecutter>`__ and the\n`audreyr/cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`__\nproject template.\n\n',
    'author': 'Tobi-De',
    'author_email': 'tobidegnon@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tobi-De/qosic-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
