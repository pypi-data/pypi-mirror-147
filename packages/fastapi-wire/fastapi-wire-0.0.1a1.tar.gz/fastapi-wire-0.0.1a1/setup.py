# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/demo-app',
 'wire': 'src/fastapi-wire/wire',
 'wire.cli': 'src/fastapi-wire/wire/cli',
 'wire.core': 'src/fastapi-wire/wire/core',
 'wire.providers': 'src/fastapi-wire/wire/providers',
 'wire.providers.debug': 'src/fastapi-wire/wire/providers/debug',
 'wire.providers.logger': 'src/fastapi-wire/wire/providers/logger',
 'wire.providers.logger.structlog': 'src/fastapi-wire/wire/providers/logger/structlog',
 'wire.providers.metrics': 'src/fastapi-wire/wire/providers/metrics',
 'wire.providers.oidc': 'src/fastapi-wire/wire/providers/oidc',
 'wire.providers.tracing': 'src/fastapi-wire/wire/providers/tracing'}

packages = \
['demo_app',
 'demo_app.hooks',
 'demo_app.lib',
 'demo_app.routes',
 'wire',
 'wire.cli',
 'wire.core',
 'wire.providers',
 'wire.providers.debug',
 'wire.providers.logger',
 'wire.providers.logger.structlog',
 'wire.providers.metrics',
 'wire.providers.oidc',
 'wire.providers.tracing']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'fastapi>=0.75.1,<0.76.0',
 'nats-py>=2.1.0,<3.0.0',
 'nkeys>=0.1.0,<0.2.0',
 'setuptools',
 'structlog>=21.5.0,<22.0.0',
 'uvicorn>=0.17.6,<0.18.0']

extras_require = \
{'dev': ['flake8>=4.0.1,<5.0.0',
         'black>=22.3.0,<23.0.0',
         'isort>=5.10.1,<6.0.0',
         'mypy>=0.942,<0.943',
         'types-setuptools>=57.4.12,<58.0.0',
         'types-PyYAML>=6.0.7,<7.0.0'],
 'oidc': ['cryptography>=36.0.2,<37.0.0',
          'httpx>=0.22.0,<0.23.0',
          'PyJWT>=2.3.0,<3.0.0'],
 'telemetry': ['prometheus-fastapi-instrumentator>=5.7.1,<6.0.0',
               'opentelemetry-instrumentation-fastapi>=0.29-beta.0,<0.29',
               'opentelemetry-sdk>=1.10.0,<2.0.0']}

entry_points = \
{'console_scripts': ['wire = wire.cli:run']}

setup_kwargs = {
    'name': 'fastapi-wire',
    'version': '0.0.1a1',
    'description': 'Build FastAPI applications easily',
    'long_description': 'None',
    'author': 'Guillaume Charbonnier',
    'author_email': 'gu.charbon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
