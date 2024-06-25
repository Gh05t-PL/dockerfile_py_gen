def contains_illegal_char(label):
    valid_chars = set('abcdefghijklmnopqrstuvwxyz0123456789.-')
    return any(char not in valid_chars for char in label)

def has_reserved_namespace(label):
    return any(label.startswith(prefix) for prefix in ["com.docker.", "io.docker.", "org.dockerproject."])

def has_consecutive_separators(label):
    return ".." in label or "--" in label

def has_no_invalid_key(pairs):
    valid_start_chars = set('abcdefghijklmnopqrstuvwxyz')
    valid_end_chars = set('abcdefghijklmnopqrstuvwxyz0123456789')
    # print(pairs)
    for key, value in pairs.items():
        if (key[0] not in valid_start_chars or
            key[-1] not in valid_end_chars or
            contains_illegal_char(key) or
            has_reserved_namespace(key) or
            has_consecutive_separators(key)):
            return False
    return True

def check_rule(instructions):
    code = "DL3048"
    severity = "DLStyleC"
    message = "Invalid label key."

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("LABEL"):
            parts = instruction.split()[1:]
            # print(parts)
            pairs = {}
            pairs.update([parts[0].split('=')])
            if not has_no_invalid_key(pairs):
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
#     "LABEL com.docker.sample=value",
#     "LABEL valid-label=value",
#     "LABEL invalid--label=value",
#     "LABEL io.docker.invalid=value"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
