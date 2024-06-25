class State:
    NO_CMD = "NoCmd"
    HAS_CMD = "HasCmd"

    def __init__(self, state=NO_CMD):
        self.state = state
        self.errors = []

    def replace_with(self, new_state):
        self.state = new_state

    def add_fail(self, error):
        self.errors.append(error)

def check_rule(instructions):
    state = State()
    code = "DL4003"
    severity = "DLWarningC"
    message = (
        "Multiple `CMD` instructions found. If you list more than one `CMD` then only the last "
        "`CMD` will take effect"
    )

    for line, instruction in enumerate(instructions):
        if instruction == "FROM":
            state.replace_with(State.NO_CMD)
        elif instruction == "CMD":
            if state.state == State.NO_CMD:
                state.replace_with(State.HAS_CMD)
            elif state.state == State.HAS_CMD:
                state.add_fail({
                    "code": code,
                    "severity": severity,
                    "message": message,
                    "line": line + 1  # Assuming line numbers start at 1
                })

    return state.errors

# Example usage
dockerfile_instructions = [
    "FROM ubuntu:latest",
    "CMD echo 'Hello, World!'",
    "CMD echo 'This will override the previous CMD'"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
