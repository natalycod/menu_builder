import yaml

SERVER_API_FILENAME = 'server_api.yaml'

def read_yaml(filename):
    f = open(filename)
    result = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return result

def get_object_schema_by_path(full_schema, path):
    props = path.split('/')
    if props[0] != '#':
        return None
    obj_schema = full_schema
    for i in range(1, len(props)):
        if props[i] in obj_schema:
            obj_schema = obj_schema[props[i]]
        else:
            return None
    return obj_schema

def parse_json_to_yaml_schema(js, full_schema, obj_schema):
    if 'type' in obj_schema:
        if obj_schema['type'] == 'string':
            try:
                return str(js)
            except:
                print("Can't convert ", js, " to str", sep="") # TODO: log
                return None
        if obj_schema['type'] == 'int':
            try:
                return int(js)
            except:
                print("Can't convert ", js, " to int", sep="") # TODO: log
                return None
        if obj_schema['type'] == 'float':
            try:
                return float(js)
            except:
                print("Can't convert ", js, " to float", sep="") # TODO: log
                return None
        if obj_schema['type'] == 'array':
            try:
                result = []
                for item in js:
                    result_item = parse_json_to_yaml_schema(item, full_schema, obj_schema['items'])
                    if result_item is None:
                        return None
                    result.append(result_item)
                return result
            except:
                print("Can't convert ", js, " to array", sep="") # TODO: log
                return None
        if obj_schema['type'] == 'object':
            if 'properties' not in obj_schema:
                return {}
            try:
                result = {}
                for prop in obj_schema['properties'].keys():
                    if prop in js:
                        result_prop = parse_json_to_yaml_schema(js[prop], full_schema, obj_schema['properties'][prop])
                        if result_prop is None:
                            return None
                        result[prop] = result_prop
                return result
            except:
                print("Can't convert ", js, " to object", sep="") # TODO: log
                return None
    if '$ref' in obj_schema:
        schema = get_object_schema_by_path(full_schema, obj_schema['$ref'])
        return parse_json_to_yaml_schema(js, full_schema, schema)

def parse_json_to_handler_response(js, handler_name, query_method, response_code="200", api_filename = None):
    if api_filename is None:
        api_filename = SERVER_API_FILENAME

    full_schema = read_yaml(api_filename)
    if 'paths' not in full_schema or handler_name not in full_schema['paths'] or query_method not in full_schema['paths'][handler_name]:
        print("handler ", handler_name, " with method ", query_method, " is not specified in schema", sep="") # TODO: log
        return None

    handler_object = full_schema['paths'][handler_name][query_method]
    if 'responses' not in handler_object or response_code not in handler_object['responses']:
        print("response ", response_code, " is not specified for handler ", handler_name, " with method ", query_method) # TODO: log
        return None

    resp_object = handler_object['responses'][response_code]
    if 'content' not in resp_object or 'application/json' not in resp_object['content'] or 'schema' not in resp_object['content']['application/json']:
        print("response is described badly")
        return None
    
    resp_schema = resp_object['content']['application/json']['schema']
    return parse_json_to_yaml_schema(js, full_schema, resp_schema)
