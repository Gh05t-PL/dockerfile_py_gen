def version_fixed(package):
    return "=" in package

def package_file(package):
    return package.endswith(".apk")

def apk_add_packages(args):
    packages = []
    commands = args.split("&&")
    for cmd in commands:
        if "apk add" in cmd:
            parts = cmd.split()
            for part in parts:
                if part not in ["apk", "add"]:
                    packages.append(part)
    return packages

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3018"
    severity = "DLWarningC"
    message = (
        "Pin versions in apk add. Instead of `apk add <package>` "
        "use `apk add <package>=<version>`"
    )

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(lambda as_: all(version_fixed(p) or package_file(p) for p in apk_add_packages(as_)), args):
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
#     "RUN apk add curl",
#     "RUN apk add wget=1.20.3-r0",
#     "RUN apk add mypackage.apk"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
