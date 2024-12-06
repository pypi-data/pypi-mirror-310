from typing import List, Callable

from stringflow import StringFlow as SF
from botchain.utils import function_to_model
from botchain.attachment import Attachment


class Bot:
    def __init__(
        self,
        name: str,
        system: str,
        tools: List[Callable],
        doc: str = None,
        sf: SF = None,
        log_level: int = 0,
        use_rich_print: bool = True,
    ):
        self.name = name
        self.system = system

        self.tools = tools or []
        self.tools = {tool.__name__: tool for tool in self.tools}

        self.__doc__ = doc or f"A bot following system:\n\n{self.system}."

        self.sf = sf or SF(
            provider="openai",
            model="gpt-4o-mini",
            log_level=log_level,
            use_rich_print=use_rich_print,
        )

        if use_rich_print:
            from rich import print

        self.log = lambda x: print(x) if log_level > 0 else None

        self.log(
            f"AC: name={self.name}, system={self.system}, tools={self.tools}, doc={self.__doc__}, sf={self.sf.rest.base_url}"
        )

    def planner(self, message: str) -> str:
        self.log(f"AC.planner: message={message}")

        options = list(self.tools)
        self.log(f"AC.planner: options={options}")

        system = f"{self.system}\n\nPlease choose a tool to assist the user."
        message = f"{message}"
        self.log(f"AC.planner: system={system}, message={message}")

        if len(options) == 1:
            choice = options[0]
        else:
            choice = self.sf.choose(
                message=message,
                system=system,
                options=options,
                allow_none=False,
            )
        self.log(f"AC.planner: choice={choice}")

        return choice

    def __call__(self, message: str, **kwargs) -> str:
        self.log(f"AC: message={message}")

        tool_name = self.planner(message)
        self.log(f"AC: tool_name={tool_name}")

        tool = self.tools[tool_name]
        self.log(f"AC: tool={tool}")

        tool_model = function_to_model(tool)
        self.log(f"AC: tool_model={tool_model}")

        system = f"{self.system}\n\nYou are using tool '{tool_name}'."
        system += (
            "You must cast the user's message into the tool's expected input format."
        )
        system += f"Ensure your response is in the format: {tool_model.schema()}"
        self.log(f"AC: system={system}")

        message = f"The user has asked:\n\n{message}"
        self.log(f"AC: message={message}")

        params = self.sf.cast(message=message, system=system, model_class=tool_model)
        self.log(f"AC: params={params}")
        self.log(f"AC: param types={[type(param) for param in params]}")

        message = tool(**{k: v for k, v in params})
        self.log(f"AC: message={message}")

        # TODO: hack
        if isinstance(message, Attachment):
            return message

        message = (
            f"I have used tool '{tool_name}' with {params} resulting in:\n\n{message}"
        )
        self.log(f"AC: message={message}")

        return message

    def __str__(self):
        return self.__doc__
