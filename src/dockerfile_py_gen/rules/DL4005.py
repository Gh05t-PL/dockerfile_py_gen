from typing import List, Dict

def check_rule(shell_scripts: List[str]) -> List[Dict]:
    errors = []

    for idx, script in enumerate(shell_scripts):
        if contains_unsafe_shell_change(script):
            errors.append({
                'code': 'DL4005',
                'severity': 'DLWarningC',
                'message': "Use SHELL to change the default shell",
                'line': idx + 1
            })

    return errors

def contains_unsafe_shell_change(script: str) -> bool:
    if script.startswith("RUN "):
        commands = script[4:].strip().split(" && ")
        for cmd in commands:
            if cmd.startswith("ln ") and "/bin/sh" in cmd.split():
                return True
    return False

# Example usage
shell_scripts = [
    "RUN ln -sf /bin/bash /bin/sh",
    "RUN apt-get update && apt-get install -y curl",
    "RUN apt-get install -y wget",
]

errors = check_rule(shell_scripts)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
