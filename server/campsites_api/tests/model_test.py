class TestCampsiteFactory:
    def test_factory(self, campsite_factory):
        c = campsite_factory.create()
        assert c is not None


class TestGeographicalNameFactory:
    def test_factory(self, geographical_name_factory):
        p = geographical_name_factory.create()
        assert p is not None
