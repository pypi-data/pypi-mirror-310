"""Decorators for testing"""
import inspect
import re
from functools import wraps
from importlib import util
from typing import Any, Iterable

from dataclasses import dataclass

from .utils import capture_io


@dataclass
class Case:
    function: callable = None
    output: Any = None
    points: float = 1
    exact: bool = True


def add_points(points: float):
    def decorator(test_function: callable):
        setattr(test_function, 'points_increment', points)
        return test_function

    return decorator


def run_solution(inputs: list):
    def decorator(test_function: callable):
        @wraps(test_function)
        def wrapper(class_self):
            from .globals import testing_script_path
            outputs = capture_io(testing_script_path, map(str, inputs))
            outputs = outputs.replace("i", "і")
            return test_function(class_self, outputs)

        return wrapper

    return decorator


def import_solution_module():
    def decorator(test_function: callable):
        @wraps(test_function)
        def wrapper(class_self):
            from .globals import testing_script_path
            spec = util.spec_from_file_location("test.test", testing_script_path)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return test_function(class_self, module)

        return wrapper

    return decorator


def create_function_for_case(name: str, case: Case) -> callable:
    """
    Create test-function for case
    :param case: case of testing
    :param name: name of test case
    :return: function
    """

    line_code = ''.join(map(str.strip, inspect.getsource(case.function).split('\n')))
    call_code = '' #re.findall(r"\.(.*?)\,", line_code, re.MULTILINE)[0]

    @import_solution_module()
    @add_points(case.points)
    def test_case(self, module):
        if case.exact:
            self.assertEqual(case.function(module), case.output, f"{call_code} should equal to {case.output}")
        else:
            self.assertIn(case.function(module), case.output, f"{call_code} should be in {case.output}")

    test_case.__name__ = name

    return test_case


def resolve_test_cases(cls):
    cases_arrays = {cases_name: cases for cases_name, cases in cls.__dict__.items() if cases_name.endswith("_cases")}

    for case_name, cases in cases_arrays.items():
        for i, case in enumerate(cases):
            name = f"test_{case_name}_{i}"
            setattr(cls, name, create_function_for_case(name=name, case=case))

    return cls


def run_pylint_check(cls):
    setattr(cls, "pylint_check", True)
    return cls


def run_doctests_check(cls):
    setattr(cls, "doctests_check", True)
    return cls
