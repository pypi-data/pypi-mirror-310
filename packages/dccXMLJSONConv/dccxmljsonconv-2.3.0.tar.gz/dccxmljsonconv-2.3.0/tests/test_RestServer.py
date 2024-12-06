# This file is part of dcc-xmljsonconv (https://gitlab1.ptb.de/digitaldynamicmeasurement/dcc_XMLJSONConv)
# Copyright 2024 [Benedikt Seeger(PTB), Vanessa Stehr(PTB), Thomas Bruns (PTB)]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from fastapi.testclient import TestClient
from dccXMLJSONConv.dccServer import app
import json
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello!\nBetter use the URL /json2dcc/?js={...} \n or /dcc2json (POST method)"}

def test_dcc2json_with_valid_xml():
    xml_data = open("./data/APITestXMLStub.xml", "r").read()
    response = client.post("/dcc2json/", json={"xml": xml_data})
    responsJsonDict=json.loads(response.text)
    assert response.status_code == 200
    assert responsJsonDict==json.loads(open("./data/APITestJSONStub.json", "r").read())
    # Add more specific assertions here depending on the expected JSON output of your valid XML input

def test_dcc2json_with_empty_xml():
    response = client.post("/dcc2json/", json={"xml": ""})
    assert response.status_code == 400  # returnes 400 Bad Request

def test_json2dcc_with_valid_json():
    json_data = json.loads(open("./data/APITestJSONStub.json", "r").read())
    response = client.post("/json2dcc/", json={"js": json_data})
    assert response.status_code == 200
    assert response.text==open("./data/unindentedJSONTOXMLRespons.xml", "r").read()
    # Add more specific assertions here depending on the expected XML output of your valid JSON input


def test_json2dcc_with_empty_json():
    response = client.post("/json2dcc/", json={"js": {}})
    assert response.status_code == 400  # Assuming it's not successful; adjust based on your error handling
