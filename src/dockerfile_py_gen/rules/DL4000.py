def check_rule(instructions):
    errors = []

    for idx, instruction in enumerate(instructions):
        instruction = instruction.strip()
        if instruction.startswith("MAINTAINER"):
            errors.append({
                'code': 'DL4000',
                'severity': 'DLErrorC',
                'message': "MAINTAINER is deprecated",
                'line': idx + 1
            })

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "FROM python:3.9",
#     "MAINTAINER John Doe <john.doe@example.com>",
#     "RUN apt-get update",
#     "COPY . /app",
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
