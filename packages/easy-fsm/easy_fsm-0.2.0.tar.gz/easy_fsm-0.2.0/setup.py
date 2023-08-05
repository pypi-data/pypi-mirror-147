# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easy_fsm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'easy-fsm',
    'version': '0.2.0',
    'description': 'Easy to implement Finite State Machines',
    'long_description': 'easy_fsm\n========\n\nEasy to implement Finite State Machines.\n\n.. image:: https://img.shields.io/pypi/l/easy_fsm.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/easy_fsm/\n   :alt: License\n\n.. image:: https://img.shields.io/pypi/status/easy_fsm.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/easy_fsm/\n   :alt: Development Status\n\n.. image:: https://img.shields.io/pypi/v/easy_fsm.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/easy_fsm/\n   :alt: Latest release\n\n.. image:: https://img.shields.io/pypi/pyversions/easy_fsm.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/easy_fsm/\n   :alt: Supported Python versions\n\n.. image:: https://img.shields.io/pypi/implementation/easy_fsm.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/easy_fsm/\n   :alt: Supported Python implementations\n\n.. image:: https://img.shields.io/pypi/wheel/easy_fsm.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/easy_fsm\n   :alt: Download format\n\n.. image:: https://img.shields.io/github/workflow/status/linkdd/easy_fsm/run-test-suite?style=flat-square\n   :target: https://github.com/linkdd/easy_fsm/actions/workflows/test-suite.yml\n   :alt: Build Status\n\n.. image:: https://img.shields.io/pypi/dm/easy_fsm.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/easy_fsm/\n   :alt: Downloads\n\nIntroduction\n------------\n\n**easy_fsm** provides a very simple API to build finite state machines.\n\nThe state machine holds a context that is passed to the different states.\n\nEach state returns either the next state to execute or `None` if the execution\nis done.\n\nThis allows you to implement business logic in small, well separated, chunks of\ncode.\n\nExample\n-------\n\n.. code-block:: python\n\n   from typing import Optional\n   from easy_fsm import StateMachine, State\n   from dataclasses import dataclass, field\n\n\n   @dataclass\n   class Stats:\n       altitude: int = 0\n       fly_time: int = 0\n       suite: list[int] = field(default_factory=list)\n\n\n   class ComputeSyracuse(State[Stats]):\n       def __init__(self, n: int):\n           self.n = n\n\n       def run(self, context: Stats) -> Optional[State[Stats]]:\n           context.altitude = max(context.altitude, self.n)\n           context.fly_time += 1\n           context.suite.append(self.n)\n\n           if self.n == 1:\n               return None\n\n           elif self.n % 2 == 0:\n               return ComputeSyracuse(self.n // 2)\n\n           else:\n               return ComputeSyracuse(3 * self.n + 1)\n\n\n   class Syracuse(StateMachine[Stats]):\n       def __init__(self):\n           super().__init__(Stats())\n\n       def compute(self, n: int) -> None:\n           self.run_from(ComputeSyracuse(n))\n\n\n   def test_fsm():\n       fsm = Syracuse()\n       fsm.compute(5)\n\n       assert fsm.context.altitude == 16\n       assert fsm.context.fly_time == 6\n       assert fsm.context.suite == [5, 16, 8, 4, 2, 1]\n\n\nLicense\n-------\n\nThis project is released under the terms of the `MIT License`_.\n\n.. _MIT License: https://github.com/linkdd/easy_fsm/blob/main/LICENSE.txt\n',
    'author': 'David Delassus',
    'author_email': 'david.jose.delassus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/linkdd/easy_fsm',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
