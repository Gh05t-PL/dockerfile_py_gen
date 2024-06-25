def drop_quotes(s):
    return s.strip('"').strip("'")

class Acc:
    def __init__(self, count=0, names=None):
        self.count = count
        self.names = set() if names is None else names

    def __eq__(self, other):
        return self.count == other.count and self.names == other.names

def inc_and_add_name(s, acc):
    if acc is None:
        return Acc(count=1, names={s})
    acc.count += 1
    acc.names.add(s)
    return acc

def inc_count(acc):
    if acc is None:
        return Acc(count=1, names=set())
    acc.count += 1
    return acc

def is_member(s, acc):
    if acc is None:
        return False
    return s in acc.names

def name_count(acc):
    if acc is None:
        return 0
    return acc.count

def check_rule(instructions):
    code = "DL3022"
    severity = "DLWarningC"
    message = "`COPY --from` should reference a previously defined `FROM` alias"

    errors = []
    acc = None

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM"):
            parts = instruction.split()
            if len(parts) > 2 and parts[2] == "AS":
                alias = parts[3]
                acc = inc_and_add_name(alias, acc)
            else:
                acc = inc_count(acc)
        elif instruction.startswith("COPY"):
            parts = instruction.split()
            if "--from" in parts:
                src = parts[parts.index("--from") + 1]
                if ":" in drop_quotes(src):
                    continue
                if not is_member(src, acc):
                    try:
                        v = int(src)
                        if v >= name_count(acc):
                            errors.append({
                                "line": line,
                                "code": code,
                                "severity": severity,
                                "message": message
                            })
                    except ValueError:
                        errors.append({
                            "line": line,
                            "code": code,
                            "severity": severity,
                            "message": message
                        })

    return errors

# Example usage
dockerfile_instructions = [
    "FROM alpine AS base",
    "FROM base AS builder",
    "COPY --from=base /src /dst",
    "COPY --from=builder /src /dst",
    "COPY --from=invalid /src /dst"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
