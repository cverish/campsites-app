from campsites_db.models import Campsite, GeographicalName


class TestCampsiteFactory:
    def test_factory(self, campsite_factory, db_session):
        c = campsite_factory.create()
        assert c is not None

        # test factory autocommit
        db_results = db_session.query(Campsite).all()
        assert len(db_results) == 1, "CampsiteFactory did not auto-commit to db"
        assert db_results[0].id == c.id


class TestGeographicalNameFactory:
    def test_factory(self, geographical_name_factory, db_session):
        p = geographical_name_factory.create()
        assert p is not None

        # test factory autocommit
        db_results = db_session.query(GeographicalName).all()
        assert len(db_results) == 1, "GeographicalNameFactory did not auto-commit to db"
        assert db_results[0].id == p.id
