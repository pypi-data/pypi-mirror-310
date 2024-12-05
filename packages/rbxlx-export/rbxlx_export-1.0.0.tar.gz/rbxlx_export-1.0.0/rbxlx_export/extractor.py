import os
import xmltodict
import re
import json

__all__ = ['run']

script_types = {
    "ModuleScript": "module",
    "Script": "server",
    "LocalScript": "client"
}

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def get_property_value(properties, prop_type, prop_name):
    prop_values = properties.get(prop_type)
    if prop_values:
        if isinstance(prop_values, list):
            for prop in prop_values:
                if prop.get('@name') == prop_name:
                    return prop.get('#text', '') or prop.get('#cdata-section', '')
        else:
            if prop_values.get('@name') == prop_name:
                return prop_values.get('#text', '') or prop_values.get('#cdata-section', '')
    return None

def load_file(file_loc):
    with open(file_loc, 'rb') as f:
        data = f.read().decode('ISO-8859-1')
    result = xmltodict.parse(data)
    return result['roblox']['Item']

def convert_item(item, where):
    if isinstance(item, list):
        item = item[0]
    class_name = item.get('@class')
    properties = item.get('Properties', {})
    item_name = get_property_value(properties, 'string', 'Name') or 'Unnamed'
    item_name_parts = [sanitize_filename(part) for part in item_name.split('/')]
    child_path = os.path.join(where, *item_name_parts)

    referent = item.get('@referent', '')

    if class_name != 'Folder':
        out_properties = {}
        for prop_type, prop_values in properties.items():
            if isinstance(prop_values, list):
                for prop in prop_values:
                    name = prop.get('@name')
                    prop_data = prop.copy()
                    prop_data.pop('@name', None)
                    out_properties[name] = {
                        '_propertyType': prop_type,
                        'values': prop_data
                    }
            else:
                name = prop_values.get('@name')
                prop_data = prop_values.copy()
                prop_data.pop('@name', None)
                out_properties[name] = {
                    '_propertyType': prop_type,
                    'values': prop_data
                }
        out_object = {
            'className': class_name,
            'name': item_name_parts[-1],
            'referent': referent,
            'properties': out_properties,
            '_exportInfo': 'Exported with rbx-export v1.0. Contains all properties of this instance.'
        }
        os.makedirs(child_path, exist_ok=True)
        if class_name == 'Model':
            file_name = os.path.join(child_path, f"{item_name_parts[-1]}.model.json")
        else:
            file_name = os.path.join(child_path, f"{item_name_parts[-1]}.{class_name}.model.json")
        property_string = json.dumps(out_object, indent=1)

        if class_name in script_types:
            class_text = script_types[class_name]
            if class_text != '':
                class_text = f".{class_text}"
            else:
                class_text = ''
            file_name = os.path.join(child_path, f"{item_name_parts[-1]}{class_text}.lua")
            protected_string = get_property_value(properties, 'ProtectedString', 'Source') or ''
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(protected_string)
            out_object['properties'].pop('ProtectedString', None)
        else:
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(property_string)
    if 'Item' in item:
        os.makedirs(child_path, exist_ok=True)
        children = item['Item']
        if not isinstance(children, list):
            children = [children]
        for child in children:
            convert_item(child, child_path)

def extract_scripts(item, where, rawname = False):
    if isinstance(item, list):
        items = item
    else:
        items = [item]
    for item in items:
        class_name = item.get('@class')
        properties = item.get('Properties', {})
        item_name = get_property_value(properties, 'string', 'Name') or 'Unnamed'
        item_name_parts = [sanitize_filename(part) for part in item_name.split('/')]
        child_path = os.path.join(where, *item_name_parts)
        if class_name in script_types:
            protected_string = get_property_value(properties, 'ProtectedString', 'Source') or ''
            class_text = script_types[class_name]
            if class_text != '':
                class_text = f".{class_text}"
            else:
                class_text = ''
            if not rawname:
                file_name = os.path.join(child_path + class_text + '.lua')
            else:
                file_name = os.path.join(child_path + '.lua')
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(protected_string)
        children = item.get('Item')
        if children:
            if not isinstance(children, list):
                children = [children]
            extract_scripts(children, child_path, rawname)

def run(location, output='Output', lua = True, json = False):
    """
    Extract scripts from a Roblox XML (RBXLX) file and save them to the specified output directory.
    :param location: Path to the Roblox XML file (.rbxlx)
    :param output: Output directory where extracted scripts will be saved
    """
    try:
        items = load_file(location)
        output_dir = os.path.join(os.getcwd(), output)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if lua:
            extract_scripts(items, output_dir, True)

        if json:
            for item in items:
                convert_item(item, output_dir)
    except Exception as e:
        print(f"An error occurred: {e}")
