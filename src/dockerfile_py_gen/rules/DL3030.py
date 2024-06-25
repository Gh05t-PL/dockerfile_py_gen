import re

def is_yum_install(cmd):
    return any(sub_cmd in cmd for sub_cmd in ["yum install", "yum groupinstall", "yum localinstall"])

def has_yes_option(cmd):
    return any(flag in cmd for flag in ["-y", "--assumeyes"])

def forgot_yum_yes_option(cmd):
    return is_yum_install(cmd) and not has_yes_option(cmd)

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3030"
    severity = "DLWarningC"
    message = "Use the -y switch to avoid manual input `yum install -y <package>`"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(forgot_yum_yes_option, args):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
dockerfile_instructions = [
    "RUN yum install curl",
    "RUN yum install -y wget",
    "RUN yum groupinstall -y 'Development Tools'"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
