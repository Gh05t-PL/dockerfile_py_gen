class State:
    NO_ENTRY = "NoEntry"
    HAS_ENTRY = "HasEntry"

    def __init__(self, state=NO_ENTRY):
        self.state = state
        self.errors = []

    def replace_with(self, new_state):
        self.state = new_state

    def add_fail(self, error):
        self.errors.append(error)

def check_rule(instructions):
    state = State()
    code = "DL4004"
    severity = "DLErrorC"
    message = (
        "Multiple `ENTRYPOINT` instructions found. If you list more than one `ENTRYPOINT` then "
        "only the last `ENTRYPOINT` will take effect"
    )

    for line, instruction in enumerate(instructions):
        if instruction == "FROM":
            state.replace_with(State.NO_ENTRY)
        elif instruction == "ENTRYPOINT":
            if state.state == State.NO_ENTRY:
                state.replace_with(State.HAS_ENTRY)
            elif state.state == State.HAS_ENTRY:
                state.add_fail({
                    "code": code,
                    "severity": severity,
                    "message": message,
                    "line": line + 1  # Assuming line numbers start at 1
                })

    return state.errors
#
# # Example usage
# dockerfile_instructions = [
#     "FROM ubuntu:latest",
#     "ENTRYPOINT echo 'Hello, World!'",
#     "ENTRYPOINT echo 'This will override the previous ENTRYPOINT'"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
