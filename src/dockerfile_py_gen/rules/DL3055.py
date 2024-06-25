import re

def get_bad_hash_labels(lbl, pairs):
    return [(l, v) for l, v in pairs if l == lbl and not is_valid_git_hash(v)]

def is_valid_git_hash(value):
    if re.match(r'^[0-9a-f]{40}$', value):
        return True
    if re.match(r'^[0-9a-f]{7}$', value):
        return True
    return False

def label_is_not_git_hash_rule(label):
    code = "DL3055"
    severity = "DLWarningC"
    message = f"Label `{label}` is not a valid git hash."

    def check_line(line, instruction):
        if instruction.startswith("LABEL"):
            parts = instruction.split()[1:]
            pairs = {}
            pairs.update([parts[0].split('=')])
            if get_bad_hash_labels(label, pairs.items()):
                return False
        return True

    return code, severity, message, check_line

def check_rule(instructions, labelschema):
    errors = []

    for label in labelschema.keys():
        code, severity, message, check_line = label_is_not_git_hash_rule(label)

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
#     "LABEL git_commit=abc1234567890123456789012345678901234567"
# ]
#
# label_schema = {
#     "maintainer": "example@example.com",
#     "version": "1.0",
#     "git_commit": "abc1234567890123456789012345678901234567"
# }
#
# errors = check_rule(dockerfile_instructions, label_schema)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
# # # TODO passing the label
