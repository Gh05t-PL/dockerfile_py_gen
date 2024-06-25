class StageID:
    def __init__(self, src, name, line):
        self.src = src
        self.name = name
        self.line = line

    def __eq__(self, other):
        if isinstance(other, StageID):
            return self.src == other.src and self.name == other.name and self.line == other.line
        return False

    def __hash__(self):
        return hash((self.src, self.name, self.line))

class Acc:
    def __init__(self, stageid=None, good=set(), bad=set()):
        self.stageid = stageid
        self.good = good
        self.bad = bad

def current_stage(src, stageid, acc):
    if acc is None:
        return Acc(stageid, set(), {stageid})
    predicate = lambda n1: n1.name == src
    if any(predicate(s) for s in acc.good):
        return Acc(stageid, acc.good | {stageid}, acc.bad)
    else:
        return Acc(stageid, acc.good, acc.bad | {stageid})

def good_stage(acc):
    if acc is None:
        return None
    now_good = recurse_good(acc.bad, acc.stageid)
    good = acc.good | now_good | {acc.stageid}
    bad = acc.bad - now_good - {acc.stageid}
    return Acc(acc.stageid, good, bad)

def recurse_good(bad, stageid):
    predicate = lambda s: s.src == stageid.name
    g1 = {s for s in bad if predicate(s)}
    b1 = bad - g1
    if not g1:
        return g1
    else:
        return g1 | set.union(*(recurse_good(b1, s) for s in g1))

def check_rule(instructions):
    code = "DL3057"
    severity = "DLIgnoreC"
    message = "`HEALTHCHECK` instruction missing."

    errors = []
    acc = None

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        parts = instruction.split()
        if instruction.startswith("FROM"):
            image = parts[1]
            alias = parts[3] if len(parts) > 3 else None
            stageid = StageID(image, alias if alias else image, line)
            acc = current_stage(image, stageid, acc)
        elif instruction.startswith("HEALTHCHECK"):
            acc = good_stage(acc)
        if acc and acc.bad:
            for stageid in acc.bad:
                errors.append({
                    "line": stageid.line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })
            acc.bad.clear()

    return errors
#
# # Example usage:
# dockerfile_lines = [
#     "FROM alpine AS base",
#     "RUN echo 'Hello World'",
#     "FROM base AS builder",
#     "RUN echo 'Building'",
#     "HEALTHCHECK CMD curl --fail http://localhost || exit 1",
# ]
#
# errors = check_rule(dockerfile_lines)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
