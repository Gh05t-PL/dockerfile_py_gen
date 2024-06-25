def drop_quotes(path):
    return path.strip('"').strip("'")

def ends_with_slash(target_path):
    return target_path.endswith('/')

def check_rule(instructions):
    code = "DL3021"
    severity = "DLErrorC"
    message = "COPY with more than 2 arguments requires the last argument to end with /"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("COPY"):
            parts = instruction.split()
            sources = parts[1:-1]
            target = parts[-1]
            if len(sources) > 1 and not ends_with_slash(drop_quotes(target)):
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
#     "COPY file1.txt file2.txt /app/",
#     "COPY file1.txt /app",
#     "COPY file1.txt file2.txt file3.txt /app"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
