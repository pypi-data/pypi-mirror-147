# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['templatest']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'templatest',
    'version': '0.1.0',
    'description': 'Templates for testing with strings',
    'long_description': 'templatest\n==========\n.. image:: https://github.com/jshwi/templatest/workflows/ci/badge.svg\n    :target: https://github.com/jshwi/templatest/workflows/ci/badge.svg\n    :alt: ci\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/pypi/v/templatest\n    :target: https://img.shields.io/pypi/v/templatest\n    :alt: pypi\n.. image:: https://codecov.io/gh/jshwi/templatest/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/templatest\n    :alt: codecov.io\n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n    :target: https://lbesson.mit-license.org/\n    :alt: mit\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nTemplates for testing with strings\n----------------------------------\n\nDesigned with ``pytest.mark.parametrize`` in mind\n\nWork with subclasses inheriting from the ``templatest.BaseTemplate`` abstract base class\n\nTo use the inherited class decorate it with ``templatest.templates.register`` and ensure the module it is in is\nimported at runtime\n\nAs there will be no need to import anything from this module related to this package, this can be ensured by\nplacing it in tests/__init__.py\n\n.. code-block:: python\n\n    >>> # tests/__init__.py\n    >>>\n    >>> import templatest\n    >>>\n    >>> @templatest.templates.register\n    ... class _ExampleTemplate(templatest.BaseTemplate):\n    ...     @property\n    ...     def template(self) -> str:\n    ...         return "Hello, world!"\n    ...\n    ...     @property\n    ...     def expected(self) -> str:\n    ...         return "Hello, world!"\n    >>>\n    >>> templatest.templates.registered.getids()\n    (\'example-template\',)\n    >>>\n    >>> templatest.templates.registered.filtergroup(\'err\').getids()\n    (\'example-template\',)\n    >>>\n    >>> templatest.templates.registered.getgroup(\'err\').getids()\n    ()\n\n\nThe class\'s properties will then be available in the ``templatest.templates.registered`` object as an instance of\n``templatest.Template`` named tuple\n\n.. code-block:: python\n\n    template = templates.templates[0]\n    name = template.name\n    template = template.template\n    expected = template.expected\n\n.. code-block:: python\n\n    template = templates.templates[0]\n    name, template, expected = template\n\nOrganise tests by prefixing subclasses for common tests\n\n.. code-block:: python\n\n    >>> # tests/__init__.py\n    >>>\n    >>> @templatest.templates.register\n    ... class _ErrExampleTemplate(templatest.BaseTemplate):\n    ...\n    ...     @property\n    ...     def template(self) -> str:\n    ...         return "Goodbye, world..."\n    ...\n    ...     @property\n    ...     def expected(self) -> str:\n    ...         return "Goodbye, world..."\n    >>>\n    >>> templatest.templates.registered.getids()\n    (\'example-template\', \'err-example-template\')\n    >>>\n    >>> templatest.templates.registered.filtergroup(\'err\').getids()\n    (\'example-template\',)\n    >>>\n    >>> templatest.templates.registered.getgroup(\'err\').getids()\n    (\'err-example-template\',)\n\nExample usage with a parametrized test\n**************************************\n\n.. code-block:: python\n\n    >>> # tests/_test.py\n    >>>\n    >>> import pytest\n    >>>\n    >>> from templatest.templates import registered as r\n    >>>\n    >>> @pytest.mark.parametrize("n,t,e", r, ids=r.getids())\n    ... def test_example_all(n: str, t: str, e: str) -> None: ...\n    >>>\n    >>> @pytest.mark.parametrize("n,t,e", r.filtergroup(\'err\'), ids=r.filtergroup(\'err\').getids())\n    ... def test_example_no_errs(n: str, t: str, e: str) -> None: ...\n    >>>\n    >>> @pytest.mark.parametrize("n,t,e", r.getgroup(\'err\'), ids=r.getgroup(\'err\').getids())\n    ... def test_example_errs(n: str, t: str, e: str) -> None:\n    ...     with pytest.raises(Exception) as err:\n    ...         raise Exception(e)\n    ...\n    ...     assert str(err.value) == e\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
