import re
from collections import defaultdict

class Acc:
    def __init__(self, stage_line=None, user_lines=None):
        self.stage_line = stage_line
        self.user_lines = user_lines if user_lines is not None else defaultdict(list)

    def __str__(self):
        return f"Acc(stage_line={self.stage_line}, user_lines={self.user_lines})"

def is_root(user):
    return user.startswith("root:") or user.startswith("0:") or user == "root" or user == "0"

def remember_stage(stage_line, acc):
    acc.stage_line = stage_line
    return acc

def forget_stage(acc):
    if acc.stage_line in acc.user_lines:
        del acc.user_lines[acc.stage_line]
    return acc

def remember_line(line, acc):
    acc.user_lines[acc.stage_line].append(line)
    return acc

def make_fail(line, code, severity, message):
    return {
        "line": line,
        "code": code,
        "severity": severity,
        "message": message
    }

def check_rule(instructions):
    code = "DL3002"
    severity = "DLWarningC"
    message = "Last USER should not be root"

    errors = []
    acc = Acc()

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        parts = instruction.split()
        if not parts:
            continue
        cmd = parts[0]

        if cmd == "FROM":
            acc = remember_stage(line, acc)
        elif cmd == "USER":
            user = parts[1].strip()
            if not is_root(user):
                acc = forget_stage(acc)
            else:
                acc = remember_line(line, acc)

    for stage_line, user_lines in acc.user_lines.items():
        for user_line in user_lines:
            errors.append(make_fail(user_line, code, severity, message))

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "FROM ubuntu:latest",
#     "USER root",
#     "RUN apt-get update",
#     "USER someuser",
#     "RUN echo 'Hello World'",
#     "USER root",
#     "RUN apt-get install -y sudo"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
