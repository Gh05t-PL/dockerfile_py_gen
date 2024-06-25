class StageID:
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def __eq__(self, other):
        return self.name == other.name and self.line == other.line

    def __hash__(self):
        return hash((self.name, self.line))

    def __repr__(self):
        return f"StageID(name={self.name}, line={self.line})"

class Acc:
    def __init__(self, current=None, good=None, silent=None, bad=None):
        self.current = current if current is not None else None
        self.good = good if good is not None else set()
        self.silent = silent if silent is not None else set()
        self.bad = bad if bad is not None else set()

def missing_label_rule(label):
    code = "DL3049"
    severity = "DLInfoC"
    message = f"Label `{label}` is missing."

    def check_line(line, state, instruction):
        if instruction.startswith("FROM"):
            img = instruction.split()[1]
            state = current_stage(StageID(img, line), state)
        elif instruction.startswith("COPY"):
            src = instruction.split()[-1]
            state = mark_silent_by_alias(src, state)
        elif instruction.startswith("LABEL"):
            pairs = dict([instruction.split()[1].split('=')])
            if label in pairs:
                state = mark_silent_by_alias(get_current_stage_name(state), state)
                state = mark_good(state)
        return state

    def mark_failures(state):
        if state and state.bad:
            return [f"Error at line {stage.line}: {message} ({code})" for stage in state.bad]
        return []

    return check_line, mark_failures

def current_stage(stage_id, acc):
    if acc is None:
        return Acc(current=stage_id, bad={stage_id})

    if any(predicate(stage_id, stage) for stage in acc.good):
        acc.good.add(stage_id)
    else:
        acc.bad.add(stage_id)

    return Acc(current=stage_id, good=acc.good, silent=acc.silent, bad=acc.bad)

def predicate(stage_id, stage):
    return stage_id.name == stage.name

def mark_good(acc):
    if acc is None:
        return acc
    acc.good.add(acc.current)
    acc.silent.discard(acc.current)
    acc.bad.discard(acc.current)
    return acc

def mark_silent_by_alias(silent_name, acc):
    if acc is None:
        return acc

    stages = {stage for stage in acc.bad if by_name(stage, silent_name)}
    acc.silent.update(stages)
    acc.bad.difference_update(stages)
    return acc

def by_name(stage, name):
    return stage.name == name

def get_current_stage_name(state):
    if state and state.current:
        return state.current.name
    return ""

def check_rule(instructions, label):
    check_line, mark_failures = missing_label_rule(label)
    state = None

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        state = check_line(line, state, instruction)

    errors = mark_failures(state)
    return errors

# # Example usage
# dockerfile_instructions = [
#     "FROM alpine AS base",
#     "LABEL ff=1.0",
#     "LABEL version=1.0",
#     "FROM alpine AS base",
#     "LABEL maintainer=example@example.com"
#     "COPY --from=base /app /app",
#     "FROM base AS builder",
#     "LABEL maintainer=example@example.com"
# ]
#
# errors = check_rule(dockerfile_instructions, "maintainer")
# for error in errors:
#     print(error)
# TODO passing the label
