import urllib.parse as urlparse

def get_bad_url_labels(lbl, pairs):
    return [(l, u) for l, u in pairs if l == lbl and not urlparse.urlparse(u).scheme]

def label_is_not_url_rule(label):
    code = "DL3052"
    severity = "DLWarningC"
    message = f"Label `{label}` is not a valid URL."

    def check_line(line, instruction):
        if instruction.startswith("LABEL"):
            parts = instruction.split()[1:]
            pairs = {}
            pairs.update([parts[0].split('=')])
            if get_bad_url_labels(label, pairs.items()):
                return False
        return True

    return code, severity, message, check_line

def check_rule(instructions, labelschema):
    errors = []

    for label in labelschema.keys():
        code, severity, message, check_line = label_is_not_url_rule(label)

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
#     "LABEL url=https://example.com"
# ]
#
# label_schema = {
#     "maintainer": "example@example.com",
#     "version": "1.0",
#     "url": "https://example.com"
# }
#
# errors = check_rule(dockerfile_instructions, label_schema)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
# # # TODO passing the label
