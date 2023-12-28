import sys, json
from ast_gen import parse_custom_syntax as parse_gen

if(len(sys.argv) < 2):
    print("pass a file:\n",sys.argv[0], "<file>")
    exit(1)
else:
    file = sys.argv[1]
    with open(file) as f:
        code = f.read()

    ast = parse_gen(code)

    with open(file.replace(".snug", ".json"),'w') as f:
        f.write(json.dumps(ast,indent=4)+"\n")

    print(f"generated ast, {file.replace(".snug", ".json")}") # if this throws a error, its because you arent using python 3.13
