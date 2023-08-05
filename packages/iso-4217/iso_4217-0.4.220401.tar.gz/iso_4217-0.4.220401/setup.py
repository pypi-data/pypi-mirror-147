# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iso_4217']

package_data = \
{'': ['*'], 'iso_4217': ['data/*']}

extras_require = \
{'pint': ['pint>=0.16,<0.17']}

setup_kwargs = {
    'name': 'iso-4217',
    'version': '0.4.220401',
    'description': 'ISO 4217 currency code library',
    'long_description': '``iso_4217``: Yet another currency data package for Python\n==========================================================\n.. image:: https://github.com/ikseek/iso_4217/workflows/Python%20package/badge.svg\n.. image:: https://img.shields.io/pypi/v/iso-4217?style=plastic\n   :target: https://pypi.org/project/iso-4217/\n\nThis package contains ISO 4217 *active* and *historical* currency data.\nWritten and tested for Python 3.6 and above.\nSupports `pint`_ for operations with currency units.\n\n>>> from iso_4217 import Currency\n>>> Currency.USD\n<Currency.USD: \'US Dollar\'>\n>>> Currency.USD.value\n\'US Dollar\'\n>>> Currency.USD.number\n840\n>>> Currency(\'US Dollar\')\n<Currency.USD: \'US Dollar\'>\n>>> Currency.JPY.entities\nfrozenset({\'JAPAN\'})\n>>> Currency.ZWR\n<Currency.ZWR: \'Zimbabwe Dollar (2009)\'>\n>>> Currency.ZWR.entities\nfrozenset()\n>>> Currency.ZWR.withdrew_entities\n(Historic(entity=\'ZIMBABWE\', name=\'Zimbabwe Dollar\'...2009, month=6), begin=None)),)\n>>> Currency.VED\n<Currency.VED: \'Bolívar Soberano (VED)\'>\n\n\nPint units and subunits are available with convenient :code:`unit` and :code:`subunit`\nproperties on Currency. Accessing these properties requires `pint` package installed\nand automatically defines currency units in application default registry.\n\n>>> Currency.USD.unit * 5 + Currency.USD.subunit * 5\n<Quantity(5.05, \'USD\')>\n\nCurrency units can be defined in any UnitRegistry manually\n\n>>> import pint\n>>> from decimal import Decimal\n>>> from iso_4217 import define_currency_units\n>>> reg = define_currency_units(pint.UnitRegistry(non_int_type=Decimal))\n>>> 5 * reg.USD\n<Quantity(5, \'USD\')>\n\nBut units from separate registries should not be mixed\n\n>>> Currency.USD.unit == reg.USD\nTraceback (most recent call last):\n...\nValueError: Cannot operate with Unit and Unit of different registries.\n\nIf you want to replace registry used by Currency just replace the application registry:\n\n>>> pint.set_application_registry(reg)\n>>> Currency.USD.unit == reg.USD\nTrue\n\nSubunits are defined with `s` suffix:\n\n>>> 5 * reg.USDs\n<Quantity(5, \'USDs\')>\n>>> (5 * reg.USDs).to("USD")\n<Quantity(0.05, \'USD\')>\n>>> (5 * reg.BHDs).to_base_units()\n<Quantity(0.005, \'BHD\')>\n\nEach currency is defined within it\'s own dimension:\n\n>>> (5 * reg.USD).to(\'EUR\')\nTraceback (most recent call last):\n...\npint.errors.DimensionalityError: Cannot convert from \'USD\' ([currency_USD]) to \'EUR\' ([currency_EUR])\n\nBut automatic currency conversion can be made via pint Contexts\n\n>>> context = pint.Context()\n>>> eur_to_usd = lambda r, eur: eur * r("1.2 USD/EUR")\n>>> context.add_transformation("[currency_EUR]", "[currency_USD]", eur_to_usd)\n>>> (Currency.EUR.unit * 5).to(\'USD\', context)\n<Quantity(6.0, \'USD\')>\n\nInspired by `iso4217`_ package by Hong Minhee.\n\n.. _iso4217: https://github.com/dahlia/iso4217\n.. _pint: https://pint.readthedocs.io\n',
    'author': 'Igor Kozyrenko',
    'author_email': 'igor@ikseek.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ikseek/iso_4217',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
