def check_rule(instructions):
    code = "DL3043"
    severity = "DLErrorC"
    message = "`ONBUILD`, `FROM` or `MAINTAINER` triggered from within `ONBUILD` instruction."

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("ONBUILD"):
            inner_instruction = instruction.split(" ", 1)[1]
            if inner_instruction.startswith(("ONBUILD", "FROM", "MAINTAINER")):
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
#     "ONBUILD RUN echo 'Hello World'",
#     "ONBUILD ONBUILD RUN echo 'Hello World'",
#     "ONBUILD FROM alpine",
#     "ONBUILD MAINTAINER example@example.com"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
