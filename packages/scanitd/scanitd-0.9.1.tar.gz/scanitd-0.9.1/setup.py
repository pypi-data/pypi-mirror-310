# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scanitd',
 'scanitd.base',
 'scanitd.cli',
 'scanitd.inference',
 'scanitd.writer']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.7.0,<0.8.0',
 'numpy>=2.0.0,<3.0.0',
 'psutil>=5.9.5,<6.0.0',
 'pyfaidx>=0.7.2,<0.8.0',
 'pysam>=0.22.0,<0.23.0',
 'rich>=13.7.0,<14.0.0',
 'ssw-py>=1.0.1,<2.0.0',
 'typer>=0.12.5,<0.13.0']

entry_points = \
{'console_scripts': ['scanitd = scanitd.cli.cli:app']}

setup_kwargs = {
    'name': 'scanitd',
    'version': '0.9.1',
    'description': 'ScanITD',
    'long_description': '# ScanITD\n\n[![PyPI version](https://img.shields.io/pypi/v/scanitd.svg)](https://pypi.python.org/pypi/scanitd)\n[![PyPI - Wheel](https://img.shields.io/pypi/wheel/scanitd)](https://pypi.org/project/scanitd/#files)\n[![license](https://img.shields.io/pypi/l/scanitd.svg)](https://github.com/ylab-hi/ScanITD/blob/main/LICENSE)\n\n\n# 📦 Installation\n\nScanITD can be installed using pip, the Python package installer.\nFollow these steps to install:\n\n1. Ensure you have Python 3.10 or later installed on your system.\n\n2. Create a virtual environment (recommended):\n\n   ```bash\n   python -m venv scanitd_env\n   source scanitd_env/bin/activate  # On Windows use `scanitd_env\\Scripts\\activate`\n   ```\n\n3. Install ScanITD:\n\n   ```bash\n   pip install scanitd\n   ```\n\n4. Verify the installation:\n\n   ```bash\n   scanitd --help\n   ```\n\n# 🛠️ Usage\n\n Usage: scanitd [OPTIONS]\n\n ScanITD: Detecting internal tandem duplication with robust variant allele frequency estimation\n## Required Arguments\n* `--input`, `-i` PATH\n    - Aligned BAM file\n    - Required\n\n* `--ref`, `-r` PATH\n    - Reference genome in FASTA format (with fai index)\n    - Required\n\n* `--output`, `-o` TEXT\n    - Output VCF file\n    - Required\n\n## Optional Arguments\n* `--mapq`, `-m` INTEGER\n    - Minimum MAPQ in BAM for calling ITD\n    - Default: 15\n\n* `--ao`, `-c` INTEGER\n    - Minimum observation count for ITD\n    - Default: 4\n\n* `--depth`, `-d` INTEGER\n    - Minimum depth to call ITD\n    - Default: 10\n\n* `--vaf`, `-f` FLOAT\n    - Minimum variant allele frequency\n    - Default: 0.1\n\n* `--length` INTEGER\n    - Minimum ITD length to report\n    - Default: 10\n\n* `--aln-mismatches`, `-n` INTEGER\n    - Maximum allowed mismatches for pairwise local alignment\n    - Default: 1\n\n* `--ins-mismatches` INTEGER\n    - Maximum allowed mismatches for insertion-inferred duplication\n    - Default: 2\n\n* `--target`, `-t` TEXT\n    - Limit analysis to targets listed in the BED-format file or a samtools region string\n\n* `--log-level`, `-l` [info|warning|error|debug|trace]\n    - Set the logging level\n    - Default: info\n\n* `--version`, `-v`\n    - Show version and exit\n\n# 📚 Citation\n\nWang TY. and Yang R. [ScanITD: Detecting internal tandem duplication with robust variant allele frequency estimation](https://doi.org/10.1093/gigascience/giaa089 "ScanITD: Detecting internal tandem duplication with robust variant allele frequency estimation").\n',
    'author': 'Ting-You Wang',
    'author_email': 'tywang@northwestern.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ylab-hi/ScanITD',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
