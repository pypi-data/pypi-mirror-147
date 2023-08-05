# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xkcd_cli']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11,<5.0', 'requests>=2.27,<3.0', 'typer>=0.4,<0.5']

entry_points = \
{'console_scripts': ['xkcd = xkcd_cli.xkcd:main']}

setup_kwargs = {
    'name': 'dcs-xkcd-cli',
    'version': '1.0.0',
    'description': 'Get your daily dose of xkcd directly from the terminal! 🤩',
    'long_description': '# xkcd cli tool\n\nGet your daily dose of [xkcd] directly from the terminal! 🤩\n\n[xkcd] is a webcomic created by [Randall Munroe][munroe]. \nIt is a comic of Language, Math, Romance and Sarcasm and a [couple of other categories][explain-xkcd-categories].\n\nIf [kitty] is used as the terminal, the xkcd comic will be rendered directly in the terminal, otherwise the default viewer for PNG images is used.\nThis tool requires [fzf] to be installed on the machine to filter available comics by their title. \n\n## Installation\n\n### With pip\n\nInstall this package directly from the [Python Package Index (PyPI)][pypi-repo].\nThe CLI tool requires Python >= 3.8 to be installed.\n\n```console\n$ pip install dcs-xkcd-cli\n```\n\nThis will install a CLI tool named `xkcd` which can be used as described below.\n\n### With pipx\n\nInstallation with [pipx] is similar to the pip variant above, but uses `pipx` instead of `pip`.\n\n```console\n$ pipx install dcs-xkcd-cli\n```\n\nNote that with pipx, this package can be tried out without the need to install it permanently.\n\n```console\n$ pipx run dcs-xkcd-cli <args>\n```\n\n\n## Usage\n\n### Search by title\n\n```console\n$ xkcd show\n```\n\nThis functionality requires [fzf] to be installed.\n\n### Show latest xkcd comic\n\n```console\n$ xkcd show --latest\n```\n\n### Show random xkcd comic\n\n```console\n$ xkcd show --random\n```\n\n### Show xkcd comic by its ID\n\n```console\n$ xkcd show --comic-id 207\n```\n\n### Enforce render optimizations for kitty terminal\n\n```console\n$ xkcd show --use-kitty\n```\n\nUse this command if the auto-detection of the kitty terminal does not work as expected.\nKitty is auto-detected by inspecting if the `$TERM` variable includes the term `kitty`.\n\nBy default the image is upscaled to the terminal width.\nUse the `--no-kitty-scale-up` flag to disable this feature if needed.\n\n### Disable or update cache\n\nUnder the hood this tool uses a cache which is updated once per day transparently.\nThe cache is used to remember the list of xkcd comics from the [archive].\n\nTo disable the cache, use the following command\n\n```console\n$ xkcd show --no-cache\n```\n\nTo update the cache manually, use the following command\n```console\n$ xkcd update-cache\n```\n\n\n[fzf]: https://github.com/junegunn/fzf\n[kitty]: https://sw.kovidgoyal.net/kitty/\n[archive]: https://xkcd.com/archive/\n[xkcd]: https://xkcd.com\n[munroe]: https://en.wikipedia.org/wiki/Randall_Munroe\n[explain-xkcd-categories]: https://www.explainxkcd.com/wiki/index.php/Category:Comics_by_topic\n[pypi-repo]: https://pypi.org/project/dcs-xkcd-cli/\n[pipx]: https://pypa.github.io/pipx/\n',
    'author': 'dotcs',
    'author_email': 'repositories@dotcs.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dotcs/xkcd-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
