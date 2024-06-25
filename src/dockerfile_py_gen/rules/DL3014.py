import re

def is_apt_get_install(cmd):
    return "apt-get install" in cmd

def has_yes_option(cmd):
    args = cmd.split()
    return (
        any(flag in args for flag in ["-y", "--yes", "-qq", "--assume-yes"]) or
        args.count("-q") == 2 or
        args.count("--quiet") == 2 or
        "-q=2" in args
    )

def forgot_apt_yes_option(cmd):
    return is_apt_get_install(cmd) and not has_yes_option(cmd)

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3014"
    severity = "DLWarningC"
    message = "Use the `-y` switch to avoid manual input `apt-get -y install <package>`"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(forgot_apt_yes_option, args):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
dockerfile_instructions = [
    "RUN apt-get update && apt-get install curl",
    "RUN apt-get -y install wget",
    "RUN apt-get install -qq software-properties-common"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
