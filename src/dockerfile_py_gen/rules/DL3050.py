def check_rule(instructions, labelschema, strictlabels):
    code = "DL3050"
    severity = "DLInfoC"
    message = "Superfluous label(s) present."

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("LABEL"):
            parts = instruction.split()[1:]
            pairs = {}
            pairs.update([parts[0].split('=')])
            if strictlabels and not all(pair[0] in labelschema.keys() for pair in pairs):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# # Example usage
# dockerfile_instructions = [
#     "LABEL maintainer=example@example.com",
#     "LABEL version=1.0",
#     "LABEL superfluous=label"
# ]
#
# label_schema = {"maintainer": "example@example.com", "version": "1.0"}
#
# errors = check_rule(dockerfile_instructions, label_schema, strictlabels=True)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
#
# # TODO passing the label
