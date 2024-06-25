def version_fixed(package):
    return any(op in package for op in ["=", ">=", ">", "<=", "<"]) or package.endswith(".rpm")

def zypper_packages(shell_cmds):
    packages = []
    commands = shell_cmds.split("&&")
    for cmd in commands:
        if any(sub_cmd in cmd for sub_cmd in ["zypper install", "zypper in"]):
            parts = cmd.split()
            packages.extend(arg for arg in parts if arg not in ["zypper", "install", "in"])
    return packages

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3037"
    severity = "DLWarningC"
    message = "Specify version with `zypper install -y <package>=<version>`."

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(lambda arg: all(version_fixed(pkg) for pkg in zypper_packages(arg)), args):
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
#     "RUN zypper install -y wget=1.20.3",
#     "RUN zypper in vim"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
