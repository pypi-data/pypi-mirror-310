import warnings
import traceback
from dccXMLJSONConv.dccConv import XMLToJson
# import pytest

def test_missingList():
    # TODO: Why does the missing #list key error happen?

    filePathsWithMissingLists = [
        "./tests/data/private/1_7calibrationanddccsampledata/AndereScheine/grabbedFiles/downloads/DCCUAQuerSchnitMetaData/DCCTableXMLStub.xml",
        # "tests/data/private/1_7calibrationanddccsampledata/AndereScheine/grabbedFiles/downloads/dccQuantities/test_xmlDumpingSingleQuantNoUncer.xml",
        # "tests/data/private/1_7calibrationanddccsampledata/AndereScheine/grabbedFiles/downloads/dccQuantities/test_dccQuantTabXMLDumping.xml",
    ]

    for filePath in filePathsWithMissingLists:
        try:
            with open(filePath) as xml_file:
                xml_data = xml_file.read()
        except FileNotFoundError:
            warnings.warn(RuntimeWarning("Test data file missing!"))


        jsonDict = XMLToJson(xml_data)
        # This is the item you want to be looking at:
        assert jsonDict['dcc:list']['dcc:quantity'][2]['si:realListXMLList']['si:valueXMLList']['#list']

    