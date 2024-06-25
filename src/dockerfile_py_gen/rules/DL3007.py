def check_rule(instructions):
    code = "DL3007"
    severity = "DLWarningC"
    message = (
        "Using latest is prone to errors if the image will ever update. Pin the version explicitly "
        "to a release tag"
    )

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM"):
            parts = instruction.split()
            if len(parts) > 1:
                image = parts[1]
                image_parts = image.split('@')
                image_name_tag = image_parts[0]
                digest = image_parts[1] if len(image_parts) > 1 else None

                tag = None
                if ':' in image_name_tag:
                    image_name, tag = image_name_tag.split(':', 1)
                else:
                    image_name = image_name_tag

                if digest is not None or (tag is not None and tag != "latest"):
                    continue

                errors.append({
                    "code": code,
                    "severity": severity,
                    "message": message,
                    "line": line
                })

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "FROM ubuntu:latest",
#     "FROM alpine:3.12",
#     "FROM myrepo/myimage@sha256:abc123",
#     "FROM debian"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
