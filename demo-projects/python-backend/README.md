Sample back-end app
===================

A sample back-end app used to illustrate testing and development techniques.

## Setup

Install these tools:
- [Docker](https://docs.docker.com/engine/install/)
- [poetry](https://python-poetry.org/docs/#installation)
- [precommit](https://pre-commit.com/#installation)

Configure `poetry` so it'll create a .venv folder in the project's directory:
```
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true
```

Run `make setup run`.

Now you have a development environment prepared, and you have the application running locally in Docker.

For additional development commands, install:
- [fd](https://github.com/sharkdp/fd?tab=readme-ov-file#installation)
- [entr](https://eradman.com/entrproject/)

## Development operations

The commands are in the Makefile. Please review it.

## Demonstrated techniques

### Technologies used

- FastAPI: HTTP backend
- SQLAlchemy: ORM
- PostgreSQL: database
- Ruff: code formatting and linting
- Mypy: static type checks

### Architecture

This is my flavor of clean architecture.
There are a lot of flavors of it, see
[tomato](https://github.com/sivaprasadreddy/tomato-architecture),
[hexagonal/"port and adapter"](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) architectures.

The code packages map to clean architecture contepts:
- `services`: the business logic, my name for usecases that conveys the internal service architecture
  - simple / point-to-point - regular method calls between services
  - (TODO) pub/sub (fan-out)- add events and listeners to service classes. They can be organizing with a Networkx graph (DAG).
    Each layer of the graph that's reachable from the current node can be taken automatically with networkx
    (TODO see my work with dependency resolution in Cloud Foundry in Intel (late) Trusted Analytic's Platform's Apployer
    (I named it - app deployer - well, it's a descriptive name ¯\_(ツ)_/¯)
  - (TODO) producer / consumer - like above, but routing each message/event to only one receiver, with retries.
    Exactly once is never really possible.
  - (TODO) streaming - with composable async generators and iterators:
    - also comes in point-to-point, pub/sub, producer / consumer
- `interface`: external interface including HTTP routers and HTTP schemas
- `connectors`: they connect to external systems (the adapters)
- `entities`: SQLAlchemy models act as the entities.
   Some may classify DB models more towards connectors, but practice shows that they work OK as the
   structures that can be passed through the layers of the application.
- `core`: various elements needed by the entire applications, e.g. configs, logging, etc.

### Development workflow

- Makefile organizes the commands used in development.
- Start work from scratch by doing only `git clone` and `make setup run` (assuming you have basic tools installed).
- The application and its dependencies run locally with Docker Compose (`make run` to start).
- Application code reloads on changes (mounts and an alternative command in Docker Compose's overrides).
- Automatically run tests on code changes while working (`make test_reload`).
- (TODO) Local dev env and CI parity.
  - getting rid of the overrides in CI, so that the image without the mount is tested.
- Injectable locally bound container ports - accommodating self-hosted CI runners.

### Testing

- Tests are located next to the file they're testing - `_test.py` suffix.
- Test code is omitted from container images with `.dockerignore`.
  - prevents image bloat and lowers the security risks
- Pytest mark to distinguish [different kinds of tests](https://bultrowicz.com/separating_kinds_of_tests/)
  - Unit tests don't have a marker, so it's less typing.
    They can be run with `pytest "not external and not integrated"``
  - "Integrated tests" get `@pytest.mark.integrated`
    - They require resources from Docker Compose (e.g. Postgres).
    - "Integrated" as in integrated with Docker, with a database, etc. That can be integrated with any external system from our application, that's still available locally.
  - "External tests" get `@pytest.mark.external`.
    - tests that use the external interface of our application
    - in this case the interface are the HTTP endpoints on an app running in the Docker container with Docker Compose.
- Running tests in parallel with `pytest-xdist`.
- Tests modify the database.
  - Tests need to be robust enough to not be broken by that.
  - Running locally for a long time will build up entries in the database, potentially uncovering bugs,
    which is what tests are supposed to do.

### SQL

- Autogenerated DB migrations done with Alembic.
- No "N+1 select" problem because of async SQLAlchemy usage.
- Migrations without the downgrade option. Downgrades create a risk of data loss in a real system.
  If there are issues with the migrations the solution is to provide fixes in new migrations.


## TODOs

- Show coverage measurements from docker in external tests.
- `make check` should also verify that requirements.txt is up to date with poetry dependencies.
- Add Github CI for the app that removes docker-compose.override.yml to fully check the app image.
- Monorepo structure with `apps/` and `libs/`.
- ...many more things...
