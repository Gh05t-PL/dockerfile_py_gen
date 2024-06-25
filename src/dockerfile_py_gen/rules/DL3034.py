def is_zypper_install(cmd):
    zypper_commands = ["zypper install", "zypper in", "zypper remove", "zypper rm",
                       "zypper source-install", "zypper si", "zypper patch"]
    return any(sub_cmd in cmd for sub_cmd in zypper_commands)

def has_yes_option(cmd):
    return any(flag in cmd for flag in ["--non-interactive", "-n", "--no-confirm", "-y"])

def forgot_zypper_yes_option(cmd):
    return is_zypper_install(cmd) and not has_yes_option(cmd)

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3034"
    severity = "DLWarningC"
    message = "Non-interactive switch missing from `zypper` command: `zypper install -y`"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(forgot_zypper_yes_option, args):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
dockerfile_instructions = [
    "RUN zypper install curl",
    "RUN zypper install -y wget",
    "RUN zypper in -n vim"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
