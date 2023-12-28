import json
import sys
import re

class MyInterpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, statement):
        if statement["type"] == "variable_assignment":
            self.variables[statement["name"]] = self.evaluate(statement["value"])
        elif statement["type"] == "binary_operation":
            return self.evaluate_binary_operation(statement)
        elif statement["type"] == "function_call":
            return self.execute_function_call(statement)
        elif statement["type"] == "while_loop":
            return self.execute_while_loop(statement)
        elif statement["type"] == "comparison":
            return self.evaluate_comparison(statement)
        elif statement['type'] == "function_definition":
            return self.execute_function_definition(statement)
        else:
            raise NotImplementedError(f"Interpreter does not support statements of type {statement['type']}")

    def evaluate(self, expression):
        if isinstance(expression, dict):
            return self.interpret(expression)
        elif isinstance(expression, str) and expression in self.variables:
            return self.variables[expression]
        else:
            return expression

    def evaluate_binary_operation(self, binary_op):
        left = self.evaluate(binary_op["left"])
        right = self.evaluate(binary_op["right"])
        op = binary_op["op"]

        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return left / right
        else:
            raise ValueError(f"Unsupported binary operation: {op}")

    def execute_function_definition(self, func_def):
        function_name = func_def["name"]
        parameters = func_def["parameters"]
        body = func_def["body"]
        self.variables[function_name] = {"type": "function", "parameters": parameters, "body": body}

    def execute_function_call(self, func_call):
        func_name = func_call["name"]
        args = [self.evaluate(arg) for arg in func_call["args"]]

        if func_name == "print":
            print(*args)
        elif func_name == "type":
            return type(*args)
        elif func_name == "input":
            return input(*args)
        elif func_name == "Format":
            return self.format_string(args)
        elif func_name in self.variables and self.variables[func_name]["type"] == "function":
            function_data = self.variables[func_name]
            # Create a local scope for the function call
            local_scope = {param: args[i] for i, param in enumerate(function_data["parameters"])}
            # Add local scope to variables
            self.variables.update(local_scope)
            # Execute the function body
            for stmt in function_data["body"]:
                result = self.interpret(stmt)
            # Remove local scope variables
            for param in function_data["parameters"]:
                del self.variables[param]
            return result
        else:
            raise ValueError(f"Unsupported function call: {func_name}")

    # Format(<string to replace>, <elements>)
    def format_string(self, args):
        def replace_match(match):
            index = int(match.group(1))
            if index < 1:
                raise ValueError("index value is too low, cannot replace string")
            return str(args[index])

        pattern = re.compile(r'\$(\d+)')
        return pattern.sub(replace_match, args[0])

    def execute_while_loop(self, while_loop):
        result = None
        while self.evaluate(while_loop["condition"]):
            for stmt in while_loop["body"]:
                result = self.interpret(stmt)
        return result

    def evaluate_comparison(self, comparison):
        left = self.evaluate(comparison["left"])
        right = self.evaluate(comparison["right"])
        op = comparison["op"]

        if op == "<":
            return left < right
        elif op == ">":
            return left > right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        else:
            raise ValueError(f"Unsupported comparison operation: {op}")

def interpret_custom_syntax(statements):
    interpreter = MyInterpreter()
    for statement in statements:
        interpreter.interpret(statement)

# Example usage
with open(sys.argv[1]) as f:
    code = json.loads(f.read())
interpret_custom_syntax(code)
