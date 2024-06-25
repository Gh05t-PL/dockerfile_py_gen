class Acc:
    def __init__(self, flags=None, count=0):
        self.flags = flags
        self.count = count

    def __eq__(self, other):
        return self.flags == other.flags and self.count == other.count

    def __repr__(self):
        return f"Acc(flags={self.flags}, count={self.count})"


class EmptyAcc:
    pass


def remember(flags, count):
    return Acc(flags=flags, count=count)


def reset():
    return EmptyAcc()


def count_commands(args):
    return len([cmd for cmd in args.split('&&') if cmd.strip()])


def check_rule(instructions):
    code = "DL3059"
    severity = "DLInfoC"
    message = "Multiple consecutive `RUN` instructions. Consider consolidation."

    acc = EmptyAcc()
    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            flags = "mount" in args

            if isinstance(acc, EmptyAcc):
                acc = remember(flags, count_commands(args))
            elif acc.flags != flags:
                acc = remember(flags, count_commands(args))
            elif count_commands(args) > 2 or acc.count > 2:
                acc = remember(flags, count_commands(args))
            else:
                errors.append({"line": line, "code": code, "severity": severity, "message": message})
        elif instruction.startswith("COMMENT"):
            continue
        else:
            acc = reset()

    return errors

#
# # Example usage
# dockerfile_instructions = [
#     "RUN apt-get update",
#     "RUN apt-get install -y python3",
#     "RUN pip install requests && pip install flask",
#     "COMMENT This is a comment",
#     "RUN echo 'Hello, world!'",
#     "RUN mkdir /app && cd /app && touch app.py",
#     "RUN apt-get install -y vim"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
