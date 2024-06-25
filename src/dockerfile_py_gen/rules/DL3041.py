def package_version_fixed(package):
    return "-" in package or package.endswith(".rpm")

def module_version_fixed(module):
    return ":" in module

def dnf_packages(shell_cmds):
    packages = []
    commands = shell_cmds.split("&&")
    for cmd in commands:
        if any(sub_cmd in cmd for sub_cmd in ["dnf install", "microdnf install"]) and "module" not in cmd:
            parts = cmd.split()
            packages.extend(arg for arg in parts if arg not in ["dnf", "microdnf", "install"])
    return packages

def dnf_modules(shell_cmds):
    modules = []
    commands = shell_cmds.split("&&")
    for cmd in commands:
        if "module" in cmd and any(sub_cmd in cmd for sub_cmd in ["dnf", "microdnf"]):
            parts = cmd.split()
            modules.extend(arg for arg in parts if arg not in ["dnf", "microdnf", "module"])
    return modules

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3041"
    severity = "DLWarningC"
    message = "Specify version with `dnf install -y <package>-<version>`."

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not (fold_arguments(lambda arg: all(package_version_fixed(pkg) for pkg in dnf_packages(arg)), args) and
                    fold_arguments(lambda arg: all(module_version_fixed(mod) for mod in dnf_modules(arg)), args)):
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
#     "RUN dnf install -y curl",
#     "RUN dnf install -y wget-1.20.3",
#     "RUN microdnf install -y vim"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
