from model import Model, DummyModel
from tester import Tester, DummyTester


class Process:
    def __init__(self, input_file: str, output_file: str,
                 model: Model, tester: Tester):
        self.input_file = input_file
        self.output_file = output_file
        self.model = model
        self.tester = tester

    def process(self, times=5):
        with open(self.input_file, "r") as f:
            code_lines = f.readlines()
        code = "".join(code_lines)
        for i in range(times):
            newcode = self.model.run(code)
            if newcode.startswith("```python"):
                newcode = newcode[10:-3]
            with open(self.output_file, "w") as f:
                f.write(newcode)
            if self.tester.test(self.input_file, self.output_file):
                print("Success: The new code is correct.")
                return


        