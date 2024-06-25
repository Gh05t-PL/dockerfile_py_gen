def is_zypper_dist_upgrade(cmd):
    return any(sub_cmd in cmd for sub_cmd in ["zypper dist-upgrade", "zypper dup"])

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3035"
    severity = "DLWarningC"
    message = "Do not use `zypper dist-upgrade`."

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(lambda arg: not is_zypper_dist_upgrade(arg), args):
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
#     "RUN zypper dist-upgrade",
#     "RUN zypper dup",
#     "RUN zypper install -y curl"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
