import ast
import json
import sys
import re
type_mapping = {
    'int': int,
    'str': str,
    'list':list,
    'dict':dict,
    'none':None
    # Add more types as needed
}

class MySyntaxVisitor(ast.NodeVisitor):
    def visit_Assign(self, node):
        variable_name = node.targets[0].id
        value = self.visit(node.value)

        return {"type": "variable_assignment", "name": variable_name, "value": value}

    def visit_Str(self, node):
        return node.value

    def visit_Num(self, node):
        return node.value


    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.visit(node.op)
        return {"type": "binary_operation", "left": left, "op": op, "right": right}

    def visit_Add(self, node):
        return "+"

    def visit_Sub(self, node):
        return "-"

    def visit_Div(self, node):
        return "/"

    def visit_Mult(self, node):
        return "*"

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Call(self, node):
        function_name = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        return {"type": "function_call", "name": function_name, "args": args}

    def visit_Name(self, node):
        return node.id

    def visit_FunctionDef(self, node):
        function_name = node.name
        parameters = [param.arg for param in node.args.args]
        body = [self.visit(stmt) for stmt in node.body]
        return {"type": "function_definition", "name": function_name, "parameters": parameters, "body": body}

    def visit_While(self, node):
        condition = self.visit(node.test)
        body = [self.visit(stmt) for stmt in node.body]
        return {"type": "while_loop", "condition": condition, "body": body}


    def visit_List(self, node):
        elements = [self.visit(elt) for elt in node.elts]
        return {"type": "list", "elements": elements}


    def visit_Dict(self, node):
        keys = [self.visit(key) for key in node.keys]
        values = [self.visit(value) for value in node.values]
        return {"type": "dictionary", "keys": keys, "values": values}

    def visit_If(self, node):
        condition = self.visit(node.test)
        body = [self.visit(stmt) for stmt in node.body]
        orelse = [self.visit(stmt) for stmt in node.orelse]
        return {"type": "if_statement", "condition": condition, "body": body, "orelse": orelse}

    def visit_For(self, node):
        target = self.visit(node.target)
        iter_node = self.visit(node.iter)
        body = [self.visit(stmt) for stmt in node.body]
        orelse = [self.visit(stmt) for stmt in node.orelse]
        return {"type": "for_loop", "target": target, "iter": iter_node, "body": body, "orelse": orelse}

    def visit_Return(self, node):
        value = self.visit(node.value) if node.value else None
        return {"type": "return_statement", "value": value}

    def visit_ClassDef(self, node):
        class_name = node.name
        methods = [self.visit(method) for method in node.body if isinstance(method, ast.FunctionDef)]
        return {"type": "class_definition", "name": class_name, "methods": methods}


    def visit_Compare(self, node):
        left = self.visit(node.left)
        op = self.visit(node.ops[0])
        right = self.visit(node.comparators[0])
        return {"type": "comparison", "left": left, "op": op, "right": right}

    def visit_Lt(self, node):
        return "<"
    def visit_Gt(self, node):
        return ">"
    def visit_LtE(self, node):
        return "<="
    def visit_GtE(self, node):
        return ">="
    def visit_Eq(self, node):
        return "=="
    def visit_NotEq(self, node):
        return "!="
    def generic_visit(self, node):
        return super().generic_visit(node)


    def visit_AnnAssign(self, node):
        variable_name = node.target.id
        annotation = self.visit(node.annotation)
        value = self.visit(node.value)

        if annotation not in type_mapping:
            raise TypeError(f"Unknown type annotation: {annotation}")

        expected_type = type_mapping[annotation]

        if not isinstance(value, expected_type):
            raise TypeError(f"Type mismatch for variable '{variable_name}'. Expected {expected_type}, but got {type(value)}")

        return {"type": "variable_assignment", "name": variable_name, "value": value}



def preprocess_code(code):
    # Define the macro pattern with optional parameters
    macro_pattern = r"macro (\w+)(?:\((.*?)\))?\n(.*?)\nend"

    # Find all occurrences of the macro pattern in the code
    matches = re.finditer(macro_pattern, code, re.DOTALL)

    # Replace macro occurrences with their corresponding code
    for match in matches:
        macro_name = match.group(1)
        parameters = match.group(2)
        macro_code = match.group(3)

        # Check if the macro has parameters
        if parameters:
            # You can choose to handle parameters as needed
            raise ValueError(f"Macros should not take parameters: {macro_name}({parameters})")
        else:
            code = code.replace(match.group(0), f'def {macro_name}():\n{macro_code}')

    return code


def parse_custom_syntax(code):
    code = preprocess_code(code)
    tree = ast.parse(code)
    visitor = MySyntaxVisitor()
    result = [visitor.visit(stmt) for stmt in tree.body]
    return [stmt for stmt in result if stmt is not None]
