def is_archive(path):
    archive_file_format_extensions = [".tar", ".gz", ".bz2", ".xz", ".zip", ".rar", ".7z"]
    return any(path.endswith(ftype) for ftype in archive_file_format_extensions)

def is_url(path):
    return path.startswith("https://") or path.startswith("http://")

def drop_quotes(path):
    return path.strip('"').strip("'")

def check_rule(instructions):
    code = "DL3020"
    severity = "DLErrorC"
    message = "Use COPY instead of ADD for files and folders"

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("ADD"):
            parts = instruction.split()
            srcs = parts[1:-1]
            if not all(is_archive(drop_quotes(src)) or is_url(drop_quotes(src)) for src in srcs):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
dockerfile_instructions = [
    "ADD file.tar.gz /app/",
    "ADD https://example.com/file.zip /app/",
    "ADD file.txt /app/"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
