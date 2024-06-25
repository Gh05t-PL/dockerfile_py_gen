def is_var_cache_apk(path):
    return path.rstrip('/') == "/var/cache/apk"

def is_cache_mount(mount):
    return is_var_cache_apk(mount)

def has_cache_mount(flags):
    return any(is_cache_mount(flag) for flag in flags)

def forgot_cache_option(cmd):
    return "apk add" in cmd and "--no-cache" not in cmd.split()

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3019"
    severity = "DLInfoC"
    message = (
        "Use the `--no-cache` switch to avoid the need to use `--update` and "
        "remove `/var/cache/apk/*` when done installing packages"
    )

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            parts = instruction.split(" ", 1)
            args = parts[1].strip() if len(parts) > 1 else ""
            flags = []  # Assuming flags can be parsed from the instruction if needed
            if not has_cache_mount(flags) and not fold_arguments(forgot_cache_option, args):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
dockerfile_instructions = [
    "RUN apk update && apk add curl",
    "RUN apk add --no-cache wget",
    "RUN apk add --update bash && rm -rf /var/cache/apk/*"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
