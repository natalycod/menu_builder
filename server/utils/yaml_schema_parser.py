import yaml

def read_yaml(filename):
    f = open(filename)
    result = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return result

def parse_json_to_yaml_schema(js, schema):
    if 'type' in schema:
        if schema['type'] == 'string':
            try:
                return str(js)
            except:
                print("Can't convert ", js, " to str", sep="") # TODO: log
                return None
        if schema['type'] == 'int':
            try:
                return int(js)
            except:
                print("Can't convert ", js, " to int", sep="") # TODO: log
                return None
        if schema['type'] == 'float':
            try:
                return float(js)
            except:
                print("Can't convert ", js, " to float", sep="") # TODO: log
                return None
        if schema['type'] == 'array':
            try:
                result = []
                for item in js:
                    result_item = parse_json_to_yaml_schema(item, schema['items'])
                    if result_item is None:
                        return None
                    result.append(result_item)
                return result
            except:
                print("Can't convert ", js, " to array", sep="") # TODO: log
                return None
        if schema['type'] == 'object':
            try:
                result = {}
                for prop in schema['properties'].keys():
                    if prop in js:
                        result_prop = parse_json_to_yaml_schema(js[prop], schema['properties'][prop])
                        if result_prop is None:
                            return None
                        result[prop] = result_prop
                return result
            except:
                print("Can't convert ", js, " to object", sep="") # TODO: log
                return None
    if '$ref' in schema:
        pass
