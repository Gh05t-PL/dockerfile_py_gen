import re

def version_fixed(package):
    return "=" in package or ("/" in package or package.endswith(".deb"))

def apt_get_packages(args):
    packages = []
    commands = re.split(r'\s&&\s|\s;\s', args)
    for command in commands:
        if re.match(r'\bapt-get\b', command) and "install" in command:
            parts = command.split()
            for part in parts:
                if part not in ["apt-get", "install"]:
                    packages.append(part)
    return packages

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3008"
    severity = "DLWarningC"
    message = (
        "Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get "
        "install <package>=<version>`"
    )

    errors = []

    for line, instruction in enumerate(instructions):
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(lambda arg: all(version_fixed(pkg) for pkg in apt_get_packages(arg)), args):
                errors.append({
                    "code": code,
                    "severity": severity,
                    "message": message,
                    "line": line + 1
                })

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "RUN apt-get install package",
#     "RUN apt-get install package=1.0",
#     "RUN apt-get update && apt-get install another-package"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
