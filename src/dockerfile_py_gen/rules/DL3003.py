import re

def using_program(program, args):
    return any(re.match(rf'\b{program}\b', arg) for arg in args.split())

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3003"
    severity = "DLWarningC"
    message = "Use WORKDIR to switch to a directory"

    errors = []

    for line, instruction in enumerate(instructions):
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(lambda arg: not using_program("cd", arg), args):
                errors.append({
                    "code": code,
                    "severity": severity,
                    "message": message,
                    "line": line + 1
                })

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "RUN cd /app && make",
#     "RUN echo 'Hello World'",
#     "RUN apt-get update"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
