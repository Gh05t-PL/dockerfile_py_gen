import re

def has_no_bad_versioning(lbl, pairs):
    return all(not is_semantic_versioning(v) for l, v in pairs if l == lbl)

def is_semantic_versioning(value):
    # Semantic versioning regex pattern
    semver_pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-([\w\d]+(?:\.[\w\d]+)*))?(?:\+([\w\d]+(?:\.[\w\d]+)*))?$'
    return re.match(semver_pattern, value) is not None

def label_is_not_semver_rule(label):
    code = "DL3056"
    severity = "DLWarningC"
    message = f"Label `{label}` does not conform to semantic versioning."

    def check_line(line, instruction):
        if instruction.startswith("LABEL"):
            parts = instruction.split()[1:]
            pairs = {}
            pairs.update([parts[0].split('=')])
            if not has_no_bad_versioning(label, pairs.items()):
                return False
        return True

    return code, severity, message, check_line

def check_rule(instructions, labelschema):
    errors = []

    for label in labelschema.keys():
        code, severity, message, check_line = label_is_not_semver_rule(label)

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
#     "LABEL version=1.0.0",
#     "LABEL release=2.1-beta+build.2024"
# ]
#
# label_schema = {
#     "maintainer": "example@example.com",
#     "version": "1.0.0",
#     "release": "2.1-beta+build.2024"
# }
#
# errors = check_rule(dockerfile_instructions, label_schema)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
# # # TODO passing the label
