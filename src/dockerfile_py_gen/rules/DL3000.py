import re

def is_windows_absolute(path):
    return bool(re.match(r'^[a-zA-Z]:', path))

def drop_quotes(path):
    return path.strip('\"').strip('\'')

def check_rule(instructions):
    code = "DL3000"
    severity = "DLErrorC"
    message = "Use absolute WORKDIR"

    errors = []

    for line, instruction in enumerate(instructions):
        if instruction.startswith("WORKDIR"):
            loc = instruction.split(" ", 1)[1].strip()
            loc = drop_quotes(loc)
            if not (loc.startswith("$") or loc.startswith("/") or is_windows_absolute(loc)):
                errors.append({
                    "code": code,
                    "severity": severity,
                    "message": message,
                    "line": line + 1
                })

    return errors

# Example usage
dockerfile_instructions = [
    "WORKDIR /app",
    "WORKDIR $HOME/app",
    "WORKDIR C:\\app",
    "WORKDIR app"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
