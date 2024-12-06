import dataclasses

from giotto_llm.consts import C0, C1, C2, C3, C4, C5, C6, C7, C8, C9
from giotto_llm.prompts.grid_formatter import GridFormatter
from giotto_llm.type_aliases import JSONTask, Messages


@dataclasses.dataclass(slots=True, kw_only=True, frozen=True)
class TextPromptBase:
    """Base class of all prompt generation classes."""

    grid_formatter: GridFormatter = dataclasses.field(default_factory=GridFormatter)

    def generate_system(self) -> str:
        """Note: redefine this metdhod in children classes"""
        raise NotImplementedError

    def generate_user(self, task: JSONTask, idx_i: int) -> str:
        """Note: redefine this metdhod in children classes"""
        raise NotImplementedError

    def generate_assistant(self, task: JSONTask, idx_i: int) -> str:
        """Note: redefine this metdhod in children classes"""
        raise NotImplementedError

    def __call__(self, task: JSONTask, idx_i: int) -> Messages:
        """Create a sequence of messages used to fine-tune a tranformer on ARC task."""
        return [
            {"role": "system", "content": self.generate_system()},
            {"role": "user", "content": self.generate_user(task, idx_i)},
            {"role": "assistant", "content": self.generate_assistant(task, idx_i)},
        ]


@dataclasses.dataclass(slots=True, kw_only=True, frozen=True)
class PromptSolveShort(TextPromptBase):
    """A short prompt format containing only input and output grids."""

    def generate_system(self) -> str:
        return ""

    def generate_user(self, task: JSONTask, idx_i: int) -> str:
        encoded_input_grid = self.grid_formatter.encode_grid(
            task["test"][idx_i]["input"], input_or_output="input"
        )
        return f"""{self.grid_formatter.encode_pairs(task['train'])}

{encoded_input_grid}

"""

    def generate_assistant(self, task: JSONTask, idx_i: int) -> str:
        if "output" in task["test"][idx_i]:
            encoded_output_grid = self.grid_formatter.encode_grid(
                grid=task["test"][idx_i]["output"], input_or_output="output"
            )
        else:
            encoded_output_grid = ""

        return encoded_output_grid


@dataclasses.dataclass(slots=True, kw_only=True, frozen=True)
class PromptSolveInstrV1(TextPromptBase):
    """A general instruction prompt format with information about ARC priors."""

    def generate_system(self) -> str:
        return f"""You are a helpful AI assistant. Your job is to solve tasks from the Abstraction and Reasoning Challenge (ARC).
The user will present you with sample input and output Grids for each task.
Your job will be to understand the transformation between the input and the output and apply it to the last input Grid given by the user.
The puzzle-like inputs and outputs present a grid where each square can be one of ten colors. A Grid can be any height or width between 1x1 and 30x30.
The background of the Grid is typically colored with {C0}.
The tasks from ARC are based on the following priors:

- Objectness: Objects persist and cannot appear or disappear without reason. Objects can interact or not depending on the circumstances.
- Goal-directed: Objects can be animate or inanimate. Some objects are "agents" - they have intentions and they pursue goals.
- Numbers & counting: Objects can be counted or sorted by their shape, appearance, or movement using basic mathematics like addition, subtraction, and comparison.
- Basic geometry & topology: Objects can be shapes like rectangles, triangles, and circles which can be mirrored, rotated, translated, deformed, combined, repeated, etc. Differences in distances can be detected.

The transformations between input and output should be based on these priors.

"""

    def generate_user(self, task: JSONTask, idx_i: int) -> str:
        encoded_input_grid = self.grid_formatter.encode_grid(
            task["test"][idx_i]["input"], input_or_output="input"
        )
        return f"""{self.grid_formatter.encode_pairs(task['train'])}

From the input test Grid above, predict the output Grid using the same rules and transformations found in the Example Grid pairs.
Reply just with the solution Grid.
DO NOT print any text, code, instructions, or anything else that is not the solution Grid.

{encoded_input_grid}
"""

    def generate_assistant(self, task: JSONTask, idx_i: int) -> str:
        if "output" in task["test"][idx_i]:
            encoded_output_grid = self.grid_formatter.encode_grid(
                grid=task["test"][idx_i]["output"], input_or_output="output"
            )
        else:
            encoded_output_grid = ""

        return encoded_output_grid


@dataclasses.dataclass(slots=True, kw_only=True, frozen=True)
class PromptSolveInstrV2(TextPromptBase):
    """A general instruction prompt format with information about ARC priors."""

    def generate_system(self) -> str:
        return f"""You are a puzzle solving wizard. You are given a puzzle from the abstraction and reasoning corpus developed by Francois Chollet.
The puzzle-like Inputs and Output pairs present a Grid where each Element is one of
- {C0}
- {C1}
- {C2}
- {C3}
- {C4}
- {C5}
- {C6}
- {C7}
- {C8}
- {C9}

"""

    def generate_user(self, task: JSONTask, idx_i: int) -> str:
        encoded_input_grid = self.grid_formatter.encode_grid(
            task["test"][idx_i]["input"], input_or_output="input"
        )
        return f"""The training data is:
{self.grid_formatter.encode_pairs(task['train'])}

Now, solve the following puzzle based on its input grid by applying the rules you have learned from the training data:
{encoded_input_grid}

What is the output grid?
Only provide the output grid in the form as in the example input and output pairs.
Do not provide any additional information:
"""

    def generate_assistant(self, task: JSONTask, idx_i: int) -> str:
        if "output" in task["test"][idx_i]:
            encoded_output_grid = self.grid_formatter.encode_grid(
                grid=task["test"][idx_i]["output"], input_or_output="output"
            )
        else:
            encoded_output_grid = ""

        return encoded_output_grid
