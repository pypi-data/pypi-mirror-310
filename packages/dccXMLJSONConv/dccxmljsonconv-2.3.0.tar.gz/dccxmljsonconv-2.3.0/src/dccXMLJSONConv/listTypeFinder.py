import requests
import json
from lxml import etree
import sys
import pathlib
import io


def download_xsd(url: str):
    """
    Downloads an XSD file from a given URL.

    Parameters:
        url (str): The URL of the XSD file to download.

    Returns:
        io.BytesIO: A bytes stream of the downloaded XSD file if successful, None otherwise.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return io.BytesIO(response.content)
    return None


def find_list_types(xsd_path: str):
    """
    Parses an XSD file to find elements with types ending in 'ListType'.

    Parameters:
        xsd_path (str): The path to the XSD file.

    Returns:
        tuple: A tuple containing two elements; the first is a list of names of the list types,
               and the second is a list of attributes of the list types.
    """
    tree = etree.parse(xsd_path)
    list_types = []
    for element in tree.iter():
        if 'name' in element.attrib and element.tag.endswith('simpleType'):
            name = element.attrib['name']
            if name.endswith('ListType'):
                item_type = element.find('.//xs:list', namespaces={'xs': 'http://www.w3.org/2001/XMLSchema'})
                if item_type is not None and 'itemType' in item_type.attrib:
                    list_types.append({'name': name, 'itemType': item_type.attrib['itemType']})
    names = [list_type['name'] for list_type in list_types]
    return names, list_types


def map_item_type_to_python_type(item_type):
    """
    Maps an XSD item type to the corresponding Python type for casting.

    Parameters:
        item_type (str): The XSD item type.

    Returns:
        str: The corresponding Python type.
    """
    type_mapping = {
        'xs:string': 'str',
        'xs:double': 'float',
        'xs:decimal': 'float',
        'xs:integer': 'int',
        'xs:dateTime': 'str',  # datetime type can be handled separately if needed
        'si:unitType': 'str',
        'si:unitPhaseType': 'str',
        'si:decimalType': 'float',
        'si:uncertaintyValueType': 'float',
        'si:kValueType': 'float',
        'si:probabilityValueType': 'float',
        'xs:boolean': 'bool',
        'dcc:stringConformityStatementStatusType': 'str', # infact enum of 	['pass', 'fail', 'conditionalPass', 'conditionalFail',	'noPass', 'noFail'

    }
    return type_mapping.get(item_type, 'str')  # Default to str if not found


def extract_list_types_info(xsd_path: str):
    """
    Extracts list types information from an XSD file.

    Parameters:
        xsd_path (str): The path to the XSD file.

    Returns:
        list: A list of dictionaries containing information about list types.
    """
    names, list_types = find_list_types(xsd_path)
    list_types_info = []

    for lt in list_types:
        name = lt['name']
        item_type = lt['itemType']
        python_type = map_item_type_to_python_type(item_type)
        list_types_info.append({'name': name, 'type': item_type, 'cast_type': python_type})

    return list_types_info


def find_repeated_elements(xsd_path: str):
    """
    Parses an XSD file to identify elements that can be repeated.

    Parameters:
        xsd_path (str): The path to the XSD file.

    Returns:
        tuple: A tuple containing two elements; the first is a list of names of the repeated elements,
               and the second is a dictionary with the names as keys and the max occurrences as values.
    """
    tree = etree.parse(xsd_path)
    repeated_elements = {}
    for element in tree.iter():
        if element.tag is etree.Comment:
            continue
        if element.tag.endswith('element'):
            name = element.get('name')
            try:
                if not 'XMLList' in name:
                    type_ = element.get('type')
                    max_occurs = element.get('maxOccurs', '1')  # Default is 1 if not specified
                    if max_occurs not in ('1', 'unbounded'):
                        repeated_elements[name] = type_
                    elif max_occurs == 'unbounded':
                        repeated_elements[name] = type_
                else:
                    print(name+" Skipping XMLLists for automatic embedding in lists since this can only happen in ListTypeMements anyways.")
            except:
                pass
    names = list(repeated_elements.keys())
    return names, repeated_elements


def extract_space_separated_list_types(xsd_path: str):
    """
    Extracts space-separated list types from an XSD file.

    Parameters:
        xsd_path (str): The path to the XSD file.

    Returns:
        dict: A dictionary containing information about space-separated list types.
    """
    list_types_info = extract_list_types_info(xsd_path)
    space_separated_list_types = {'spaceSeparatedNumberListTypes': [], 'spaceSeparatedStrListTypes': []}

    number_types = ['float', 'int']

    for lt in list_types_info:
        if lt['cast_type'] in number_types:
            space_separated_list_types['spaceSeparatedNumberListTypes'].append(lt)
        else:
            space_separated_list_types['spaceSeparatedStrListTypes'].append(lt)

    return space_separated_list_types


def merge_dicts(dict1, dict2):
    """
    Merges two dictionaries by combining their lists.

    Parameters:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.

    Returns:
        dict: The merged dictionary.
    """
    merged = {}
    for key in dict1.keys() | dict2.keys():
        merged[key] = dict1.get(key, []) + dict2.get(key, [])
    return merged


def write_to_json(data: dict, file_path: str):
    """
    Writes a given dictionary to a JSON file, with all keys sorted alphabetically at all nesting levels.

    Parameters:
        data (dict): The data to write to the file.
        file_path (str): The path to the JSON file where the data should be saved.
    """

    def sort_dict_recursively(d):
        """
        Recursively sorts a dictionary by its keys.
        """
        if isinstance(d, dict):
            return {key: sort_dict_recursively(value) for key, value in sorted(d.items())}
        elif isinstance(d, list):
            return [sort_dict_recursively(item) for item in d]
        else:
            return d

    # Sort the data recursively
    sorted_data = sort_dict_recursively(data)

    # Write the sorted data to the JSON file
    with open(file_path, 'w') as file:
        json.dump(sorted_data, file, indent=4)


# This method now recursively sorts all nested dictionaries.


def process_xsd(url: str):
    """
    Processes an XSD file from a URL to extract list types and repeated elements.

    Parameters:
        url (str): The URL of the XSD file.

    Returns:
        tuple: A tuple containing information about list types, repeated elements, and space-separated list types found in the XSD file.
    """
    xsd_file = download_xsd(url)
    if xsd_file:
        names, list_types = find_list_types(xsd_file)
        xsd_file.seek(0)  # Reset file pointer to the beginning
        repeated_field_names, repeated_field_types = find_repeated_elements(xsd_file)
        xsd_file.seek(0)  # Reset file pointer to the beginning
        space_separated_list_types = extract_space_separated_list_types(xsd_file)
        return names, list_types, repeated_field_names, repeated_field_types, space_separated_list_types
    else:
        print(f"Failed to download XSD file from {url}")
        return [], [], [], {}, {'spaceSeparatedNumberListTypes': [], 'spaceSeparatedStrListTypes': []}


def create_space_separated_dict(space_separated_list_types):
    """
    Creates a dictionary with the space-separated field names in their namespace.

    Parameters:
        space_separated_list_types (dict): A dictionary containing space-separated list types.

    Returns:
        dict: A dictionary containing the space-separated field names in their namespace.
    """
    space_separated_dict = {}

    for key, value in space_separated_list_types.items():
        for item in value:
            field_name = item['name']
            namespace = item['type'].split(":")[0]
            cast_type = item['cast_type']
            space_separated_dict[field_name] = {'namespace': namespace, 'cast_type': cast_type}

    return space_separated_dict


def create_repeated_types_dict(repeated_field_types):
    """
    Creates a dictionary with the repeated field names and their types.

    Parameters:
        repeated_field_types (dict): A dictionary containing repeated field names and their types.

    Returns:
        dict: A dictionary containing the repeated field names and their types.
    """
    repeated_types_dict = {}
    for field_name, type_ in repeated_field_types.items():
        repeated_types_dict[field_name] = type_
    return repeated_types_dict


def create_casting_hints_dict(space_separated_list_types):
    """
    Creates a dictionary with field names as keys and type casting hints as values.

    Parameters:
        space_separated_list_types (dict): A dictionary containing space-separated list types.

    Returns:
        dict: A dictionary with field names as keys and type casting hints as values.
    """
    casting_hints_dict = {}
    for key, value in space_separated_list_types.items():
        for item in value:
            field_name = item['name']
            cast_type = item['cast_type']
            casting_hints_dict[field_name] = cast_type

    return casting_hints_dict


def find_elements_by_type(xsd_path: str, casting_hints_dict):
    """
    Finds elements in the XML structure that correspond to the types listed in casting_hints_dict.

    Parameters:
        xsd_path (str): The path to the XSD file.
        casting_hints_dict (dict): A dictionary with field names as keys and type casting hints as values.

    Returns:
        dict: A dictionary with field names and their corresponding node tags.
    """
    tree = etree.parse(xsd_path)
    elements_by_type = {}
    for element in tree.iter():
        try:
            print(element.attrib['type'])
            print(element.attrib['name'])
        except:
            pass
        if 'type' in element.attrib and element.attrib['type'].split(':')[1] in casting_hints_dict:
            print(element.attrib['type'])
            field_name = element.attrib['name']
            elements_by_type[field_name] = casting_hints_dict[element.attrib['type'].split(':')[1]]
    return elements_by_type


def main():
    """
    The main function to run the script. It handles command-line arguments for the XSD URLs
    and output JSON file path, processes the XSD files to extract list types and repeated elements,
    merges the results, and writes them to a JSON file.
    """
    if len(sys.argv) > 2:
        urls = sys.argv[1:-1]  # All but the last argument
        json_file_path = sys.argv[-1]  # The last argument
    else:
        urls=["https://ptb.de/si/v2.1.0/SI_Format.xsd","https://ptb.de/si/v2.2.1/SI_Format.xsd", "https://ptb.de/dcc/v3.2.1/dcc.xsd"]
        script_location = pathlib.Path(__file__).resolve().parent.parent
        json_file_path = script_location.parent / 'src' / 'dccXMLJSONConv' / 'data' / 'listDCCElements.json'

    combined_names = []
    combined_list_types = []
    combined_repeated_field_names = []
    combined_repeated_field_types = {}
    combined_space_separated_list_types = {'spaceSeparatedNumberListTypes': [], 'spaceSeparatedStrListTypes': []}

    for url in urls:
        names, list_types, repeated_field_names, repeated_field_types, space_separated_list_types = process_xsd(url)

        combined_names = list(set(combined_names + names))
        combined_list_types += list_types
        combined_repeated_field_names = list(set(combined_repeated_field_names + repeated_field_names))
        combined_repeated_field_types.update(repeated_field_types)
        combined_space_separated_list_types = merge_dicts(combined_space_separated_list_types,
                                                          space_separated_list_types)

    # Create space-separated dictionary
    space_separated_dict = create_space_separated_dict(combined_space_separated_list_types)

    # Create repeated types dictionary
    repeated_types_dict = create_repeated_types_dict(combined_repeated_field_types)

    # Create casting hints dictionary
    casting_hints_dict = create_casting_hints_dict(combined_space_separated_list_types)

    # Find elements by type
    elements_by_type = {}
    for url in urls:
        xsd_file = download_xsd(url)
        if xsd_file:
            elements_by_type.update(find_elements_by_type(xsd_file, casting_hints_dict))

    # Write to JSON
    write_to_json({
        'schemaUrls': urls,
        'listTypeElements': combined_names,
        'listTypeElementsDetails': combined_list_types,
        'repeatedFieldNames': combined_repeated_field_names,
        'repeatedFieldNamesDetails': combined_repeated_field_types,
        'spaceSeparatedListTypes': combined_space_separated_list_types,
        'spaceSeparatedDict': space_separated_dict,
        'repeatedTypesDict': repeated_types_dict,
        'castingHintsDict': casting_hints_dict,
        'spaceSeperatedFieldNamesAndTypes': elements_by_type
    }, json_file_path)
    print(f"Combined list types have been written to {json_file_path}")


if __name__ == "__main__":
    main()
