import factory
from factory import fuzzy
from campsites_db.models import (
    Campsite,
    CampsiteCountryEnum,
    CampsiteStateEnum,
    CampsiteTypeEnum,
    GeographicalName,
)


class CampsiteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Campsite

    code = factory.Sequence(lambda n: f"code{n:04d}")
    name = factory.Sequence(lambda n: f"name{n:04d}")
    state = CampsiteStateEnum.AB
    country = CampsiteCountryEnum.CAN
    campsite_type = CampsiteTypeEnum.AMC
    lon = fuzzy.FuzzyFloat(-180.0, 180.0)
    lat = fuzzy.FuzzyFloat(-90.0, 90.0)
    composite = factory.Sequence(lambda n: f"composite{n:04d}")


class GeographicalNameFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GeographicalName

    govt_id = factory.Sequence(lambda n: f"govt_id{n:04d}")
    name = factory.Sequence(lambda n: f"name{n:04d}")
    search_str = factory.Sequence(lambda n: f"search_str{n:04d}")
    generic_category = factory.Sequence(lambda n: f"generic_category{n:04d}")
    generic_term = factory.Sequence(lambda n: f"generic_term{n:04d}")
    state_province = CampsiteStateEnum.AB
    country = CampsiteCountryEnum.CAN
    lon = fuzzy.FuzzyFloat(-180.0, 180.0)
    lat = fuzzy.FuzzyFloat(-90.0, 90.0)
    priority_order = 1
