
from fastapi.testclient import TestClient
from aml_service_mapper.main import app

client = TestClient(app)

def test_json_public_policy_drops_pii_and_maps_list():
    payload = {
        "customer": {"id": "CUST-1", "name": "John Public"},
        "order": {"total": "10.50", "items": [{"sku": "X", "qty": 1}]}
    }
    r = client.post("/v1/transform/legacy-to-modern",
                    headers={"Content-Type":"application/json","X-API-Key":"dev-key","X-Data-Policy":"public"},
                    json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["user"]["user_id"] == "CUST-1"
    assert "full_name" not in data["user"]  # dropped due to PII tag
    assert data["order"]["total_amount"] == 10.5
    assert data["order"]["lines"][0]["sku"] == "X"
    assert data["order"]["lines"][0]["quantity"] == 1
    assert data["meta"]["policy_applied"] == "public"

def test_xml_internal_policy_keeps_pii_and_maps_list():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
<LegacyOrderRequest>
  <customer>
    <id>CUST-2</id>
    <name>Jane Internal</name>
  </customer>
  <order>
    <total>42</total>
    <items><item><sku>Y</sku><qty>2</qty></item></items>
  </order>
</LegacyOrderRequest>'''
    r = client.post("/v1/transform/legacy-to-modern",
                    headers={"Content-Type":"application/xml","X-API-Key":"dev-key","X-Data-Policy":"internal"},
                    data=xml.encode("utf-8"))
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["user"]["user_id"] == "CUST-2"
    assert data["user"]["full_name"] == "Jane Internal"
    assert data["order"]["total_amount"] == 42.0
    assert data["order"]["lines"][0]["sku"] == "Y"
    assert data["order"]["lines"][0]["quantity"] == 2
    assert data["meta"]["policy_applied"] == "internal"
