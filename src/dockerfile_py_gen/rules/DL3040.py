def is_dnf_install(cmd, cmd_name):
    return f"{cmd_name} install" in cmd

def is_dnf_clean(cmd, cmd_name):
    return any(sub_cmd in cmd for sub_cmd in [f"{cmd_name} clean all", "rm -rf /var/cache/yum/*"])

def check_missing_clean(args, cmd_name):
    return (all(not is_dnf_install(arg, cmd_name) for arg in args.split("&&")) or
            (any(is_dnf_install(arg, cmd_name) for arg in args.split("&&")) and
             any(is_dnf_clean(arg, cmd_name) for arg in args.split("&&"))))

def check_rule(instructions):
    code = "DL3040"
    severity = "DLWarningC"
    message = "`dnf clean all` missing after dnf command."

    errors = []
    dnf_cmds = ["dnf", "microdnf"]

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if any(not check_missing_clean(args, cmd_name) for cmd_name in dnf_cmds):
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
#     "RUN dnf install -y wget && dnf clean all",
#     "RUN microdnf install -y vim && rm -rf /var/cache/yum/*"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
