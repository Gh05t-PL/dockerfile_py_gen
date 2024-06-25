import re

truthy = {"1", "true", "True", "TRUE", "on", "On", "ON", "yes", "Yes", "YES"}

class Stage:
    def __init__(self, stage):
        self.stage = stage

    def __eq__(self, other):
        if isinstance(other, Stage):
            return self.stage == other.stage
        return False

    def __hash__(self):
        return hash(self.stage)

class Acc:
    def __init__(self, current=None, no_cache_map=None):
        self.current = current if current is not None else None
        self.no_cache_map = no_cache_map if no_cache_map is not None else {}

def remember_stage(from_instr, acc):
    if from_instr['alias']:
        alias = from_instr['alias']
        if acc is None:
            return Acc(current=Stage(alias), no_cache_map={})
        parent_value = acc.no_cache_map.get(Stage(from_instr['image']), False)
        acc.no_cache_map[Stage(alias)] = parent_value
        return Acc(current=Stage(alias), no_cache_map=acc.no_cache_map)
    if acc is None:
        return Acc(current=Stage(from_instr['image']), no_cache_map={})
    parent_value = acc.no_cache_map.get(Stage(from_instr['image']), False)
    acc.no_cache_map[Stage(from_instr['image'])] = parent_value
    return Acc(current=Stage(from_instr['image']), no_cache_map=acc.no_cache_map)

def register_env(pairs, acc):
    if pip_no_cache_dir_set(pairs):
        if acc is None:
            return Acc(current=None, no_cache_map={None: True})
        acc.no_cache_map[acc.current] = True
    return acc

def pip_no_cache_dir_set(pairs):
    return any(pair[0] == "PIP_NO_CACHE_DIR" and pair[1] in truthy for pair in pairs)

def pip_no_cache_dir_is_set(shell):
    return any(
        truth in shell for truth in truthy
    )

def is_pip_wrapper(cmd):
    return any(wrapper in cmd for wrapper in ["pipx", "pipenv"]) or \
        (cmd.startswith("python") and any(arg in cmd for arg in ["-m pipx", "-m pipenv"]))

def uses_no_cache_dir(cmd):
    return "--no-cache-dir" in cmd

def forgot_no_cache_dir(cmd):
    return "pip install" in cmd and not uses_no_cache_dir(cmd) and not is_pip_wrapper(cmd)

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3042"
    severity = "DLWarningC"
    message = "Avoid use of cache directory with pip. Use `pip install --no-cache-dir <package>`"

    errors = []
    acc = None

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM"):
            parts = instruction.split()

            from_instr = {"image": parts[1], "alias": parts[3]}

            acc = remember_stage(from_instr, acc)
        elif instruction.startswith("ENV"):
            parts = instruction.split()

            pairs = parts[1].split('=')
            acc = register_env(pairs, acc)
        elif instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if acc and acc.no_cache_map.get(acc.current, False):
                continue
            if not fold_arguments(forgot_no_cache_dir, args):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
# dockerfile_instructions = [
#     "FROM alpine AS base",
#     "ENV PIP_NO_CACHE_DIR=1",
#     "RUN pip install somepackage",
#     "FROM base AS builder",
#     "RUN pip install --no-cache-dir anotherpackage"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
