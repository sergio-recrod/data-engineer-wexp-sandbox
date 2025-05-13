import argparse

def test(a):
    print(f"test {a}")

def show(a):
    print(f"show {a}")

parser = argparse.ArgumentParser()
parser.add_argument("command", nargs="+")
arguments = parser.parse_args(["test", "asdf", "1"])

command_functions = {"test": test, "show": show}

command_functions[arguments.command[0]](arguments.command[1:])

print(arguments.command[0])
print(arguments.command[1:])
print(int(arguments.command[-1]))

