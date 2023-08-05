# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['info',
 'info.gianlucacosta.eos.core',
 'info.gianlucacosta.eos.core.db',
 'info.gianlucacosta.eos.core.db.sqlite',
 'info.gianlucacosta.eos.core.functional',
 'info.gianlucacosta.eos.core.io',
 'info.gianlucacosta.eos.core.io.files',
 'info.gianlucacosta.eos.core.io.serializing',
 'info.gianlucacosta.eos.core.logic',
 'info.gianlucacosta.eos.core.multiprocessing',
 'info.gianlucacosta.eos.core.multiprocessing.pool',
 'info.gianlucacosta.eos.core.reflection',
 'info.gianlucacosta.eos.core.threading',
 'info.gianlucacosta.eos.core.threading.queues']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'info.gianlucacosta.eos.core',
    'version': '1.0.0',
    'description': 'Type-checked, dependency-free utility library for modern Python',
    'long_description': "# Eos-core\n\n_Type-checked, dependency-free utility library for modern Python_\n\n## Introduction\n\nMy voyage through the vast and fascinating universe of **Python** started back in 2004 - when _Python 2.3_ was still the latest, exciting release... 😊\n\nSince then, both the language and its ecosystem have evolved a lot: in particular, I feel that _type hints_ make Python even more robust, without sacrificing its charming syntax - just like another language I'm fond of: **TypeScript**.\n\nConsequently, the **Eos** library is designed to provide a set of shared utilities and patterns emerged during the creation of my open source projects with modern, type-checked Python - and this **core** package only builds upon the standard library, with no additional runtime dependencies.\n\nFor further details, please refer to the sections below, to the documentation within each module, and even to the tests - whose coverage is more than 97%! ^\\_\\_^\n\n## Installation\n\nTo install **eos.core**, just run:\n\n> pip install info.gianlucacosta.eos.core\n\nor, if you prefer using Poetry:\n\n> poetry add info.gianlucacosta.eos.core\n\nThen, you'll be able to access the **info.gianlucacosta.eos.core** package and its subpackages.\n\n## Highlights\n\n**eos.core** provides a wide variety of patterns - including:\n\n- _higher-order functional abstractions_, such as functions returning **adaptable queue writers** and **readers** - whose timeouts vary according to the queue state\n\n- a disposable **TemporaryPath** - and a **Uuid4TemporaryPath** string subclass that perform advanced cleanup, no matter whether you create a file or a whole directory tree upon it\n\n- a **BufferedDbSerializer** - using advanced but simple decorators to serialize objects of different types via dedicated SQL statements, but actually writing to DB only when the internal buffer is full\n\n- an **InThreadPool** class having the same interface as Python's **Pool** - but running within the very same thread: definitely handful when debugging and testing\n\n- a **CancelableThread** and the related **CancelableThreadHandle** - enabling the client to send a cancelation request\n\n- an **Atomic** class, to read and update arbitrary values atomically\n\n- a **functional** module, with expressive type aliases for functions - with ideas borrowed from other languages such as C#, Java and Rust\n\n...and more! ^\\_\\_^ It's definitely not easy to mention everything in a README file, so please feel free to browse the modules and explore how they are used in the tests!\n",
    'author': 'Gianluca Costa',
    'author_email': 'gianluca@gianlucacosta.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giancosta86/Eos-core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
