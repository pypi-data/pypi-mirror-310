from __future__ import annotations

import pytest

from asyncopenapi3 import OpenAPI

from yaml import safe_load

LOADED_FILES = {}


def _get_parsed_yaml(filename):
    """
    Returns a python dict that is a parsed yaml file from the tests/fixtures
    directory.

    :param filename: The filename to load.  Must exist in tests/fixtures and
                     include extension.
    :type filename: str
    """
    if filename not in LOADED_FILES:
        with open("tests/fixtures/" + filename) as f:
            raw = f.read()
        parsed = safe_load(raw)

        LOADED_FILES[filename] = parsed

    return LOADED_FILES[filename]


def _get_parsed_spec(filename):
    """
    Returns an OpenAPI object loaded from a file in the tests/fixtures directory

    :param filename: The filename to load.  Must exist in tests/fixtures and
                     include extension.
    :type filename: str
    """
    if "spec:" + filename not in LOADED_FILES:
        parsed = _get_parsed_yaml(filename)

        spec = OpenAPI(parsed)

        LOADED_FILES["spec:" + filename] = spec

    return LOADED_FILES["spec:" + filename]


@pytest.fixture
def petstore_expanded():
    """
    Provides the petstore-expanded.yaml spec
    """
    return _get_parsed_yaml("petstore-expanded.yaml")


@pytest.fixture
def petstore_expanded_spec():
    """
    Provides an OpenAPI version of the petstore-expanded.yaml spec
    """
    return _get_parsed_spec("petstore-expanded.yaml")


@pytest.fixture
def broken():
    """
    Provides the parsed yaml for a broken spec
    """
    return _get_parsed_yaml("broken.yaml")


@pytest.fixture
def broken_reference():
    """
    Provides the parsed yaml for a spec with a broken reference
    """
    return _get_parsed_yaml("broken-ref.yaml")


def has_bad_parameter_name():
    """
    Provides the parsed yaml for a spec with a bad parameter name
    """
    yield _get_parsed_yaml("bad-parameter-name.yaml")


@pytest.fixture
def dupe_op_id():
    """
    A spec with a duplicate operation ID
    """
    return _get_parsed_yaml("dupe-operation-ids.yaml")


@pytest.fixture
def parameter_with_underscores():
    """
    A valid spec with underscores in a path parameter
    """
    return _get_parsed_yaml("parameter-with-underscores.yaml")


@pytest.fixture
def obj_example_expanded():
    """
    Provides the obj-example.yaml spec
    """
    return _get_parsed_yaml("obj-example.yaml")


@pytest.fixture
def float_validation_expanded():
    """
    Provides the float-validation.yaml spec
    """
    return _get_parsed_yaml("float-validation.yaml")


@pytest.fixture
def has_bad_parameter_name():
    """
    Provides a spec with a bad parameter name
    """
    return _get_parsed_yaml("bad-parameter-name.yaml")


@pytest.fixture
def with_links():
    """
    Provides a spec with links defined
    """
    return _get_parsed_yaml("with-links.yaml")


@pytest.fixture
def with_broken_links():
    """
    Provides a spec with broken links defined
    """
    return _get_parsed_yaml("with-broken-links.yaml")


@pytest.fixture
def with_param_types():
    """
    Provides a spec with multiple parameter types and typed examples
    """
    # JSON file to allow specific typing of bool example (bool is a subclass of int in Python)
    return _get_parsed_yaml("parameter-types.json")


@pytest.fixture
def with_securityparameters():
    """
    Provides a spec with security parameters
    """
    return _get_parsed_yaml("with-securityparameters.yaml")


@pytest.fixture
def with_nested_allof_ref():
    """
    Provides a spec with a $ref under a schema defined in an allOf
    """
    return _get_parsed_yaml("nested-allOf.yaml")


@pytest.fixture
def with_ref_allof():
    """
    Provides a spec that includes a reference to a component schema in and out of
    an allOf
    """
    return _get_parsed_yaml("ref-allof.yaml")


@pytest.fixture
def schema_without_properties():
    """
    Provides a spec that includes a schema with no properties defined
    """
    return _get_parsed_yaml("schema-without-properties.yaml")


@pytest.fixture
def rfc_6901():
    """
    Provides a spec that includes RFC 6901 escape codes in ref paths
    """
    return _get_parsed_yaml("rfc_6901.yaml")


@pytest.fixture
def with_array_example():
    """
    Provides a spec that includes arrays as the value of examples
    """
    return _get_parsed_yaml("example_array.yaml")


@pytest.fixture
def empty_contact():
    """
    Provides a spec with an empty contact section in info
    """
    return _get_parsed_yaml("empty_contact.yaml")


@pytest.fixture
def with_external_docs():
    """
    Provides a spec with externalDocs objects in all valid places
    """
    return _get_parsed_yaml("with-external-docs.yaml")


@pytest.fixture
def with_openapi_310_references():
    """
    Provides a spec with OpenAPI 3.1.0 expanded Reference Objects
    """
    return _get_parsed_yaml("openapi-3.1.0-refs.yaml")


@pytest.fixture
def with_reference_referencing_reference():
    """
    Provides a spec with a reference that references a reference
    """
    return _get_parsed_yaml("reference-reference-reference.yaml")


@pytest.fixture
def with_all_default_types():
    """
    Provides a spec with defaults defined in various schemas of all types
    """
    return _get_parsed_yaml("with_all_default_types.yaml")


@pytest.fixture
def with_merge_extension():
    """
    Provides a spec that merges extensions from a component ref.
    """
    return _get_parsed_yaml("merge-extension.yaml")


@pytest.fixture
def with_deeply_nested_allof():
    """
    Provides a spec with a $ref under a schema defined in an allOf
    """
    return _get_parsed_yaml("deeply-nested-allOf.yaml")
