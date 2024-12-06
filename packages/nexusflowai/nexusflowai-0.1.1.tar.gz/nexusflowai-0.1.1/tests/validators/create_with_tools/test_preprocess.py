from nexusflowai.validators.create_with_tools.preprocess import (
    RavenFunctionReturn,
    RavenFunctionParameter,
    RavenType,
)


class TestRavenFunctionReturnUnit:
    def test_return_format_for_prompt_definition(self) -> None:
        no_schema_return = RavenFunctionReturn(schema=None)
        assert no_schema_return.format_for_prompt_definition() is None

        bool_schema_return = RavenFunctionReturn(schema=True)
        assert bool_schema_return.format_for_prompt_definition() is None

        object_type_return = RavenFunctionReturn(
            schema={
                "type": {
                    "string": 2,
                }
            },
        )
        assert object_type_return.format_for_prompt_definition() is None

        invalid_type_return = RavenFunctionReturn(
            schema={"type": "invalid"},
        )
        assert invalid_type_return.format_for_prompt_definition() is None

        unknown_types_return = RavenFunctionReturn(
            schema={"type": ["unknown_type1", "unknown_type2"]},
        )
        assert unknown_types_return.format_for_prompt_definition() is None

        single_type_return = RavenFunctionReturn(
            schema={"type": "number"},
        )
        assert single_type_return.format_for_prompt_definition() == "float"

        multiple_types_return = RavenFunctionReturn(
            schema={"type": ["string", "integer"]},
        )
        assert multiple_types_return.format_for_prompt_definition() == "Union[str, int]"


class TestRavenFunctionParameterUnit:
    def test_parameter_format_for_prompt_definition(self) -> None:
        no_schema_parameter = RavenFunctionParameter(name="no_schema", schema=None)
        assert no_schema_parameter.format_for_prompt_definition() == "no_schema"

        bool_schema_parameter = RavenFunctionParameter(name="bool_schema", schema=True)
        assert bool_schema_parameter.format_for_prompt_definition() == "bool_schema"

        object_type_parameter = RavenFunctionParameter(
            name="object_type",
            schema={
                "type": {
                    "string": 2,
                }
            },
        )
        assert object_type_parameter.format_for_prompt_definition() == "object_type"

        invalid_type_parameter = RavenFunctionParameter(
            name="invalid_type",
            schema={"type": "invalid"},
        )
        assert invalid_type_parameter.format_for_prompt_definition() == "invalid_type"

        unknown_types_parameter = RavenFunctionParameter(
            name="unknown_types",
            schema={"type": ["unknown_type1", "unknown_type2"]},
        )
        assert unknown_types_parameter.format_for_prompt_definition() == "unknown_types"

        single_type_parameter = RavenFunctionParameter(
            name="single_type",
            schema={"type": "number"},
        )
        assert (
            single_type_parameter.format_for_prompt_definition() == "single_type: float"
        )

        multiple_types_parameter = RavenFunctionParameter(
            name="multiple_types",
            schema={"type": ["string", "integer"]},
        )
        assert (
            multiple_types_parameter.format_for_prompt_definition()
            == "multiple_types: Union[str, int]"
        )

    def test_parameter_format_for_prompt_docstring(self) -> None:
        no_schema_parameter = RavenFunctionParameter(name="no_schema", schema=None)
        assert no_schema_parameter.format_for_prompt_docstring() is None

        bool_schema_parameter = RavenFunctionParameter(name="bool_schema", schema=True)
        assert bool_schema_parameter.format_for_prompt_docstring() is None

        object_type_parameter = RavenFunctionParameter(
            name="object_type",
            schema={
                "type": {
                    "string": 2,
                }
            },
        )
        assert object_type_parameter.format_for_prompt_docstring() is None

        invalid_type_parameter = RavenFunctionParameter(
            name="invalid_type",
            schema={"type": "invalid"},
        )
        assert invalid_type_parameter.format_for_prompt_docstring() == "- invalid_type"

        unknown_types_parameter = RavenFunctionParameter(
            name="unknown_types",
            schema={"type": ["unknown_type1", "unknown_type2"]},
        )
        assert (
            unknown_types_parameter.format_for_prompt_docstring() == "- unknown_types"
        )

        single_type_parameter = RavenFunctionParameter(
            name="single_type",
            schema={
                "type": "number",
                "description": "hello world",
            },
        )
        assert (
            single_type_parameter.format_for_prompt_docstring()
            == "- single_type (float): Hello world."
        )

        multiple_types_parameter = RavenFunctionParameter(
            name="multiple_types",
            schema={
                "type": ["string", "integer"],
                "description": "hello world",
            },
        )
        assert (
            multiple_types_parameter.format_for_prompt_docstring()
            == "- multiple_types (Union[str, int]): Hello world."
        )

        array_type_parameter = RavenFunctionParameter(
            name="array_type",
            schema={
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "Hello world.",
                },
            },
        )
        assert (
            array_type_parameter.format_for_prompt_docstring()
            == "- array_type (List[str]): Hello world."
        )


class TestRavenTypeUnit:
    def test_format_type_for_prompt(self) -> None:
        assert RavenType.format_type_for_prompt("string") == "str"
        assert RavenType.format_type_for_prompt("number") == "float"
        assert RavenType.format_type_for_prompt("integer") == "int"
        assert RavenType.format_type_for_prompt("object") == "object"
        assert RavenType.format_type_for_prompt("array") == "list"
        assert RavenType.format_type_for_prompt("boolean") == "bool"
        assert RavenType.format_type_for_prompt("null") == "None"
        assert RavenType.format_type_for_prompt("unknown") is None

        assert RavenType.format_type_for_prompt("array", {}) == "list"
        assert (
            RavenType.format_type_for_prompt(
                "array",
                {"items": "string"},
            )
            == "list"
        )
        assert (
            RavenType.format_type_for_prompt(
                "array",
                {"items": {}},
            )
            == "list"
        )
        assert (
            RavenType.format_type_for_prompt(
                "array",
                {
                    "items": {
                        "type": "inner",
                    }
                },
            )
            == "list"
        )
        assert (
            RavenType.format_type_for_prompt(
                "array",
                {
                    "items": {
                        "type": "string",
                    }
                },
            )
            == "List[str]"
        )
        assert (
            RavenType.format_type_for_prompt(
                "array",
                {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "integer",
                        },
                    }
                },
            )
            == "List[List[int]]"
        )

        assert RavenType.format_type_for_prompt([]) is None
        assert RavenType.format_type_for_prompt(["random"]) is None
        assert RavenType.format_type_for_prompt(["string"]) == "str"
        assert RavenType.format_type_for_prompt(["integer", "extra"]) == "int"
        assert (
            RavenType.format_type_for_prompt(["boolean", "number"])
            == "Union[bool, float]"
        )
        assert (
            RavenType.format_type_for_prompt(["object", "array", "object", "null"])
            == "Union[object, list, None]"
        )
        assert (
            RavenType.format_type_for_prompt(["string", "integer", 3, "boolean"])
            == "Union[str, int, bool]"
        )
