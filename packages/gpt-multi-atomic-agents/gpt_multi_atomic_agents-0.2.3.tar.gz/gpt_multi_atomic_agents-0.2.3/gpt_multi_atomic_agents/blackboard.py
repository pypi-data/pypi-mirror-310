from dataclasses import dataclass, field
import logging

from .functions_dto import FunctionCallSchema
from . import util_graphql

logger = logging.getLogger("blackboard")


@dataclass
class Blackboard:
    # TODO try split this blackboard, have a base class
    previously_generated_functions: list[FunctionCallSchema] = field(
        default_factory=list
    )
    previously_generated_mutation_calls: list[str] = field(default_factory=list)

    def add_generated_functions(
        self, generated_function_calls: list[FunctionCallSchema]
    ) -> None:
        self.previously_generated_functions += generated_function_calls

    def get_generated_functions_matching(
        self, function_names: list[str]
    ) -> list[FunctionCallSchema]:
        return list(
            filter(
                lambda f: f.function_name in function_names,
                self.previously_generated_functions,
            )
        )

    def add_generated_mutations(self, generated_mutation_calls: list[str]) -> None:
        self.previously_generated_mutation_calls += generated_mutation_calls

    def get_generated_mutations_matching(
        self, accepted_graphql_schemas: list[str]
    ) -> list[str]:
        accepted_mutation_names = util_graphql.parse_out_mutation_names_from_schemas(
            accepted_graphql_schemas
        )

        return util_graphql.filter_to_matching_mutation_calls(
            self.previously_generated_mutation_calls, accepted_mutation_names
        )
