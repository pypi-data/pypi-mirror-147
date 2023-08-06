# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reportbro']

package_data = \
{'': ['*'], 'reportbro': ['data/*']}

install_requires = \
['Babel>=2.9.1,<3.0.0',
 'Pillow>=4.0',
 'XlsxWriter>=3.0.2,<4.0.0',
 'qrcode>=7.3.1,<8.0.0',
 'reportbro-fpdf>=1.7.11,<2.0.0',
 'reportbro-simpleeval>=0.9.11,<0.10.0']

extras_require = \
{':python_version < "3.4"': ['enum34>=1.1.10,<2.0.0'],
 ':python_version < "3.5"': ['typing>=3.10.0,<4.0.0']}

setup_kwargs = {
    'name': 'reportbro-lib',
    'version': '2.1.0',
    'description': 'Generate PDF and Excel reports from visually designed templates',
    'long_description': "ReportBro Lib\n=================\n\nReportBro is a library to generate PDF and XLSX reports. Report templates can be created\nwith `ReportBro Designer <https://github.com/jobsta/reportbro-designer>`_,\na Javascript Plugin which can be integrated in your web application.\n\nSee the ReportBro project website on https://www.reportbro.com for full documentation and demos.\n\nFeatures\n--------\n\n* Python 2.7 and Python >= 3.5 support\n* Generate pdf and xlsx reports\n* Supports (repeating) header and footer\n* Allows predefined and own page formats\n* Use text, line, images, barcodes and tables, page breaks\n* Text and element styling\n* Evaluate expressions, define conditional styles, format parameters\n\nInstallation\n------------\n\n.. code:: shell\n\n    pip install reportbro-lib\n\nGo to https://www.reportbro.com/doc/api#lib-arguments for more information on configuration and usage.\n\nPython Coding Style\n-------------------\n\nThe `PEP 8 (Python Enhancement Proposal) <https://www.python.org/dev/peps/pep-0008/>`_\nstandard is used which is the de-facto code style guide for Python. An easy-to-read version\nof PEP 8 can be found at https://pep8.org\n\nFor pull requests the same coding styles should be used.\n\nLicense\n-------\n\n- Commercial license\n\nIf you want to use ReportBro to develop commercial applications and projects, the Commercial license is the appropriate license. With this license, your source code is kept proprietary. Purchase a ReportBro Commercial license at https://www.reportbro.com/license/index.\n\n- Open-source license\n\nIf you are creating an open-source application under a license compatible with the `GNU AGPL license v3 <https://www.gnu.org/licenses/agpl-3.0.html>`_, you may use ReportBro under the terms of the AGPLv3.\n\nRead more about ReportBro's license options at https://www.reportbro.com/license/index.\n",
    'author': 'jobsta',
    'author_email': 'alex@reportbro.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.reportbro.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
