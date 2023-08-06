# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ezfuse']

package_data = \
{'': ['*']}

install_requires = \
['colorama']

entry_points = \
{'console_scripts': ['ezfuse = ezfuse.cli:run']}

setup_kwargs = {
    'name': 'ezfuse',
    'version': '1.1.0',
    'description': 'Quickly mount fuse filesystems in temporary directories',
    'long_description': '![Github](https://img.shields.io/github/tag/essembeh/ezfuse.svg)\n![PyPi](https://img.shields.io/pypi/v/ezfuse.svg)\n![Python](https://img.shields.io/pypi/pyversions/ezfuse.svg)\n\n# EzFuse\n\nEzFuse is a tool handle temporary mountpoints for _Fuse_ filesystems.\n\nFeatures:\n\n- automatically create and remove a directory to mount the filesystem\n- interactive shell dialog to execute actions\n- you can mount, umount the mountpoint\n- you can open a shell in the mounted directory\n- you can open your _file browser_ in the mounted directory\n- you can exit the _EzFuse_ and keep the mountpoint mounted\n\n![demo.gif](images/demo.gif)\n\n# Install\n\nInstall from [Pypi](https://pypi.org/project/ezfuse/)\n\n```sh\n$ pip3 install ezfuse\n```\n\nOr install latest version using pip and poetry\n\n```sh\n$ pip3 install poetry\n$ pip3 install git+https://github.com/essembeh/ezfuse\n```\n\nOr setup a development environment\n\n```sh\n$ pip3 install poetry\n$ git clone https://github.com/essembeh/ezfuse\n$ cd ezfuse\n$ poetry install\n$ poetry shell\n(.venv) $ ezfuse --version\n```\n\n# Usage\n\nTo mount a remote folder using `sshfs` ensure that `sshfs` is installed on your system before.\n\nWhile the temporary directory is created, _EzFuse_ is interactive and you are prompted for an action:\n\n```sh\n$ ezfuse --type sshfs MYREMOTEHOST:/some/path/here\n[info] Using mountpoint ezmount-sshfs-9dy6yb34\n[exec] sshfs MYREMOTEHOST:/some/path/here ezmount-sshfs-9dy6yb34\n\nx: exit\nq: umount and exit\no: xdg-open\ns: shell\nm: mount\nu: umount\n[x/q/o/s/m/u]\n\n```\n\n![dialog.png](images/dialog.png)\n\nWhen exiting _EzFuse_ using `q`, the filesystem will automatically be unmounted and the temporary directory removed.\n\n> Note: All executed commands are displayed with `[exec]` prefix.\n\n# Advanced usage: use symlinks\n\nBy default, you have to pass the `-t, --type` to _EzFuse_ to specify which _Fuse_ filesystem to use, but you can also create symplinks to avoid that.\n\nFor example, to use `sshfs`, create a symlink named `ezsshfs` pointing to `ezfuse`\n\n```sh\n$ mkdir -p ~/.local/bin/\n$ ln -s $(which ezfuse) ~/.local/bin/ezsshfs\n# Now the two commands are equivalent\n$ ezsshfs MYREMOTEHOST:/some/path/here\n$ ezfuse -t sshfs MYREMOTEHOST:/some/path/here\n```\n\nYou can do it for every _Fuse_ filesystem you may use, like `borgfs`for example:\n\n```sh\n$ ln -s $(which ezfuse) ~/.local/bin/ezborgfs\n$ ezborgfs /path/to/my/backup.borg/\n```\n',
    'author': 'Sébastien MB',
    'author_email': 'seb@essembeh.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/essembeh/ezfuse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
