import importlib
from abc import ABC, abstractmethod

import pytest
from begsbrill_implicit import ClassA

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
        # Save the input code to a file
        #with open('begsbrill_implicit.py', 'w') as f:
        #    f.write(input_code)

        # Save the new code to a file
        #with open('mybegsbrill.py', 'w') as f:
        #    f.write(new_code)

        # Dynamically import the new module
        spec = importlib.util.spec_from_file_location("mybegsbrill", "mybegsbrill.py")
        mybegsbrill = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mybegsbrill)

        # Create an instance of the class from the new module
        new_class_instance = mybegsbrill.HydraulicSystem(0.1)

        # Create an instance of the original class
        original_class_instance = ClassA(0.1)

        # Compare the results of the functions
        result1 = new_class_instance._determine_flow_regime(65, 1)
        expected1 = original_class_instance.fun_1(65, 1)
        assert result1 == pytest.approx(expected1)

        result3 = new_class_instance.update_flow_parameters(65, 1, 0.5, 850, 120, 10)
        expected3 = original_class_instance.fun_3(65, 1, 0.5, 850, 120, 10)
        assert result3 == expected3

        return True