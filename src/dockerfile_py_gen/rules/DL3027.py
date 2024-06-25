def using_program(program, args):
    return any(program in arg for arg in args.split("&&"))

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3027"
    severity = "DLWarningC"
    message = "Do not use apt as it is meant to be an end-user tool, use apt-get or apt-cache instead"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(lambda arg: not using_program("apt", arg), args):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "RUN apt update && apt install -y curl",
#     "RUN apt-get update && apt-get install -y wget",
#     "RUN apt-cache search git"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
