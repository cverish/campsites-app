import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy_utils import create_database, drop_database, database_exists

from campsites_db.models import Base
from campsites_db.session import get_session

from campsites_api.app import create_app
from server.campsites_api.services.campsites_service import get_campsites_service
from server.campsites_api.services.places_service import get_places_service
from server.campsites_api.tests.factories import (
    CampsiteFactory,
    GeographicalNameFactory,
)


def pytest_addoption(parser):
    parser.addoption(
        "--dburl",
        action="store",
        default="postgresql://postgres:postgres@campsites_postgresql/test",
        help="Database URL to use for tests",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    db_url = session.config.getoption("--dburl")
    try:
        engine = create_engine(db_url, poolclass=StaticPool, echo=True)
        connection = engine.connect()
        connection.close()
        print("Database connection successful")  # noqa: T201
    except SQLAlchemyOperationalError as e:
        print(f"Failed to connect to database at {db_url}: {repr(e)}")  # noqa: T201
        pytest.exit(
            "Stopping tests because database connection could not be established"
        )


@pytest.fixture(scope="session")
def db_url(request):
    return request.config.getoption("--dburl")


# spin up new database for tests
@pytest.fixture(scope="session", autouse=True)
def create_and_delete_database(db_url):
    if database_exists(db_url):
        print(  # noqa: T201
            "Test database already exists. Dropping test database before starting tests."
        )
        drop_database(db_url)

    print("Creating test database.")  # noqa: T201
    create_database(db_url)

    yield

    close_all_sessions()
    drop_database(db_url)


@pytest.fixture(scope="function")
def db_session(db_url):
    engine = create_engine(
        db_url,
        poolclass=StaticPool,
    )

    with engine.connect() as connection:
        # install PostGIS extension
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        connection.commit()

    # Create a sessionmaker to manage sessions
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables in the database
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def campsite_factory(db_session):
    """For some reason, when the sqlalchemy_session was set in db_session before yielding the session,
    the session was not being correctly passed to the CampsiteFactory. Instead, pass this to the tests
    that use CampsiteFactory and instantiate using campsite_factory"""
    CampsiteFactory._meta.sqlalchemy_session = db_session
    CampsiteFactory._meta.sqlalchemy_session_persistence = "commit"
    yield CampsiteFactory


@pytest.fixture(scope="function")
def geographical_name_factory(db_session):
    GeographicalNameFactory._meta.sqlalchemy_session = db_session
    GeographicalNameFactory._meta.sqlalchemy_session_persistence = "commit"
    yield GeographicalNameFactory


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    # I'm not sure why these dependencies need to be overwritten but it doesn't work without it
    def override_campsites_service(_):
        yield get_campsites_service

    def override_places_service(_):
        yield get_places_service

    app = create_app()

    app.dependency_overrides[get_session] = override_get_db
    app.dependency_overrides[get_campsites_service] = override_campsites_service
    app.dependency_overrides[get_places_service] = override_places_service

    with TestClient(app) as test_client:
        yield test_client
