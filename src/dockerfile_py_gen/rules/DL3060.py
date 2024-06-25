import re

def check_rule(instructions):
    errors = []
    from_statement_encountered = False
    last_from_line = None
    yarn_install_line = None
    yarn_cache_clean_line = None

    for idx, instruction in enumerate(instructions):
        if instruction.startswith("FROM"):
            from_statement_encountered = True
            last_from_line = idx + 1

        if instruction.startswith("RUN"):
            parts = instruction.split(maxsplit=1)
            if len(parts) == 2:
                command = parts[1]
                if yarn_install_line is None and is_yarn_install(command):
                    yarn_install_line = idx + 1
                elif yarn_cache_clean_line is None and is_yarn_cache_clean(command):
                    yarn_cache_clean_line = idx + 1

        if yarn_install_line is not None and yarn_cache_clean_line is None and from_statement_encountered:
            errors.append({
                'code': 'DL3060',
                'severity': 'DLInfoC',
                'message': "`yarn cache clean` missing after `yarn install` was run.",
                'line': last_from_line
            })
            break

    return errors

def is_yarn_install(command: str) -> bool:
    return re.search(r'\byarn\s+install\b', command) is not None

def is_yarn_cache_clean(command: str) -> bool:
    return re.search(r'\byarn\s+cache\s+clean\b', command) is not None

# Example usage
dockerfile_instructions = [
    "FROM node:14",
    "RUN yarn install",
    "RUN apt-get update && apt-get install -y python3",
    "RUN --mount=type=cache,target=/app yarn build",
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
