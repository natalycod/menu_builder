import pytest

import utils.yaml_schema_parser as yaml_schema_parser


yaml_objects = yaml_schema_parser.read_yaml('tests/static/yaml_parser_objects.yaml')


@pytest.mark.parametrize(
    ('value','expected_result'),
    [
        pytest.param('hi', 'hi'),
        pytest.param(123, '123'),
        pytest.param(123.45, '123.45'),
        pytest.param({'hi': 'hello'}, "{'hi': 'hello'}"),
    ]
)
def test_string_value(value, expected_result):
    result = yaml_schema_parser.parse_json_to_yaml_schema(value, yaml_objects, yaml_objects['SimpleString'])
    assert result == expected_result


@pytest.mark.parametrize(
    ('value','expected_result'),
    [
        pytest.param(123, 123),
        pytest.param('123', 123),
        pytest.param(123.45, 123),
    ]
)
def test_int_value(value, expected_result):
    result = yaml_schema_parser.parse_json_to_yaml_schema(value, yaml_objects, yaml_objects['SimpleInt'])
    assert result == expected_result


@pytest.mark.parametrize(
    ('value','expected_result'),
    [
        pytest.param(123, 123.0),
        pytest.param('123', 123.0),
        pytest.param(123.45, 123.45),
        pytest.param('123.45', 123.45),
    ]
)
def test_float_value(value, expected_result):
    result = yaml_schema_parser.parse_json_to_yaml_schema(value, yaml_objects, yaml_objects['SimpleFloat'])
    assert result == expected_result

@pytest.mark.parametrize(
    ('value','expected_result'),
    [
        pytest.param([1, 2, 3], [1, 2, 3]),
        pytest.param(['1', '2', '3'], [1, 2, 3]),
        pytest.param(['1', 2.34, 3], [1, 2, 3]),
    ]
)
def test_int_array(value, expected_result):
    result = yaml_schema_parser.parse_json_to_yaml_schema(value, yaml_objects, yaml_objects['IntArray'])
    assert result == expected_result

@pytest.mark.parametrize(
    ('value','expected_result'),
    [
        pytest.param({}, {}),
        pytest.param({'some_str': 'hi', 'some_int': 42, 'some_float': 42.42}, {'some_str': 'hi', 'some_int': 42, 'some_float': 42.42}),
        pytest.param({'some_str': 12.34, 'some_int': 42.4, 'some_float': '42.42'}, {'some_str': '12.34', 'some_int': 42, 'some_float': 42.42}),
        pytest.param({'some_str': 'hi', 'some_int': 42.4, 'some_float': '42.42', 'extra': 'hi!'}, {'some_str': 'hi', 'some_int': 42, 'some_float': 42.42})
    ]
)
def test_simple_object(value, expected_result):
    result = yaml_schema_parser.parse_json_to_yaml_schema(value, yaml_objects, yaml_objects['SimpleObject'])
    assert result == expected_result

@pytest.mark.parametrize(
    ('value','expected_result'),
    [
        pytest.param({}, {}),
        pytest.param(
            {'str_arr': [{'just_int': 1}, {'just_int': 2.3}, {'just_int': '4'}]},
            {'str_arr': [{'just_int': 1}, {'just_int': 2}, {'just_int': 4}]},
        ),
        pytest.param(
            {'some_obj': {'one_more_obj': {'prop_one': '1', 'prop_two': 2}}},
            {'some_obj': {'one_more_obj': {'prop_one': 1, 'prop_two': 2}}},
        ),
        pytest.param(
            {'some_obj': {'one_more_obj': {'prop_one': '1', 'prop_two': 2}}, 'str_arr': [{'just_int': 1}, {'just_int': 2.3}, {'just_int': '4'}]},
            {'some_obj': {'one_more_obj': {'prop_one': 1, 'prop_two': 2}}, 'str_arr': [{'just_int': 1}, {'just_int': 2}, {'just_int': 4}]},
        ),
        pytest.param(
            {'some_obj': {}},
            {'some_obj': {}},
        ),
        pytest.param(
            {'some_obj': {'one_more_obj': {'prop_three': 3}}, 'str_arr': []},
            {'some_obj': {'one_more_obj': {}}, 'str_arr': []},
        ),
    ]
)
def test_recursive_object(value, expected_result):
    result = yaml_schema_parser.parse_json_to_yaml_schema(value, yaml_objects, yaml_objects['RecursiveObject'])
    assert result == expected_result

@pytest.mark.parametrize(
    ('value','expected_result'),
    [
        pytest.param(123, 123),
        pytest.param('123', 123),
        pytest.param(123.45, 123),
    ]
)
def test_ref_int(value, expected_result):
    result = yaml_schema_parser.parse_json_to_yaml_schema(value, yaml_objects, yaml_objects['RefInt'])
    assert result == expected_result

@pytest.mark.parametrize(
    ('value','expected_result'),
    [
        pytest.param({}, {}),
        pytest.param({'one_prop': 1, 'two_prop': '2.3'}, {'one_prop': '1', 'two_prop': 2.3}),
    ]
)
def test_ref_component(value, expected_result):
    result = yaml_schema_parser.parse_json_to_yaml_schema(value, yaml_objects, yaml_objects['RefComponent'])
    assert result == expected_result

@pytest.mark.parametrize(
    ('value','expected_result'),
    [
        pytest.param({}, {}),
        pytest.param({'one_prop': {'one_prop': 'abc', 'two_prop': '123'}, 'two_prop': '123'}, {'one_prop': {'one_prop': 'abc', 'two_prop': 123}, 'two_prop': 123}),
    ]
)
def test_ref_recursive(value, expected_result):
    result = yaml_schema_parser.parse_json_to_yaml_schema(value, yaml_objects, yaml_objects['RefRecursive'])
    assert result == expected_result


@pytest.mark.parametrize(
    ('response_code', 'value','expected_result'),
    [
        pytest.param('200', {}, {}),
        pytest.param('200', {'param1': 123.45, 'param2': 123.45, 'param3': [123.45, '123']}, {'param1': '123.45', 'param2': 123.45, 'param3': [123, 123]}),
        pytest.param('400', {'param1': 123.45, 'param2': 123.45, 'param3': [123.45, '123']}, {}),
    ]
)
def test_test_handler(response_code, value, expected_result):
    result = yaml_schema_parser.parse_json_to_handler_response(value, '/test_handler', 'post', response_code, 'tests/static/yaml_parser_api.yaml')
    assert result == expected_result
