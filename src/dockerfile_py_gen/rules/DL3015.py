def is_apt_get_install(cmd):
    return "apt-get install" in cmd

def disables_recommend_option(cmd):
    args = cmd.split()
    return (
        "--no-install-recommends" in args or
        any(arg.startswith("APT::Install-Recommends=false") for arg in args)
    )

def forgot_no_install_recommends(cmd):
    return is_apt_get_install(cmd) and not disables_recommend_option(cmd)

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3015"
    severity = "DLInfoC"
    message = "Avoid additional packages by specifying `--no-install-recommends`"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(forgot_no_install_recommends, args):
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
#     "RUN apt-get update && apt-get install curl",
#     "RUN apt-get install --no-install-recommends wget",
#     "RUN apt-get install -y software-properties-common"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
