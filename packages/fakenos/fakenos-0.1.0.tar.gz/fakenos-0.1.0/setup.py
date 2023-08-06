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
    'version': '0.1.0',
    'description': 'Fake Network Operating System',
    'long_description': '# Fake Network Operating Systems - FakeNOS\n\n> "Reality is merely an illusion, albeit a very persistent one."\n>\n> ~ Albert Einstein\n\nFakeNOS created to simulate Network Operating Systems interactions.\n\n[Documentation](https://dmulyalin.github.io/fakenos/)\n\n## FakeNOS inspired by and borrowed from\n\n- [sshim](https://pythonhosted.org/sshim/) - library for testing and debugging SSH automation clients\n- [PythonSSHServerTutorial](https://github.com/ramonmeza/PythonSSHServerTutorial) - tutorial on creating paramiko based SSH server\n- [fake-switches](https://github.com/internap/fake-switches) - pluggable switch/router command-line simulator\n- [ncs-netsim](https://developer.cisco.com/docs/nso/guides/#!the-network-simulator) - tool to simulate a network of devices\n- [cisshgo](https://github.com/tbotnz/cisshgo) - concurrent SSH server to emulate network equipment for testing purposes\n- [scrapli-replay](https://pypi.org/project/scrapli-replay/) - tools to enable easy testing of SSH programs and to create semi-interactive SSH servers\n',
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
