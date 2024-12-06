import logging
import typing

from atomic_agents.agents.base_agent import (
    BaseAgent,
    BaseAgentConfig,
    BaseIOSchema,
)

from rich.console import Console
from rich.text import Text

from . import util_ai, prompts_router, config
from .agent_definition import (
    AgentDefinitionBase,
    FunctionAgentDefinition,
    GraphQLAgentDefinition,
)
from .blackboard import Blackboard
from .config import Config
from .functions_dto import FunctionAgentOutputSchema
from .graphql_dto import GraphQLAgentOutputSchema

console = Console()

logger = logging.getLogger("main_service")


# TODO extract util_agent_print
def _print_agent(
    agent: prompts_router.RecommendedAgent,
    _config: config.Config,
    max_prompt_out_len: int = 100,
    prefix="",
) -> None:
    rewritten_user_prompt = (
        agent.rewritten_user_prompt
        if _config.is_debug
        else agent.rewritten_user_prompt[:max_prompt_out_len] + "..."
    )
    console.print(Text(f" {prefix} - [{agent.agent_name}]", style="cyan"))
    console.print(Text(f"  <-- '{rewritten_user_prompt}'", style="blue"))


def _print_router_assistant(
    message: prompts_router.RouterAgentOutputSchema, _config: config.Config
) -> None:
    console.print(
        f":robot: [bold cyan]Assistant [router]: {message.chat_message}[/bold cyan]"
    )
    console.print(Text("  - recommended agents:", style="blue"))
    for agent in message.recommended_agents:
        _print_agent(agent, _config=_config, max_prompt_out_len=50)


def _print_assistant_base(chat_message: str, output: typing.Any, agent_name="general"):
    console.print(
        f":robot: [bold green]Assistant [{agent_name}]: {chat_message}[/bold green]"
    )
    console.print(Text("  New calls:", style="yellow"))
    console.print(output)


def _print_assistant_functions(
    message: FunctionAgentOutputSchema, agent_name="general"
):
    return _print_assistant_base(
        message.chat_message, message.generated_function_calls, agent_name=agent_name
    )


def _print_assistant_graphql(message: GraphQLAgentOutputSchema, agent_name="general"):
    return _print_assistant_base(
        message.chat_message, message.generated_mutations, agent_name=agent_name
    )


def _print_assistant_output(
    response: BaseIOSchema, agent_definition: AgentDefinitionBase
) -> None:
    if isinstance(agent_definition, FunctionAgentDefinition):
        return _print_assistant_functions(response, agent_definition.agent_name)
    elif isinstance(agent_definition, GraphQLAgentDefinition):
        return _print_assistant_graphql(response, agent_definition.agent_name)
    else:
        raise RuntimeError("Not a recognised AgentDefinitionBase")


def _create_agent(agent_definition: AgentDefinitionBase, _config: Config) -> BaseAgent:
    client, model, max_tokens = util_ai.create_client(_config=_config)
    system_prompt_builder = agent_definition.get_system_prompt_builder(_config=_config)

    agent = BaseAgent(
        config=BaseAgentConfig(
            client=client,
            model=model,
            system_prompt_generator=system_prompt_builder.build_system_prompt(),
            input_schema=agent_definition.input_schema,
            output_schema=agent_definition.output_schema,
            max_tokens=max_tokens,
        )
    )
    return agent


def run_chat_loop(
    agent_definitions: list[AgentDefinitionBase],
    chat_agent_description: str,
    _config: Config,
    given_user_prompt: str | None = None,
) -> list:
    if not agent_definitions:
        raise RuntimeError("Expected at least 1 Agent Definition")
    is_function_based = isinstance(agent_definitions[0], FunctionAgentDefinition)

    initial_message = FunctionAgentOutputSchema(
        chat_message="How can I help you?", generated_function_calls=[]
    )

    _print_assistant_functions(initial_message)

    # for more emojis - see "poetry run python -m rich.emoji"
    if given_user_prompt:
        console.print(f":sunglasses: You: {given_user_prompt}")

    blackboard = Blackboard()
    while True:
        user_prompt = (
            given_user_prompt
            if given_user_prompt
            else console.input(":sunglasses: You: ")
        )
        if not user_prompt:
            break

        with console.status("[bold green]Processing...") as _status:
            try:
                console.log("Routing...")
                router_agent = prompts_router.create_router_agent(config=_config)
                response = typing.cast(
                    prompts_router.RouterAgentOutputSchema,
                    router_agent.run(
                        prompts_router.build_input(
                            user_prompt=user_prompt,
                            agents=agent_definitions,
                            chat_agent_description=chat_agent_description,
                        )
                    ),
                )
                recommended_agents = response.recommended_agents

                _print_router_assistant(response, _config=_config)

                # Loop thru all the recommended agents, sending each one a rewritten version of the user prompt
                for recommended_agent in recommended_agents:
                    try:
                        if recommended_agent.agent_name == "chat":
                            # TODO: add a Chat agent - but not really needed
                            continue

                        console.log(
                            f":robot: Executing agent {recommended_agent.agent_name}..."
                        )
                        _print_agent(
                            recommended_agent, _config=_config, prefix="EXECUTING: "
                        )
                        matching_agent_definitions = list(
                            filter(
                                lambda a: a.agent_name == recommended_agent.agent_name,
                                agent_definitions,
                            )
                        )
                        if not matching_agent_definitions:
                            raise RuntimeError(
                                f"Could not match recommended agent {recommended_agent.agent_name}"
                            )
                        if len(matching_agent_definitions) > 1:
                            console.print(
                                f":warning: Matched more than one agent to {recommended_agent.agent_name}"
                            )
                        agent_definition = matching_agent_definitions[0]
                        agent = _create_agent(agent_definition, _config=_config)

                        response = agent.run(
                            agent_definition.build_input(
                                recommended_agent.rewritten_user_prompt,
                                blackboard=blackboard,
                                config=_config,
                            )
                        )
                        _print_assistant_output(response, agent_definition)

                        agent_definition.update_blackboard(
                            response=response, blackboard=blackboard
                        )
                    except Exception as e:
                        logger.exception(e)
            except Exception as e:
                logger.exception(e)

            console.log(":robot: (done)")

        if given_user_prompt:
            break
    return (
        blackboard.previously_generated_functions
        if is_function_based
        else blackboard.previously_generated_mutation_calls
    )


# to debug - see agent.system_prompt_generator.generate_prompt()
