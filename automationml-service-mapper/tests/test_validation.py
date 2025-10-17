
from fastapi.testclient import TestClient
from aml_service_mapper.main import app

client = TestClient(app)

def test_rejects_unsupported_media_type():
    r = client.post("/v1/transform/legacy-to-modern",
                    headers={"Content-Type":"text/plain","X-API-Key":"dev-key"},
                    data="hello")
    assert r.status_code == 415

def test_rejects_bad_apikey():
    r = client.post("/v1/transform/legacy-to-modern",
                    headers={"Content-Type":"application/json","X-API-Key":"wrong"},
                    json={"customer": {"id": "1"}, "order": {"total": "1", "items": [{"sku":"A","qty":1}]}})
    assert r.status_code == 401
