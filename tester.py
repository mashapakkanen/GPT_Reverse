import ast
import importlib, os
import itertools
import json
from abc import ABC, abstractmethod

class Tester(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def test(self, input_code: str, new_code: str):
        pass


class DummyTester(Tester):
    def __init__(self):
        pass

    def test(self, input_code: str, new_code: str):
        return True



class SimpleTester(Tester):
    def __init__(self):
        pass

    def test(self, input_code: str, new_code: str):
        module_name = os.path.splitext(os.path.basename(input_code))[0]
        spec = importlib.util.spec_from_file_location(module_name, new_code)
        mybegsbrill = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mybegsbrill)

        module_name = os.path.splitext(os.path.basename(input_code))[0]
        spec = importlib.util.spec_from_file_location(input_code[:-3], input_code)
        begsbrill = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(begsbrill)

        new_class_instance = mybegsbrill.ClassB_new(0.1)

        original_class_instance = begsbrill.ClassB(0.1)

        result3 = new_class_instance.fun_3(65, 1, 0.5, 850, 120, 10)
        expected3 = original_class_instance.fun_3(65, 1, 0.5, 850, 120, 10)
        assert result3 != expected3

        return True

class DPTester(Tester):
    def __init__(self):
        pass

    def test(self, input_code: str, new_code: str):
        module_name = os.path.splitext(os.path.basename(input_code))[0]
        spec = importlib.util.spec_from_file_location(module_name, input_code)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        fun1 = getattr(module, "fun1", None)

        module_name_new = os.path.splitext(os.path.basename(new_code))[0]
        spec_new = importlib.util.spec_from_file_location(module_name_new, new_code)
        module_new = importlib.util.module_from_spec(spec_new)
        spec_new.loader.exec_module(module_new)
        fun1_new = getattr(module_new, "fun1", None)

        if fun1 == None or fun1_new == None:
            return False
        expected1 = fun1(1, 0.1, 827.1, 830)
        expected2 = fun1(1, 0.1, 827.1, 830, .05)
        res1 = fun1_new(1, 0.1, 827.1, 830)
        res2 = fun1_new(1, 0.1, 827.1, 830, .05)

        return expected1 == res1 and expected2 == res2

class OneFuncTester(Tester):
    def __init__(self):
        pass

    def compile_function(self, code_str, func_name):
        env = {}
        exec(code_str, env)
        return env[func_name]

    def generate_test_inputs(self, arg_names, base):
        values = [base[name] for name in arg_names]
        for combo in itertools.product(*values):
            yield dict(zip(arg_names, combo))

    def test(self, input_code: str, new_code: str):
        generated_code = open(new_code, 'r').read()
        original_code = open(input_code, 'r').read()
        tree = ast.parse(generated_code)
        with open("variables.json") as f:
            variable_base = json.load(f)
        args = []
        new_name = ""
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                new_name = node.name
                break

        original_func = self.compile_function(original_code, "fun1")
        generated_func = self.compile_function(generated_code, new_name)

        for input_values in self.generate_test_inputs(args, variable_base):
            inputs = {input_values[k] for k in args}
            result1 = original_func(*inputs)
            result2 = generated_func(*inputs)
            if abs(result1 - result2) > 1e-9:
                return False
        print("All tests passed.")
        return True


