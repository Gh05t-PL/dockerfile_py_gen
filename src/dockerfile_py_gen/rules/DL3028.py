import re

def version_fixed(package):
    return ":" in package

def gems(shell_cmds):
    gem_list = []
    commands = shell_cmds.split("&&")
    for cmd in commands:
        if re.search(r'\bgem (install|i)\b', cmd) and not re.search(r'\bgem (-v|--version|--version=)', cmd):
            args = cmd.split()
            args_until_double_dash = args[:args.index("--")] if "--" in args else args
            gem_list.extend(arg for arg in remove_options(args_until_double_dash) if arg not in ["install", "i"])
    return gem_list

def remove_options(args):
    return [arg for arg in args if not arg.startswith("-")]

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3028"
    severity = "DLWarningC"
    message = "Pin versions in gem install. Instead of `gem install <gem>` use `gem install <gem>:<version>`"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(lambda arg: all(version_fixed(pkg) for pkg in gems(arg)), args):
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
#     "RUN gem install rails",
#     "RUN gem install bundler:2.1.4",
#     "RUN gem i rake"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
