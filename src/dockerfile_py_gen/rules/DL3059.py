def check_rule(instructions):
    errors = []
    consecutive_run_count = 0
    current_flags = None

    for idx, instruction in enumerate(instructions):
        if instruction.startswith("RUN"):
            parts = instruction.split(maxsplit=1)
            if len(parts) == 2:
                command = parts[1]
                flags = extract_flags(command)
                if current_flags is None:
                    current_flags = flags
                    consecutive_run_count = 1
                elif current_flags != flags:
                    current_flags = flags
                    consecutive_run_count = 1
                else:
                    consecutive_run_count += 1

                if consecutive_run_count > 2:
                    errors.append({
                        'code': 'DL3059',
                        'severity': 'DLInfoC',
                        'message': "Multiple consecutive `RUN` instructions. Consider consolidation.",
                        'line': idx + 1
                    })

    return errors

def extract_flags(command: str) -> str:
    # Logic to extract flags from the RUN command
    # Assuming a simple extraction for demonstration purposes
    # Adjust as per actual flag extraction logic in your use case
    return ""  # Replace with actual flag extraction logic

# Example usage
dockerfile_instructions = [
    "RUN apt-get update && apt-get install -y python3",
    "RUN pip install requests",
    "RUN mkdir /app",
    "RUN chmod +x /app/script.sh",
    "RUN --mount=type=bind,source=/src,target=/dest cp /src/file /dest",
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
