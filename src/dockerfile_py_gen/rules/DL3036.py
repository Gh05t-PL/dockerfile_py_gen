def is_zypper_install(cmd):
    return any(sub_cmd in cmd for sub_cmd in ["zypper install", "zypper in"])

def is_zypper_clean(cmd):
    return any(sub_cmd in cmd for sub_cmd in ["zypper clean", "zypper cc"])

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3036"
    severity = "DLWarningC"
    message = "`zypper clean` missing after zypper use."

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(is_zypper_install, args) or (fold_arguments(is_zypper_install, args) and fold_arguments(is_zypper_clean, args)):
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
#     "RUN zypper install curl",
#     "RUN zypper install -y wget && zypper clean",
#     "RUN zypper in -y vim && zypper cc"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
