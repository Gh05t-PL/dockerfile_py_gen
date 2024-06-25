import re

class State:
    def __init__(self):
        self.state = set()

    def modify(self, func):
        self.state = func(self.state)

    def replace_with(self, new_state):
        self.state = new_state

    def add_fail(self, failure):
        self.failures.append(failure)

def check_rule(instructions):
    code = "DL4001"
    severity = "DLWarningC"
    message = "Either use Wget or Curl but not both"

    errors = []
    state = State()

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            new_args = extract_commands(args)
            new_state = state.modify(lambda s: s.union(new_args))
            if len(new_args) > 0 and len(state.state) >= 2:
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })
        elif instruction.startswith("FROM"):
            state.replace_with(set())

    return errors

def extract_commands(args):
    return {
        0 if "curl" in cmd else 1
        for cmd in re.findall(r'\b(curl|wget)\b', args)
    }
#
# # Example usage
# dockerfile_instructions = [
#     "FROM alpine",
#     "RUN apt-get update && apt-get install -y curl",
#     "RUN wget https://example.com"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
