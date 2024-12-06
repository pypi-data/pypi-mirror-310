from typing import Any, Dict, List, Optional, Union

from enum import Enum

import json

from pydantic import BaseModel

from nexusflowai.validators.json_schema_to_dataclasses import (
    try_convert_to_dataclasses_str,
)

from nexusflowai.validators.create_with_tools.postprocess import (
    ResponseFormatTranslator,
)


class TestResponseFormatTranslator:
    def test_response_format_openai_examples(self) -> None:
        """
        Examples from https://platform.openai.com/docs/guides/structured-outputs/examples
        """

        def helper(
            response_format: Union[BaseModel, Dict[str, Any]],
            expected_output: Dict[str, Any],
            mock_raven_response: str,
        ) -> None:
            json_schema_str, _ = try_convert_to_dataclasses_str(response_format)
            json_schema = json.loads(json_schema_str)

            rft = ResponseFormatTranslator()
            actual_output = rft.raw_response_to_parsed(json_schema, mock_raven_response)
            assert expected_output == actual_output

        expected_output = {
            "steps": [
                {
                    "explanation": "Start with the equation 8x + 7 = -23.",
                    "output": "8x + 7 = -23",
                },
                {
                    "explanation": "Subtract 7 from both sides to isolate the term with the variable.",
                    "output": "8x = -23 - 7",
                },
                {
                    "explanation": "Simplify the right side of the equation.",
                    "output": "8x = -30",
                },
                {
                    "explanation": "Divide both sides by 8 to solve for x.",
                    "output": "x = -30 / 8",
                },
                {"explanation": "Simplify the fraction.", "output": "x = -15 / 4"},
            ],
            "final_answer": "x = -15 / 4",
        }

        mock_raven_response = """extract_item(value=MathReasoning(steps=[Step(explanation='Start with the equation 8x + 7 = -23.', output='8x + 7 = -23'), Step(explanation='Subtract 7 from both sides to isolate the term with the variable.', output='8x = -23 - 7'), Step(explanation='Simplify the right side of the equation.', output='8x = -30'), Step(explanation='Divide both sides by 8 to solve for x.', output='x = -30 / 8'), Step(explanation='Simplify the fraction.', output='x = -15 / 4')], final_answer='x = -15 / 4'))"""

        class Step(BaseModel):
            explanation: str
            output: str

        class MathReasoning(BaseModel):
            steps: list[Step]
            final_answer: str

        helper(
            response_format=MathReasoning,
            expected_output=expected_output,
            mock_raven_response=mock_raven_response,
        )

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "math_reasoning",
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "explanation": {"type": "string"},
                                    "output": {"type": "string"},
                                },
                                "required": ["explanation", "output"],
                                "additionalProperties": False,
                            },
                        },
                        "final_answer": {"type": "string"},
                    },
                    "required": ["steps", "final_answer"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }
        helper(
            response_format=response_format,
            expected_output=expected_output,
            mock_raven_response=mock_raven_response,
        )

        expected_output = {
            "title": "Application of Quantum Algorithms in Interstellar Navigation: A New Frontier",
            "authors": ["Dr. Stella Voyager", "Dr. Nova Star", "Dr. Lyra Hunter"],
            "abstract": "This paper investigates the utilization of quantum algorithms to improve interstellar navigation systems. By leveraging quantum superposition and entanglement, our proposed navigation system can calculate optimal travel paths through space-time anomalies more efficiently than classical methods. Experimental simulations suggest a significant reduction in travel time and fuel consumption for interstellar missions.",
            "keywords": [
                "Quantum algorithms",
                "interstellar navigation",
                "space-time anomalies",
                "quantum superposition",
                "quantum entanglement",
                "space travel",
            ],
        }

        mock_raven_response = """extract_item(value=ResearchPaperExtraction(title='Application of Quantum Algorithms in Interstellar Navigation: A New Frontier', authors=['Dr. Stella Voyager', 'Dr. Nova Star', 'Dr. Lyra Hunter'], abstract='This paper investigates the utilization of quantum algorithms to improve interstellar navigation systems. By leveraging quantum superposition and entanglement, our proposed navigation system can calculate optimal travel paths through space-time anomalies more efficiently than classical methods. Experimental simulations suggest a significant reduction in travel time and fuel consumption for interstellar missions.', keywords=['Quantum algorithms', 'interstellar navigation', 'space-time anomalies', 'quantum superposition', 'quantum entanglement', 'space travel']))"""

        class ResearchPaperExtraction(BaseModel):
            title: str
            authors: List[str]
            abstract: str
            keywords: List[str]

        helper(
            response_format=ResearchPaperExtraction,
            expected_output=expected_output,
            mock_raven_response=mock_raven_response,
        )

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "research_paper_extraction",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "authors": {"type": "array", "items": {"type": "string"}},
                        "abstract": {"type": "string"},
                        "keywords": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["title", "authors", "abstract", "keywords"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }
        helper(
            response_format=response_format,
            expected_output=expected_output,
            mock_raven_response=mock_raven_response,
        )

        expected_output = {
            "type": "form",
            "label": "User Profile Form",
            "children": [
                {
                    "type": "div",
                    "label": "",
                    "children": [
                        {
                            "type": "field",
                            "label": "First Name",
                            "children": [],
                            "attributes": [
                                {"name": "type", "value": "text"},
                                {"name": "name", "value": "firstName"},
                                {
                                    "name": "placeholder",
                                    "value": "Enter your first name",
                                },
                            ],
                        },
                        {
                            "type": "field",
                            "label": "Last Name",
                            "children": [],
                            "attributes": [
                                {"name": "type", "value": "text"},
                                {"name": "name", "value": "lastName"},
                                {
                                    "name": "placeholder",
                                    "value": "Enter your last name",
                                },
                            ],
                        },
                    ],
                    "attributes": [],
                },
                {
                    "type": "button",
                    "label": "Submit",
                    "children": [],
                    "attributes": [{"name": "type", "value": "submit"}],
                },
            ],
            "attributes": [
                {"name": "method", "value": "post"},
                {"name": "action", "value": "/submit-profile"},
            ],
        }

        mock_raven_response = """extract_item(value=UI(type='form', label='User Profile Form', children=[UI(type='div', label='', children=[UI(type='field', label='First Name', children=[], attributes=[Attribute(name='type', value='text'), Attribute(name='name', value='firstName'), Attribute(name='placeholder', value='Enter your first name')]), UI(type='field', label='Last Name', children=[], attributes=[Attribute(name='type', value='text'), Attribute(name='name', value='lastName'), Attribute(name='placeholder', value='Enter your last name')])], attributes=[]), UI(type='button', label='Submit', children=[], attributes=[Attribute(name='type', value='submit')])], attributes=[Attribute(name='method', value='post'), Attribute(name='action', value='/submit-profile')]))"""

        class UIType(str, Enum):
            div = "div"
            button = "button"
            header = "header"
            section = "section"
            field = "field"
            form = "form"

        class Attribute(BaseModel):
            name: str
            value: str

        class UI(BaseModel):
            type: UIType
            label: str
            children: List["UI"]
            attributes: List[Attribute]

        UI.model_rebuild()  # This is required to enable recursive types

        helper(
            response_format=UI,
            expected_output=expected_output,
            mock_raven_response=mock_raven_response,
        )

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "UI",
                "description": "Dynamically generated UI",
                "schema": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "description": "The type of the UI component",
                            "enum": [
                                "div",
                                "button",
                                "header",
                                "section",
                                "field",
                                "form",
                            ],
                        },
                        "label": {
                            "type": "string",
                            "description": "The label of the UI component, used for buttons or form fields",
                        },
                        "children": {
                            "type": "array",
                            "description": "Nested UI components",
                            "items": {"$ref": "#"},
                        },
                        "attributes": {
                            "type": "array",
                            "description": "Arbitrary attributes for the UI component, suitable for any element",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the attribute, for example onClick or className",
                                    },
                                    "value": {
                                        "type": "string",
                                        "description": "The value of the attribute",
                                    },
                                },
                                "required": ["name", "value"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["type", "label", "children", "attributes"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }
        helper(
            response_format=response_format,
            expected_output=expected_output,
            mock_raven_response=mock_raven_response,
        )

        expected_output = {
            "is_violating": False,
            "category": None,
            "explanation_if_violating": None,
        }

        mock_raven_response = """extract_item(value=ContentCompliance(is_violating=False, category=None, explanation_if_violating=None))"""

        class Category(str, Enum):
            violence = "violence"
            sexual = "sexual"
            self_harm = "self_harm"

        class ContentCompliance(BaseModel):
            is_violating: bool
            category: Optional[Category]
            explanation_if_violating: Optional[str]

        helper(
            response_format=ContentCompliance,
            expected_output=expected_output,
            mock_raven_response=mock_raven_response,
        )

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "content_compliance",
                "description": "Determines if content is violating specific moderation rules",
                "schema": {
                    "type": "object",
                    "properties": {
                        "is_violating": {
                            "type": "boolean",
                            "description": "Indicates if the content is violating guidelines",
                        },
                        "category": {
                            "type": ["string", "null"],
                            "description": "Type of violation, if the content is violating guidelines. Null otherwise.",
                            "enum": ["violence", "sexual", "self_harm"],
                        },
                        "explanation_if_violating": {
                            "type": ["string", "null"],
                            "description": "Explanation of why the content is violating",
                        },
                    },
                    "required": [
                        "is_violating",
                        "category",
                        "explanation_if_violating",
                    ],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }
        helper(
            response_format=response_format,
            expected_output=expected_output,
            mock_raven_response=mock_raven_response,
        )
