def get_empty_labels(lbl, pairs):
    return [(l, v) for l, v in pairs if l == lbl and v == ""]

def label_is_not_empty_rule(label):
    code = "DL3051"
    severity = "DLWarningC"
    message = f"label `{label}` is empty."

    def check_line(line, instruction):
        if instruction.startswith("LABEL"):
            parts = instruction.split()[1:]
            pairs = {}
            for part in parts:
                if '=' in part:
                    key, value = part.split('=', 1)
                    pairs[key] = value
                else:
                    pairs[part] = ""
            if get_empty_labels(label, pairs.items()):
                return False
        return True

    return code, severity, message, check_line

def check_rule(instructions, labelschema):
    errors = []

    for label in labelschema.keys():
        code, severity, message, check_line = label_is_not_empty_rule(label)

        for line_num, instruction in enumerate(instructions):
            line = line_num + 1
            if not check_line(line, instruction):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# # Example usage
# dockerfile_instructions = [
#     "LABEL maintainer=",
#     "LABEL version=1.0",
#     "LABEL description="
# ]
#
# label_schema = {"maintainer": "example@example.com", "version": "1.0", "description": "Description"}
#
# errors = check_rule(dockerfile_instructions, label_schema)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
#
# # TODO passing the label
