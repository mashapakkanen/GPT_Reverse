from model import Model, DummyModel
from tester import Tester, DummyTester


class Process:
    def __init__(self, input_file: str, output_file: str,
                 model: Model, tester: Tester):
        self.input_file = input_file
        self.output_file = output_file
        self.model = model
        self.tester = tester

    def process(self):
        with open(self.input_file, "r") as f:
            code_lines = f.readlines()
        code = "".join(code_lines)
        newcode = self.model.run(code)
        print(newcode)
        with open(self.output_file, "w") as f:
            f.write(newcode)
        self.tester.test(self.input_file, self.output_file)
        