from server.campsites_api.dto.campsites import CampsiteDTO, CampsiteListDTO


class TestCampsitesRouter:
    def test_get_campsite(self, test_client, campsite_factory, db_session):
        c = campsite_factory.create()
        # this one should not be returned
        campsite_factory.create()

        response = test_client.get(f"/campsites/campsite/{c.id}")
        assert response.status_code == 200

        data = CampsiteDTO(**response.json())
        assert data.id == c.id

    def test_list_campsites(self, test_client, campsite_factory):
        c = campsite_factory.create_batch(3)

        response = test_client.get("/campsites")
        assert response.status_code == 200

        data = CampsiteListDTO(**response.json())
        assert data.num_total_results == 3

        # default sort is name
        assert [item.name for item in data.items] == [c[0].name, c[1].name, c[2].name]
