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
    'version': '0.0.1a3',
    'description': 'Build FastAPI applications easily',
    'long_description': '## Install\n\n#### Install using poetry\n\n```bash\npoetry install\n```\n\n#### Install using script\n\n```bash\npython ./install.py\n```\n\n#### Install manually\n\n- Create a virtual environment:\n\n```bash\npython -m venv .venv\n```\n\n- Update python package toolkit (within the virtual environment):\n\n```bash\npython -m pip install -U pip setuptools wheel build\n```\n\n- Install the project in editable mode (within the virtual environment) with all extras:\n\n```bash\npython -m pip install -e .[dev,oidc,telemetry]\n```\n\n## Run the app\n\n- Either use the `wire` module:\n\n```bash\npython -m wire examples/app.yaml -c examples/config.json\n```\n\n- The command line interface:\n\n```bash\nwire --help\n```\n\n- Or use `uvicorn` to start the application:\n\n```bash\nCONFIG_FILEPATH=examples/config.json uvicorn --factory demo_app.spec:spec.create_app\n```\n\n> Note that server config won\'t be applied since uvicorn is started from command line and not within Python process in this case.\n\n- It\'s also possible to start the application with hot-reloading:\n\n```bash\nCONFIG_FILEPATH=examples/config.json uvicorn --factory demo_app.spec:spec.create_app --reload\n```\n\n## Configure the app\n\nApplication can be configured using environment variables or file, or options when using the CLI:\n\n![App Container](https://github.com/charbonnierg/nats-fastapi-issuer-demo/raw/next/docs/settings-to-container.png)\n\n> Note: Environment variables take precedence over variables declared in file. For example, assuming the above configuration is declared in a file named `config.json`, when running: `PORT=8000 CONFIG_FILE=./demo/config.json python -m demo_app`, application will listen on port `8000` and not `7777`.\n\n> Note: When using `uvicorn`, `HOST` and `PORT` are ignored and must be specified as command line arguments if required.\n\n## Design choices\n\nApplication is wrapped within a [`Container`](./src/quara-wiring/quara/wiring/core/container.py):\n\nAn [`Container`](./src/quara-wiring/quara/wiring/core/container.py) is created from:\n\n- _Some [**settings**](./src/quara-wiring/quara/wiring/core/settings.py)_: settings are defined as pydantic models. When they are not provided directly, values are parsed from environment or file.\n\n- _Some **hooks**_: hooks are async context managers which can inject arbitrary resources into application state. In this application, a hook is used to add an `Issuer` instance to the application state. See documentation on [Asynchronous Context Managers](https://docs.python.org/3/reference/datamodel.html#asynchronous-context-managers) and [@contextlib.asynccontextmanager](https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager) to easily create context managers from coroutine functions. You can see how it\'s used in [the hook used by the example application](https://github.com/charbonnierg/nats-fastapi-issuer-demo/blob/declarative/src/demo-app/demo_app/hooks/issuer.py).\n\n- _Some **providers**_: providers are functions which must accept a single argument, an application container, and can add additional features to the application. They are executed before the FastAPI application is initialized, unlike hooks, which are started after application is initiliazed, but before it is started. In the repo example, providers are used for example to optionally enable prometheus metrics and opentelemetry traces. The [CORS Provider](https://github.com/charbonnierg/nats-fastapi-issuer-demo/blob/declarative/src/quara-wiring/quara/wiring/providers/cors.py) is surely the most simple provider.\n\n- _Some [**routers**](https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter)_: routers are objects holding a bunch of API endpoints together. Those endpoints can share a prefix and some OpenAPI metadata.\n\nIn order to faciliate creation and declaration of application containers, the [`AppSpec`](./src/quara-wiring/quara/wiring/core/spec.py) class can be used as a container factory.\n\n> See usage in [`src/demo-app/demo_app/spec.py`](./src/demo-app/demo_app/spec.py)\n\n## Objectives\n\n- [x] **Distributable**: Application can be distributed as a python package.\n\n- [x] **Configurable**: The database used in the application must be configurable using either a file or an environment variable.\n\n- [x] **Configurable**: The server configuration (host, port, debug mode) must be configurable using either a file or an environment variable.\n\n- [x] **User friendly**: A command line script should provide a quick and simply way to configure and start the application.\n\n- [x] **Debug friendly**: Application settings should be exposed on a `/debug/settings` endpoint when application is started on debug mode.\n\n- [x] **Observable**: Adding metrics or tracing capabilities to the application should be straighforward and transparent.\n\n- [x] **Explicit**: Router endpoints must not use global variables but instead explicitely declare dependencies to be injected (such as database client or settings). This enables [efficient sharing of resources and facilitate eventual refactoring in the future](https://github.com/charbonnierg/nats-fastapi-issuer-demo/blob/9beb7e4f1d37d616de10ab701cbde7fe1115f2a2/src/demo-app/demo_app/routes/demo.py#L34).\n\n- [x] **Conposable**: Including additional routers or features in the future should require minimal work.\n\n  - Arbitrary hooks with access to application container within their scope can be registered. Those hooks are guaranteed to be started and stopped in order, and even if an exception is encountered during a hook exit, all remaining hooks will be closed before an exception is raised. It minimize risk of resource leak within the application. Hooks can be seen as contexts just like in the illustration below:\n\n  - Arbitrary tasks can be started along the application. Tasks are similar to hooks, and are defined using a coroutine function which takes the application container as argument and can stay alive as long as application\n  is alive. Unlike hooks, tasks have a status and can be:\n    - stopped\n    - started\n    - restarted\n  It\'s also possible to fetch the task status to create healthcheck handlers for example.\n\n  - Arbitrary providers with access to application container within their scope can be registered. Those providers are executed once, before the application is created. They can be used to add optional features such as tracing or metrics.\n  \n  - Objects provided by hooks or providers can be accessed through dependency injection in the API endpoints. Check [this example](https://github.com/charbonnierg/nats-fastapi-issuer-demo/blob/9beb7e4f1d37d616de10ab701cbde7fe1115f2a2/src/demo-app/demo_app/routes/demo.py#L34) to see dependency injection in practice.\n\nBelow is an illustration of an hypothetic application lifecycle:\n\n![App Lifecycle](https://github.com/charbonnierg/nats-fastapi-issuer-demo/raw/next/docs/container-lifecycle.png)\n\n## Declarative application\n\nIt\'s possible to declare application using YAML, JSON or INI files. An example application could be:\n\n```yaml\n---\n# Application metadata\nmeta:\n  name: demo_app\n  title: Demo App\n  description: A declarative FastAPI application 🎉\n  package: wire\n\n# Custom settings model\nsettings: demo_app.settings.AppSettings\n\n# Declare providers\n# A few providers are available to use directly\n# It\'s quite easy to add new providers\nproviders:\n  - wire.providers.structured_logging_provider\n  - wire.providers.prometheus_metrics_provider\n  - wire.providers.openid_connect_provider\n  - wire.providers.openelemetry_traces_provider\n  - wire.providers.cors_provider\n  - wire.providers.debug_provider\n# It\'s possible to add routers\nrouters:\n  - demo_app.routes.issuer_router\n  - demo_app.routes.nats_router\n  - demo_app.routes.demo_router\n# Or hooks\nhooks:\n  - demo_app.hooks.issuer_hook\n# Or tasks (not used in this example)\ntasks: []\n# # It\'s also possible to declare default config file\n# config_file: ~/.quara.config.json\n```\n\n## `AppSpec` container factory\n\nIt\'s also possible to define applications using a python object instead of a text file.\n\nThe `AppSpec` class can be used to create application containers according to an application specification.\n\n### Adding new hooks\n\nUpdate the file `demo_app/spec.py` to add a new hook to your application.\n\nThe `hooks` argument of the `AppSpec` constructor can be used to specify a list of hooks used by the application.\n\nEach hook must implement the `AsyncContextManager` protocol or be functions which might return `None` or an `AsyncContextManager` instance.\n\nObject yielded by the hook is available in API endpoints using dependency injection.\n\n> Note: It\'s possible to access any container attribute within hooks.\n\n### Adding new routers\n\nUpdate the file `demo_app/spec.py` to register a new router within your application.\n\nThe `routers` argument of the `AppSpec` constructor can be used to specify a list of routers used by the application.\n\nBoth `fastapi.APIRouter` and functions which might return `None` or an `fastapi.APIRouter` instance are accepted as list items.\n\n\n## Adding providers to the application\n\nProviders are functions which can modify the FastAPI application before it is started.\n\nThey must accept an application container instance as unique argument, and can return a list of objects or None.\nWhen None is returned, it is assumed that provider is disabled.\nWhen a list is returned, each object present in the list will be available in API endpoints using dependency injection.\n\nExample providers are located in `src/quara-wiring/quara/wiring/providers/` directory and are registered in `demo_app/spec.py`.\n\n## Building the application\n\nRun the following command to build the application:\n\n```bash\npython -m build .\n```\n\n### Advantages of the `src/` layout\n\nThis project uses a `src/` layout. It means that all source code can be found under `src/` directory. It might appear overkill at first, but it brings several benefits:\n\n- Without src you get messy editable installs ("pip install -e"). Having no separation (no src dir) will force setuptools to put your project\'s root on `sys.path` - with all the junk in it (e.g.: setup.py and other test or configuration scripts will unwittingly become importable).\n\n- You get import parity. The current directory is implicitly included in `sys.path`; but not so when installing & importing from site-packages.\n\n- You will be forced to test the installed code (e.g.: by installing in a virtualenv and performing an editable install). This will ensure that the deployed code works (it\'s packaged correctly) - otherwise your tests will fail.\n\n- Simpler packaging code and manifest. It makes manifests very simple to write (e.g.: root directory of project is never considered by setuptools or other packaging toolswhen bundling files into package). Also, zero fuss for large libraries that have multiple packages. Clear separation of code being packaged and code doing the packaging.\n\n### Telemetry\n\n- [`BatchSpanProcessor`](https://opentelemetry-python.readthedocs.io/en/latest/sdk/trace.export.html#opentelemetry.sdk.trace.export.BatchSpanProcessor) is configurable with the following environment variables which correspond to constructor parameters:\n\n- [OTEL_BSP_SCHEDULE_DELAY](https://opentelemetry-python.readthedocs.io/en/latest/sdk/environment_variables.html#envvar-OTEL_BSP_SCHEDULE_DELAY)\n- [OTEL_BSP_MAX_QUEUE_SIZE](https://opentelemetry-python.readthedocs.io/en/latest/sdk/environment_variables.html#envvar-OTEL_BSP_MAX_QUEUE_SIZE)\n- [OTEL_BSP_MAX_EXPORT_BATCH_SIZE](https://opentelemetry-python.readthedocs.io/en/latest/sdk/environment_variables.html#envvar-OTEL_BSP_MAX_EXPORT_BATCH_SIZE)\n- [OTEL_BSP_EXPORT_TIMEOUT](https://opentelemetry-python.readthedocs.io/en/latest/sdk/environment_variables.html#envvar-OTEL_BSP_EXPORT_TIMEOUT)\n',
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
