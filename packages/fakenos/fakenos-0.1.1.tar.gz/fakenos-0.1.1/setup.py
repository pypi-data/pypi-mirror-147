# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fakenos',
 'fakenos.core',
 'fakenos.plugins',
 'fakenos.plugins.nos',
 'fakenos.plugins.servers',
 'fakenos.plugins.shell',
 'fakenos.plugins.tapes',
 'fakenos.plugins.utils']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=2.10.3,<3.0.0', 'pydantic>=1.9.0,<2.0.0', 'pyyaml>=6.0.0,<7.0.0']

entry_points = \
{'console_scripts': ['fakenos = fakenos.plugins.utils.cli:run_cli']}

setup_kwargs = {
    'name': 'fakenos',
    'version': '0.1.1',
    'description': 'Fake Network Operating System',
    'long_description': '[![Downloads][pepy-downloads-badge]][pepy-downloads-link]\n[![PyPI][pypi-latest-release-badge]][pypi-latest-release-link]\n[![PyPI versions][pypi-pyversion-badge]][pypi-pyversion-link]\n[![GitHub Discussion][github-discussions-badge]][github-discussions-link]\n[![Code style: black][black-badge]][black-link]\n[![Tests][github-tests-badge]][github-tests-link]\n\n# Fake Network Operating Systems - FakeNOS\n\n> "Reality is merely an illusion, albeit a very persistent one."\n>\n> ~ Albert Einstein\n\nFakeNOS created to simulate Network Operating Systems interactions.\n\n[Documentation](https://dmulyalin.github.io/fakenos/)\n\n## Why?\n\nCrucial aspect of writing applications or scripts for Network Automation is \ntesting, often testing done using physical or virtual instances of network\nappliances running certain version of Network Operating System (NOS). That\napproach, while gives best integration results, in many cases carries a lot\nof overhead to setup, run and tear down as well as putting significant burden\non compute and storage resource utilization.\n\nOther approach is to mock underlying libraries methods to fool applications\nunder testing into believing that it is getting output from real devices. That\napproach works very well for unit testing, but fails to simulate such aspects\nas connection establishment and handling.\n\nFakeNOS positions itself somewhere in the middle between full integration testing\nand testing that mocks device interactions. FakeNOS allows to create NOS plugins\nto produce pre-defined output to test applications behavior while running servers \nto establish connections with.\n\n## What?\n\nFakeNOS can:\n\n- Run thousands of servers to stress test applications\n- Simulate Network Operating Systems Command Line Interface (CLI) interactions\n- Provide high-level API to create custom NOS plugins\n- Run in docker container to simplify integration with your infrastructure\n- Make use of FakeNOS CLI tool for quick run and prototype simulations\n- Works on Windows, MAC and Linux under major Python version\n\n## How?\n\nSend input and get the output - this is how we interact with many \nNetwork Operating Systems, FakeNOS allows to pre-define the output \nto sent in response to certain input commands, making it ideal for\nisolated feature testing.\n\nFakeNOS is a micro-kernel framework that can be extended using plugins. \nThe core is kept small and optimized while most of the functionality \noffloaded to plugins.\n\nFakeNOS has these pluggable systems:\n\n- Server Plugins - plugins responsible for running various servers to connect with\n- Shell Plugins - plugins to simulate command line interface shell\n- NOS plugins - plugins to simulate Network Operating System commands\n\n## What not?\n\nFakeNOS is a simulator, it does not emulate any of Network Control, Data \nor Management planes, it merely takes the commands as input and responds\nwith predefined output.\n\n## FakeNOS inspired by and borrowed from\n\n- [sshim](https://pythonhosted.org/sshim/) - library for testing and debugging SSH automation clients\n- [PythonSSHServerTutorial](https://github.com/ramonmeza/PythonSSHServerTutorial) - tutorial on creating paramiko based SSH server\n- [fake-switches](https://github.com/internap/fake-switches) - pluggable switch/router command-line simulator\n- [ncs-netsim](https://developer.cisco.com/docs/nso/guides/#!the-network-simulator) - tool to simulate a network of devices\n- [cisshgo](https://github.com/tbotnz/cisshgo) - concurrent SSH server to emulate network equipment for testing purposes\n- [scrapli-replay](https://pypi.org/project/scrapli-replay/) - tools to enable easy testing of SSH programs and to create semi-interactive SSH servers\n\n\n[github-discussions-link]:     https://github.com/dmulyalin/fakenos/discussions\n[github-discussions-badge]:    https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github\n[black-badge]:                 https://img.shields.io/badge/code%20style-black-000000.svg\n[black-link]:                  https://github.com/psf/black\n[pypi-pyversion-link]:         https://pypi.python.org/pypi/fakenos/\n[pypi-pyversion-badge]:        https://img.shields.io/pypi/pyversions/fakenos.svg\n[pepy-downloads-link]:         https://pepy.tech/project/fakenos\n[pepy-downloads-badge]:        https://pepy.tech/badge/fakenos\n[github-tests-badge]:          https://github.com/dmulyalin/fakenos/actions/workflows/main.yml/badge.svg\n[github-tests-link]:           https://github.com/dmulyalin/fakenos/actions\n[pypi-latest-release-badge]:   https://img.shields.io/pypi/v/fakenos.svg\n[pypi-latest-release-link]:    https://pypi.python.org/pypi/fakenos\n',
    'author': 'Denis Mulyalin',
    'author_email': 'd.mulyalin@gmail.com',
    'maintainer': 'Denis Mulyalin',
    'maintainer_email': 'd.mulyalin@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.5,<3.10',
}


setup(**setup_kwargs)
