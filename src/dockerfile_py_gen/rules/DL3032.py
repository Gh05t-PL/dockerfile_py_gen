import re

def yum_install(cmd):
    return "yum install" in cmd

def yum_clean(cmd):
    return any(sub_cmd in cmd for sub_cmd in ["yum clean all", "rm -rf /var/cache/yum/*"])

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3032"
    severity = "DLWarningC"
    message = "`yum clean all` missing after yum command."

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(yum_install, args) or (fold_arguments(yum_install, args) and fold_arguments(yum_clean, args)):
                continue
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
#     "RUN yum install curl",
#     "RUN yum install -y wget && yum clean all",
#     "RUN yum install -y gcc && rm -rf /var/cache/yum/*"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
