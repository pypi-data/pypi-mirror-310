import os
import json
import pytest
from dccXMLJSONConv.typeCastDictCreator import XSDParserCacheWrapper

@pytest.fixture
def setup_wrapper():
    # Set up a temporary JSON file to simulate cache
    test_cache_file = "test_cache.json"
    if os.path.exists(test_cache_file):
        os.remove(test_cache_file)
    with open(test_cache_file, 'w') as f:
        json.dump({}, f)

    # Initialize the XSDParserCacheWrapper with the test cache file
    wrapper = XSDParserCacheWrapper(test_cache_file)
    yield wrapper, test_cache_file

    # Clean up the temporary JSON file after tests
    if os.path.exists(test_cache_file):
        os.remove(test_cache_file)


def test_parse_with_cache_no_cache(setup_wrapper):
    wrapper, test_cache_file = setup_wrapper

    # Test with a schema that is not in the cache
    url = 'https://www.ptb.de/dcc/v3.3.0/dcc.xsd'
    namespace = 'dcc'
    version = None

    # Attempt to parse the schema and add it to cache
    non_list_dict, list_dict = wrapper.parse_with_cache(url, namespace, version)

    # Check if the cache file is updated
    with open(test_cache_file, 'r') as f:
        cache = json.load(f)
        cache_key = json.dumps((url.replace('/v3.3.0', ''), '3.3.0'))
        assert cache_key in cache


def test_parse_with_cache_existing_cache(setup_wrapper):
    wrapper, test_cache_file = setup_wrapper

    # Add a dummy entry to the cache file
    dummy_key = json.dumps(('https://www.ptb.de/dcc/', '3.3.0'))
    dummy_value = {
        'non_list_typecast_dict': json.dumps({'element1': 'str'}),
        'list_typecast_dict': json.dumps({'element2': 'int'})
    }
    with open(test_cache_file, 'w') as f:
        json.dump({dummy_key: dummy_value}, f)

    # Attempt to parse the schema with the same URL and version
    url = 'https://www.ptb.de/dcc/v3.3.0/dcc.xsd'
    namespace = 'dcc'
    version = '3.3.0'

    non_list_dict, list_dict = wrapper.parse_with_cache(url, namespace, version)

    # Check if the returned dictionaries match the dummy data
    assert non_list_dict == {'element1': str}
    assert list_dict == {'element2': int}


def test_extract_version_from_url(setup_wrapper):
    wrapper, _ = setup_wrapper

    # Test extracting version from various URLs
    urls = [
        'https://www.ptb.de/dcc/v3.3.0/dcc.xsd',
        'https://www.ptb.de/dcc/v3.0.0-rc.2/dcc.xsd',
        'https://www.ptb.de/dcc/v3.2.1/dcc.xsd',
        'https://www.ptb.de/dcc/v3.1.0/dcc.xsd',
        'https://www.ptb.de/dcc/v2.4.0/dcc.xsd'
    ]
    expected_versions = ['3.3.0', '3.0.0-rc.2', '3.2.1', '3.1.0', '2.4.0']

    for url, expected_version in zip(urls, expected_versions):
        version = wrapper.extract_version_from_url(url)
        assert version == expected_version


if __name__ == '__main__':
    pytest.main()
