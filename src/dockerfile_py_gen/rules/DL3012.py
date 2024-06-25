def check_rule(instructions):
    code = "DL3012"
    severity = "DLErrorC"
    message = "Multiple `HEALTHCHECK` instructions"

    errors = []
    healthcheck_state = False

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM"):
            healthcheck_state = False
        elif instruction.startswith("HEALTHCHECK"):
            if not healthcheck_state:
                healthcheck_state = True
            else:
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
dockerfile_instructions = [
    "FROM ubuntu:latest",
    "HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1",
    "HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1",
    "FROM alpine",
    "HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
