def check_rule(instructions):
    code = "DL3029"
    severity = "DLWarningC"
    message = "Do not use --platform flag with FROM"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM") and "--platform" in instruction:
            platform = instruction.split("--platform", 1)[1].split()[0]
            if "BUILDPLATFORM" in platform or "TARGETPLATFORM" in platform:
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
dockerfile_instructions = [
    "FROM --platform=$BUILDPLATFORM ubuntu:20.04",
    "FROM alpine:latest",
    "FROM --platform=$TARGETPLATFORM node:14"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
