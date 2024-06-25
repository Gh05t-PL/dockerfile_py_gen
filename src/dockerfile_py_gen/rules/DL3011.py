def check_rule(instructions):
    code = "DL3011"
    severity = "DLErrorC"
    message = "Valid UNIX ports range from 0 to 65535"

    errors = []

    def is_valid_port(port):
        return 0 <= port <= 65535

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("EXPOSE"):
            ports = instruction.split()[1:]
            valid = True
            for port in ports:
                if '-' in port:
                    start, end = map(int, port.split('-'))
                    if not (is_valid_port(start) and is_valid_port(end)):
                        valid = False
                        break
                else:
                    if not is_valid_port(int(port)):
                        valid = False
                        break
            if not valid:
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
#     "FROM ubuntu:latest",
#     "EXPOSE 8080",
#     "EXPOSE 70000",
#     "EXPOSE 1024-2048",
#     "EXPOSE 1024-70000"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
