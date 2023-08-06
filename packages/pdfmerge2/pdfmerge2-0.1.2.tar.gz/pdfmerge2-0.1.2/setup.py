# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdfmerge2']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.27.7,<2.0.0']

entry_points = \
{'console_scripts': ['pdfmerge = pdfmerge2.app:run']}

setup_kwargs = {
    'name': 'pdfmerge2',
    'version': '0.1.2',
    'description': 'CLI app that merges PDF files',
    'long_description': '# General info\nIt is a simple CLI app that merges PDF files in given directory\n\n# Technologies\n* Python 3.10\n* PyPDF2 1.26.0\n\n# Install\n## Using pip\n```\npip install pdfmerge2\n```\n\n## Cloning repository for development\n1. Clone repository\n2. Install requirements\n   ```\n   pip install -r requirements.txt\n   ```\n   or\n   ```\n   poetry install\n   ```\n\n# Usage\n1. Pass only path to merge ALL pdf files in there\n   ```\n   pdfmerge2 /path/to/pdf/files\n   ```\n2. Pass path and file names to merge only them \n   ```\n   pdfmerge2 /path/to/pdf/files -f file1 file2\n   ```\n3. You can also pass output path\n   ```\n   pdfmerge2 /path/to/pdf/files -f file1 file2 -o /path/to/output\n   ```\n\n# Contact\nCreated by [@Gasper3](https://github.com/Gasper3) - feel free to contact me!\n',
    'author': 'Gasper3',
    'author_email': 'trzecik65@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Gasper3/pdf-merger',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
