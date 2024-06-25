def check_rule(instructions):
    errors = []
    found_valid_start = False

    for idx, instruction in enumerate(instructions):
        instruction = instruction.strip()
        if instruction.startswith("FROM") or instruction.startswith("ARG") or instruction.startswith("#"):
            found_valid_start = True
        elif instruction.startswith("COMMENT"):
            continue
        else:
            errors.append({
                'code': 'DL3061',
                'severity': 'DLErrorC',
                'message': "Invalid instruction order. Dockerfile must begin with `FROM`, `ARG` or comment.",
                'line': idx + 1
            })
            break

    if not found_valid_start:
        errors.append({
            'code': 'DL3061',
            'severity': 'DLErrorC',
            'message': "Invalid instruction order. Dockerfile must begin with `FROM`, `ARG` or comment.",
            'line': 1
        })

    return errors

# Example usage
dockerfile_instructions = [
    "ARG VERSION=latest",
    "RUN apt-get update",
    "FROM python:3.9",
    "# This is a comment",
    "COPY . /app",
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
