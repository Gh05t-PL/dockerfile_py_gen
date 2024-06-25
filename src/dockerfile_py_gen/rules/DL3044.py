def check_rule(instructions):
    code = "DL3044"
    severity = "DLErrorC"
    message = "Do not refer to an environment variable within the same ENV statement where it is defined."

    env_state = set()

    failures = []
    for line_num, instruction in enumerate(instructions):
        instruction = instruction.strip()

        if instruction.startswith("ENV"):
            pairs = parse_env_instruction(instruction[4:])
            new_env_vars = {var for var, _ in pairs}

            if any(env_var in new_env_vars for env_var in list_of_references(pairs)):
                failures.append({
                    "code": code,
                    "severity": severity,
                    "message": message,
                    "line": line_num + 1
                })

            env_state.update(new_env_vars)

        elif instruction.startswith("ARG"):
            arg = instruction[4:].strip()
            env_state.add(arg)


    return failures

def parse_env_instruction(instruction):
    pairs = []
    env_vars = instruction.split()
    for env_var in env_vars:
        if "=" in env_var:
            var, value = env_var.split("=", 1)
            pairs.append((var, value))
    return pairs

def list_of_references(pairs):
    references = []
    for idx, (var, _) in enumerate(pairs):
        for _, (other_var, value) in enumerate(pairs):
            if idx != _ and is_substring_of_any(var, [value]):
                references.append(var)
    return references

def is_substring_of_any(t, l):
    for v in l:
        if f"${{{t}}}" in v or bare_variable_in_text(t, v):
            return True
    return False

def bare_variable_in_text(v, t):
    var = f"${v}"
    rest = t.split(var)[1:]
    return var in t and any(terminates_var_name(r) for r in rest)

def terminates_var_name(x):
    return not x or not begins_with_any_of(x, var_char())

def begins_with_any_of(txt, char_set):
    return any(txt.startswith(c) for c in char_set)

def var_char():
    return set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')
