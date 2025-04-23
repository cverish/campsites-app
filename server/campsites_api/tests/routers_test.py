import uuid

import pytest
from campsites_api.dto.campsites import CampsiteDTO, CampsiteListDTO
from campsites_api.tests.const import (
    example_filter_combos,
    example_csv_content,
    example_incorrect_csv_content,
)
from campsites_db.models import Campsite


class TestCampsitesRouter:
    class TestGetCampsite:
        def test_get_campsite(self, test_client, campsite_factory):
            c = campsite_factory.create()
            # this one should not be returned
            campsite_factory.create()

            response = test_client.get(f"/campsites/campsite/{c.id}")
            assert response.status_code == 200

            data = CampsiteDTO(**response.json())
            assert data.id == c.id, "Query is not filtering by correct ID"

        def test_get_campsite_invalid_id(self, test_client):
            response = test_client.get("/campsites/campsite/foobar")
            assert response.status_code == 422

        def test_get_campsite_404(self, test_client):
            uuid4 = uuid.uuid4()
            response = test_client.get(f"/campsites/campsite/{uuid4}")
            assert response.status_code == 404

    class TestListCampsites:
        def test_list_campsites(self, test_client, campsite_factory):
            c = campsite_factory.create_batch(3)

            response = test_client.get("/campsites")
            assert response.status_code == 200

            data = CampsiteListDTO(**response.json())
            assert data.num_total_results == 3

            # default sort is name
            assert [item.id for item in data.items] == [c[0].id, c[1].id, c[2].id]

        def test_list_campsites_sort(self, test_client, campsite_factory):
            c = campsite_factory.create_batch(3)

            response = test_client.get(
                "/campsites", params={"sort_by": "code", "sort_dir": "desc"}
            )
            data = CampsiteListDTO(**response.json())

            assert data.num_total_results == 3
            assert [item.id for item in data.items] == [c[2].id, c[1].id, c[0].id]

        def test_list_campsites_pagination(self, test_client, campsite_factory):
            c = campsite_factory.create_batch(3)

            response = test_client.get("/campsites", params={"limit": 2})
            data = CampsiteListDTO(**response.json())

            assert data.num_total_results == 3
            assert len(data.items) == 2
            assert [item.id for item in data.items] == [c[0].id, c[1].id]

            response = test_client.get("/campsites", params={"limit": 2, "offset": 2})
            data = CampsiteListDTO(**response.json())
            assert len(data.items) == 1
            assert data.items[0].id == c[2].id

        @pytest.mark.parametrize(
            "obj_attr,filter_attr,_",
            example_filter_combos,
            ids=[e[2] for e in example_filter_combos],
        )
        def test_list_campsites_filter(
            self, obj_attr, filter_attr, _, test_client, campsite_factory
        ):
            c_exp = campsite_factory.create(**obj_attr)
            # generic campsite that should be filtered out
            campsite_factory.create()

            response = test_client.get("/campsites", params=filter_attr)
            data = CampsiteListDTO(**response.json())

            assert data.num_total_results == 1
            assert data.items[0].id == c_exp.id

        def test_list_campsites_distance(self, test_client, campsite_factory):
            c_exp = campsite_factory.create(lat=41.751, lon=-70.593)
            # campsite outside of range
            campsite_factory.create(lat=50.0, lon=-74.0)

            target = (42.3584308, -71.0597732)  # boston

            response = test_client.get(
                "/campsites",
                params={
                    "distance_value": 50,
                    "distance_units": "mi",
                    "distance_lat": target[0],
                    "distance_lon": target[1],
                },
            )
            data = CampsiteListDTO(**response.json())

            assert data.num_total_results == 1
            assert data.items[0].id == c_exp.id

            # smaller range should now exclude campsite
            response = test_client.get(
                "/campsites",
                params={
                    "distance_value": 2,
                    "distance_units": "mi",
                    "distance_lat": target[0],
                    "distance_lon": target[1],
                },
            )
            data = CampsiteListDTO(**response.json())

            assert data.num_total_results == 0

        def test_list_campsites_distance_incomplete(
            self, test_client, campsite_factory
        ):
            # campsite outside of range
            campsite_factory.create(lat=41.751, lon=-70.593)
            campsite_factory.create(lat=50.0, lon=-74.0)

            target = (42.3584308, -71.0597732)  # boston

            # provide incomplete distance parameters
            response = test_client.get(
                "/campsites",
                params={"distance_lat": target[0], "distance_lon": target[1]},
            )
            data = CampsiteListDTO(**response.json())

            # should not filter based on distance without all parameters
            assert data.num_total_results == 2

    class TestPostCampsite:
        def test_post_campsite(self, test_client, db_session):
            c = CampsiteDTO(
                name="foobar",
                state="MN",
                country="USA",
                lon=0,
                lat=0,
                composite="composite",
            )

            response = test_client.post(
                "/campsites/campsite", content=c.model_dump_json()
            )
            assert response.status_code == 200

            data = CampsiteDTO(**response.json())
            assert data.id is not None
            assert data.name == c.name

            db_c = db_session.query(Campsite).all()
            assert len(db_c) == 1
            assert db_c[0].name == c.name

        def test_post_campsite_incomplete(self, test_client):
            response = test_client.post(
                "/campsites/campsite", content='{"name": "foobar"}'
            )
            assert response.status_code == 422

    class TestPatchCampsite:
        def test_patch_campsite(self, test_client, db_session, campsite_factory):
            c = campsite_factory.create(name="foobar")
            c_new = CampsiteDTO(
                **{**c.__dict__, "name": "fizzbang", "campsite_type": "AUTH"}
            )

            response = test_client.patch(
                f"/campsites/campsite/{c.id}", content=c_new.model_dump_json()
            )
            assert response.status_code == 200

            data = CampsiteDTO(**response.json())
            assert data.id == c.id
            assert data.name == "fizzbang"
            assert data.campsite_type == "AUTH"

            db_c = db_session.query(Campsite).all()
            assert len(db_c) == 1
            assert db_c[0].name == "fizzbang"
            assert db_c[0].campsite_type == "AUTH"

        def test_patch_campsite_incomplete(
            self, test_client, db_session, campsite_factory
        ):
            c = campsite_factory.create(name="foobar")

            response = test_client.patch(
                f"/campsites/campsite/{c.id}",
                content='{"name": "fizzbang", "campsite_type": "AUTH"}',
            )
            assert response.status_code == 422

            db_c = db_session.query(Campsite).all()
            assert len(db_c) == 1
            assert db_c[0].name == "foobar"

    class TestDeleteCampsite:
        def test_delete_campsite(self, test_client, db_session, campsite_factory):
            c = campsite_factory.create()

            response = test_client.delete(f"/campsites/campsite/{c.id}")
            assert response.status_code == 200

            assert db_session.query(Campsite).count() == 0

        def test_delete_campsite_does_not_exist(
            self, test_client, db_session, campsite_factory
        ):
            response = test_client.delete(f"/campsites/campsite/{uuid.uuid4()}")
            assert response.status_code == 404

    class TestUploadCampsites:
        def test_upload_campsites(self, test_client, db_session, tmp_path):
            p = tmp_path / "test.csv"
            p.write_text(example_csv_content)
            with open(p, "rb") as f:
                response = test_client.post("/campsites/upload", files={"csv_file": f})

            assert response.status_code == 200

            db_c = db_session.query(Campsite).all()
            assert len(db_c) == 4

        def test_upload_campsites_wrong_data(self, test_client, db_session, tmp_path):
            p = tmp_path / "test.csv"
            p.write_text(example_incorrect_csv_content)
            with open(p, "rb") as f:
                response = test_client.post("/campsites/upload", files={"csv_file": f})

            assert response.status_code == 422
