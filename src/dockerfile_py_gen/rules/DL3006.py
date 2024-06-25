import re
from collections import defaultdict

def insert_from_alias(base_image, state):
    if 'alias' in base_image and base_image['alias']:
        state.add(base_image['alias'])
    return state

def check_rule(instructions):
    code = "DL3006"
    severity = "DLWarningC"
    message = "Always tag the version of an image explicitly"

    errors = []
    state = set()

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM"):
            parts = instruction.split()
            base_image = {
                'image': parts[1] if len(parts) > 1 else '',
                'alias': parts[3] if len(parts) > 3 and parts[2].lower() == 'as' else None
            }

            new_state = insert_from_alias(base_image, state)

            if 'image' in base_image:
                image_parts = base_image['image'].split(':')
                image_name = image_parts[0]
                image_tag = image_parts[1] if len(image_parts) > 1 else None

                if image_name == "scratch" or 'digest' in base_image:
                    state = new_state
                elif image_tag is None:
                    if image_name.startswith("$") or image_name in state:
                        state = new_state
                    else:
                        errors.append({
                            "code": code,
                            "severity": severity,
                            "message": message,
                            "line": line
                        })
                else:
                    state = new_state

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "FROM ubuntu",
#     "FROM scratch",
#     "FROM alpine as builder",
#     "FROM builder"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
