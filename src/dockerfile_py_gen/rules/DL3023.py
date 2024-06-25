def drop_quotes(s):
    return s.strip('"').strip("'")

class State:
    def __init__(self, failures=None, from_instr=None):
        self.failures = failures if failures is not None else []
        self.from_instr = from_instr

def alias_must_be(predicate, from_instr):
    if from_instr is None:
        return False
    _, alias = from_instr
    return predicate(alias)

def check_rule(instructions):
    code = "DL3023"
    severity = "DLErrorC"
    message = "`COPY --from` cannot reference its own `FROM` alias"

    errors = []
    state = State()

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM"):
            parts = instruction.split()
            alias = parts[-1] if len(parts) > 2 and parts[-2] == "AS" else None
            state.from_instr = (instruction, alias)
        elif instruction.startswith("COPY") and state.from_instr:
            parts = instruction.split()
            if "--from" in parts:
                stage_name = drop_quotes(parts[parts.index("--from") + 1])
                if not alias_must_be(lambda x: x != stage_name, state.from_instr):
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
#     "FROM alpine AS base",
#     "COPY --from=base /src /dst",
#     "FROM base AS builder",
#     "COPY --from=builder /src /dst",
#     "FROM invalid AS invalid",
#     "COPY --from=invalid /src /dst"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
