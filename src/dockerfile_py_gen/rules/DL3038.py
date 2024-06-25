def is_dnf_install(cmd):
    dnf_cmds = ["dnf install", "dnf groupinstall", "dnf localinstall",
                "microdnf install", "microdnf groupinstall", "microdnf localinstall"]
    return any(sub_cmd in cmd for sub_cmd in dnf_cmds)

def has_yes_option(cmd):
    return any(flag in cmd for flag in ["-y", "--assumeyes"])

def forgot_dnf_yes_option(cmd):
    return is_dnf_install(cmd) and not has_yes_option(cmd)

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3038"
    severity = "DLWarningC"
    message = "Use the -y switch to avoid manual input `dnf install -y <package>`"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(forgot_dnf_yes_option, args):
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
#     "RUN dnf install curl",
#     "RUN dnf install -y wget",
#     "RUN microdnf install -y vim"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
