import re

invalid_cmds = {"free", "kill", "mount", "ps", "service", "shutdown", "ssh", "top", "vim"}

def find_command_names(args):
    # This is a simple implementation to find command names in arguments
    # Adjust based on the actual parsing logic required
    return re.findall(r'\b\w+\b', args)

def fold_arguments(check_func, args):
    return any(check_func(arg) for arg in args)

def has_invalid(args):
    command_names = find_command_names(args)
    return not any(arg in invalid_cmds for arg in command_names)

def check_rule(instructions):
    code = "DL3001"
    severity = "DLInfoC"
    message = (
        "For some bash commands it makes no sense running them in a Docker container like `ssh`, "
        "`vim`, `shutdown`, `service`, `ps`, `free`, `top`, `kill`, `mount`, `ifconfig`"
    )

    errors = []

    for line, instruction in enumerate(instructions):
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if fold_arguments(has_invalid, [args]):
                errors.append({
                    "code": code,
                    "severity": severity,
                    "message": message,
                    "line": line + 1
                })

    return errors

# Example usage
dockerfile_instructions = [
    "RUN ssh some_host",
    "RUN echo 'Hello World'",
    "RUN vim some_file",
    "RUN apt-get update && apt-get install -y curl"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
