def check_rule(instructions):
    code = "DL3025"
    severity = "DLWarningC"
    message = "Use arguments JSON notation for CMD and ENTRYPOINT arguments"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("CMD") or instruction.startswith("ENTRYPOINT"):
            if not instruction.startswith(('CMD ["', 'ENTRYPOINT ["')):
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
#     'CMD ["echo", "Hello World"]',
#     'CMD echo Hello World',
#     'ENTRYPOINT ["sh", "-c", "echo Hello World"]',
#     'ENTRYPOINT echo Hello World'
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
