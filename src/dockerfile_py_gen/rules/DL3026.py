class State:
    def __init__(self, aliases=None):
        self.aliases = aliases if aliases is not None else set()

def match_registry(allow, registry):
    if allow == "*":
        return True
    if allow.startswith("*"):
        return registry.endswith(allow[1:])
    if allow.endswith("*"):
        return registry.startswith(allow[:-1])
    return registry == allow

def is_allowed_image(image, allowed):
    if image.startswith("docker.io") or image.startswith("hub.docker.com") or image == "scratch":
        return True
    registry = image.split('/')[0] if '/' in image else ''
    return any(match_registry(allow, registry) for allow in allowed)

def check_rule(instructions, allowed_registries):
    code = "DL3026"
    severity = "DLErrorC"
    message = "Use only an allowed registry in the FROM image"

    errors = []
    state = State()

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM"):
            parts = instruction.split()
            image = parts[1]
            alias = parts[3] if len(parts) > 3 and parts[2] == "AS" else None
            state.aliases.add(alias)
            if not is_allowed_image(image, allowed_registries):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
dockerfile_instructions = [
    "FROM docker.io/alpine AS base",
    "FROM unauthorized.registry/alpine AS builder",
    "FROM scratch"
]

allowed_registries = {"docker.io", "hub.docker.com"}

errors = check_rule(dockerfile_instructions, allowed_registries)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
# TODO add passing
