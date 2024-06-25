import re

def using_program(program, args):
    return any(re.match(rf'\b{program}\b', arg) for arg in args.split())

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3004"
    severity = "DLErrorC"
    message = "Do not use sudo as it leads to unpredictable behavior. Use a tool like gosu to enforce root"

    errors = []

    for line, instruction in enumerate(instructions):
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(lambda arg: not using_program("sudo", arg), args):
                errors.append({
                    "code": code,
                    "severity": severity,
                    "message": message,
                    "line": line + 1
                })

    return errors

# Example usage
dockerfile_instructions = [
    "RUN sudo apt-get update",
    "RUN echo 'Hello World'",
    "RUN apt-get install -y curl"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
