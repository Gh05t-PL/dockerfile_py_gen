import re


def is_valid_email(email):
    # Regular expression pattern for validating an email address according to RFC5322
    email_pattern = re.compile(
        r"(?:(?:\r\n)?[\t ])*"
        r"(?:[!#-'*+/-9=?A-Z^-~]+(?:\.[!#-'*+/-9=?A-Z^-~]+)*|"
        r"\"(?:[!#-[\]-~]|\\[\x00-\x7f])*\")"
        r"@(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?|"
        r"\[(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])\."
        r"(?:1?\d{1,2}|2[0-4]\d|25[0-5])\."
        r"(?:1?\d{1,2}|2[0-4]\d|25[0-5])\."
        r"(?:1?\d{1,2}|2[0-4]\d|25[0-5])|"
        r"[a-zA-Z0-9-]*[a-zA-Z0-9]:"
        r"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]"
        r"|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)])"
    )

    return re.fullmatch(email_pattern, email) is not None

def check_rule(instructions, labelschema):
    errors = []
    for label in labelschema.keys():
        for instruction in instructions:
            if instruction.startswith("LABEL"):
                parts = instruction.split()
                if len(parts) >= 2:
                    labels = parts[1:]
                    for lbl in labels:
                        if lbl.startswith(f"{label}="):
                            value = lbl.split("=")[1]
                            if not is_valid_email(value):
                                errors.append({
                                    'code': 'DL3058',
                                    'severity': 'DLWarningC',
                                    'message': f"Label `{label}` is not a valid email format - must conform to RFC5322.",
                                    'line': instructions.index(instruction) + 1
                                })

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "LABEL maintainer=test@example.com",
#     "LABEL author=John Doe"
# ]
#
# labelschema = {
#     "maintainer": "Email",
#     "author": "Name"
# }
#
# errors = check_rule(dockerfile_instructions, labelschema)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
# # # TODO passing the label
