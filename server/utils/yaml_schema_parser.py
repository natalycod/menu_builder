import yaml

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
