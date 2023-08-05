import argparse
import json
from .display import Display


def get_input():
    return get_input_from_cli()


def get_input_from_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    parser.add_argument("--input-json", type=str)
    args = parser.parse_known_args()[0]

    input_json = getattr(args, "input_json")
    if input_json:
        input_json = json.loads(input_json)
        return input_json

    input_str = getattr(args, "input")
    if input_str:
        return input_str

    return None


class BaseContext:
    input = None
    output = None
    display = None

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        if self.display is None:
            self.display = Display()

        if self.output is None:
            self.output = {}

        if self.input is None:
            input = get_input()
            if input is not None:
                self.set_input(input)

    def set_input(self, input):
        self.input = input

    def get_output(self):
        return self.output
