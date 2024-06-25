import datetime

def get_bad_timeformat_labels(lbl, pairs):
    return [(l, v) for l, v in pairs if l == lbl and not is_valid_rfc3339(v)]

def is_valid_rfc3339(value):
    try:
        datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False

def label_is_not_rfc3339_rule(label):
    code = "DL3053"
    severity = "DLWarningC"
    message = f"Label `{label}` is not a valid time format - must conform to RFC3339."

    def check_line(line, instruction):
        if instruction.startswith("LABEL"):
            parts = instruction.split()[1:]
            pairs = {}
            pairs.update([parts[0].split('=')])
            if get_bad_timeformat_labels(label, pairs.items()):
                return False
        return True

    return code, severity, message, check_line

def check_rule(instructions, labelschema):
    errors = []

    for label in labelschema.keys():
        code, severity, message, check_line = label_is_not_rfc3339_rule(label)

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
#
# # Example usage
# dockerfile_instructions = [
#     "LABEL maintainer=example@example.com",
#     "LABEL version=1.0",
#     "LABEL created_at=2024-06-25T12:00:00Z"
# ]
#
# label_schema = {
#     "maintainer": "example@example.com",
#     "version": "1.0",
#     "created_at": "2024-06-25T12:00:00Z"
# }
#
# errors = check_rule(dockerfile_instructions, label_schema)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
# # # TODO passing the label
