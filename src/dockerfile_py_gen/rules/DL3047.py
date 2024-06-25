def is_wget(cmd):
    return "wget" in cmd

def has_progress_option(cmd):
    return "--progress" in cmd

def has_special_flags(cmd):
    return (any(flag in cmd for flag in ["-q", "--quiet", "-nv", "--no-verbose"]) or
            any(flag in cmd for flag in ["-o", "--output-file", "-a", "--append-output"]))

def forgot_progress(cmd):
    return is_wget(cmd) and not has_progress_option(cmd) and not has_special_flags(cmd)

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3047"
    severity = "DLInfoC"
    message = "Avoid use of wget without progress bar. Use `wget --progress=dot:giga <url>`. Or consider using `-q` or `-nv` (shorthands for `--quiet` or `--no-verbose`)."

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(forgot_progress, args):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "RUN wget http://example.com",
#     "RUN wget --progress=dot:giga http://example.com",
#     "RUN wget -q http://example.com"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
