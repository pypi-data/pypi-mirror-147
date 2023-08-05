import subprocess
from .context import BaseContext


class BaseTask:
    name = None
    description = None
    version = None
    ctx: BaseContext = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        if self.ctx is None:
            self.ctx = self._get_ctx()

        if "input" in kwargs:
            self.set_input(kwargs["input"])

    def set_input(self, input):
        if hasattr(self, "Input") and type(input) == dict:
            input = self.__class__.Input(**input)
        self.ctx.set_input(input)

    def _get_ctx(self) -> BaseContext:
        return BaseContext()

    def run(self):
        raise NotImplementedError()


class CommandTask(BaseTask):
    command = None
    args = None

    def run(self, input=None):
        if not input:
            input = []
        elif type(input) is str:
            input = [input]
        else:
            raise Exception("input must be str or list")
        args = [self.command]
        if self.args:
            args.extend(self.args)
        args.extend(input)

        rst = subprocess.run(args, capture_output=True)
        if rst.returncode != 0:
            raise Exception(rst.stderr.decode("utf-8"))

        self.ctx.output = rst.stdout.decode("utf-8")
