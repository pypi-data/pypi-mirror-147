# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aurornis']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aurornis',
    'version': '1.3.0',
    'description': 'A command line program test helper',
    'long_description': '# Aurornis - A command line program test helper\n\n[![Coverage Status](https://coveralls.io/repos/github/Deuchnord/Aurornis/badge.svg?branch=main)](https://coveralls.io/github/Deuchnord/Aurornis?branch=main)\n\nAurornis is a small, yet powerful library designed to help testing command line programs.\nThe name is a reference to the [_aurornis xui_](https://en.wikipedia.org/wiki/Aurornis), a prehistoric bird that lived 10 millions ago.\n\n## Installation\n\nAurornis is available in PyPI, so all you need is to install it with PIP:\n\n```bash\npip install --user aurornis\n```\n\nIf you are using Pipenv or Poetry, it is recommended to install it as a development dependency:\n\n```bash\npipenv install --dev aurornis\npoetry add --dev aurornis\n```\n\n## Usage\n\nAurornis provides a package with only one function to run a command, that returns an object with the result of the command:\n\n```python\nimport aurornis\n\ncommand_result = aurornis.run(["ls", "-la", "/"])\n# <CommandResult command="ls -la /" return_code=0 stdout="total 68 ..." stderr="">\n```\n\nFor better security and reproducibility, the environment variables of your system are not reproduced.\n\nIf you need to specify environment variables before you run the command, add them to the `run` function:\n\n```python\nimport aurornis\n\ncommand_result = aurornis.run(["env"], environment={"HOME": "/home/deuchnord"})\n```\n\nBy default, the `LANG` environment variable (used for internationalization) is reset to `C` (default system language, commonly English). You can change it if you want another language of execution.\n\nOnce you get the result, all you need to do is to use your favorite unit test framework to check it returned what you expected it to return:\n\n```python\nimport aurornis\nimport unittest\n\nclass CommandTest(unittest.TestCase):\n    def test_ls_home(self):\n        command_result = aurornis.run(["ls", "-l", "$HOME"], environment={"HOME": "/home/deuchnord"})\n        # You can check quickly the command was successful:\n        self.assertTrue(command_result.is_successful())\n        # Or if you expected a more specific return value:\n        self.assertEqual(2, command_result.return_code) # ls returns 2 if the file does not exist\n        \n        # Then, check the text returned in standard output and standard error:\n        self.assertEqual("""total 6\ndrwxr-xr-x 1 deuchnord deuchnord 40 27 May 13:19 Desktop\ndrwxr-xr-x 1 deuchnord deuchnord 40 14 Oct 18:08 Documents\ndrwxr-xr-x 1 deuchnord deuchnord 40  1 Sep 16:52 Downloads\ndrwxr-xr-x 1 deuchnord deuchnord 40 29 Sep 09:11 Pictures\ndrwxr-xr-x 1 deuchnord deuchnord 40 11 Jun  2020 Music\ndrwxr-xr-x 1 deuchnord deuchnord 40 10 Nov 11:32 Videos""", command_result.stdout)\n        self.assertEqual("", command_result.stderr)\n```\n\nIf your command returns colors in your standard output or standard error, you can ask Aurornis to automatically remove them:\n\n```python\nimport aurornis\n\naurornis.run(["echo", "-e", r\'\\e[0;32mHello World!\\e[0m\'], remove_colors=True)\n```\n\nThis option also automatically sets [the standard `NO_COLOR` environment variable](https://no-color.org). If your application shows colors, you may want to handle this environment variable to facilitate their deactivation by end users.\n\n## FAQ/Troubleshooting\n\n### My tests fail in virtual environments\n\nIf you are using Aurornis in a virtual environment, you will need to add the path of its `bin` folder in the environment variable:\n\n```python\nimport aurornis\n\naurornis.run(["python", "my-script.py"], environment={"PATH": "path/to/the/venv/bin"})\n```\n\nNote: if you use Pipenv, you can get this path with the following command:\n\n```bash\necho "$(pipenv --venv)/bin"\n```\n',
    'author': 'Jérôme Deuchnord',
    'author_email': 'jerome@deuchnord.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Deuchnord/Aurornis',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
