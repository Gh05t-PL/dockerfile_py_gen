from typing import List, Dict

def check_rule(shell_scripts: List[str]) -> List[Dict]:
    errors = []
    state = False  # Initial state

    for idx, script in enumerate(shell_scripts):
        if script.startswith("FROM "):
            state = False  # Reset state for each new FROM statement
        elif script.startswith("RUN "):
            if contains_pipe(script):
                if not state and not contains_shell_option(script):
                    errors.append({
                        'code': 'DL4006',
                        'severity': 'DLWarningC',
                        'message': ("Set the SHELL option -o pipefail before RUN with a pipe in it. "
                                    "If you are using /bin/sh in an alpine image or if your shell is "
                                    "symlinked to busybox then consider explicitly setting your SHELL to "
                                    "/bin/ash, or disable this check"),
                        'line': idx + 1
                    })
            state = True if contains_pipe(script) else False

    return errors

def contains_pipe(script: str) -> bool:
    return " | " in script or script.strip().endswith(" |")

def contains_shell_option(script: str) -> bool:
    # Check if the script sets the SHELL option with -o pipefail
    tokens = script.split()
    return any(token == "SHELL" and "-o" in tokens[i+1:i+3] and tokens[i+2] == "pipefail"
               for i, token in enumerate(tokens[:-2]))

# Example usage
shell_scripts = [
    "FROM alpine",
    "RUN apt-get update && apt-get install -y curl",
    "RUN set -o pipefail && apt-get install -y wget",
    "RUN apk update | apk add --no-cache bash && echo 'Hello World'",
]

errors = check_rule(shell_scripts)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
