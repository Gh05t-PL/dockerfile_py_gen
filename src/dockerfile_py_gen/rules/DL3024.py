class State:
    def __init__(self, aliases=None):
        self.aliases = aliases if aliases is not None else set()

def check_rule(instructions):
    code = "DL3024"
    severity = "DLErrorC"
    message = "FROM aliases (stage names) must be unique"

    errors = []
    state = State()

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM"):
            parts = instruction.split()
            if len(parts) > 2 and parts[-2] == "AS":
                alias = parts[-1]
                if alias in state.aliases:
                    errors.append({
                        "line": line,
                        "code": code,
                        "severity": severity,
                        "message": message
                    })
                state.aliases.add(alias)

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "FROM alpine AS base",
#     "FROM ubuntu AS base",
#     "FROM alpine AS builder",
#     "FROM ubuntu AS builder"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
