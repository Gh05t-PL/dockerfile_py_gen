from collections import defaultdict
import re

class Acc:
    def __init__(self, last_from=None, docker_clean=True, stages=None, forgets=None):
        self.last_from = last_from
        self.docker_clean = docker_clean
        self.stages = stages if stages is not None else {}
        self.forgets = forgets if forgets is not None else {}

    def __eq__(self, other):
        return (self.last_from, self.docker_clean, self.stages, self.forgets) == (other.last_from, other.docker_clean, other.stages, other.forgets)

    def __repr__(self):
        return f"Acc(last_from={self.last_from}, docker_clean={self.docker_clean}, stages={self.stages}, forgets={self.forgets})"

def is_cache_mount(dir, mount):
    return any(dir in m for m in mount)

def has_cache_directory(dir, flags):
    return is_cache_mount(dir, flags)

def remember_stage(line, from_image, acc):
    acc.stages[from_image['image']] = line
    acc.last_from = from_image
    return acc

def remember_line(line, acc):
    acc.forgets[line] = acc.last_from
    return acc

def remember_docker_clean(acc):
    acc.docker_clean = False
    return acc

def forgot_to_cleanup(args):
    has_update = any("apt-get update" in cmd for cmd in args.split("&&"))
    has_cleanup = any("rm -rf /var/lib/apt/lists/*" in cmd for cmd in args.split("&&"))
    return has_update and not has_cleanup

def disabled_docker_clean(args):
    removes_script = any("rm /etc/apt/apt.conf.d/docker-clean" in cmd for cmd in args.split("&&"))
    keeps_packages = any("echo 'Binary::apt::APT::Keep-Downloaded-Packages \"true\";'" in cmd for cmd in args.split("&&"))
    return removes_script or keeps_packages

def check_rule(instructions):
    code = "DL3009"
    severity = "DLInfoC"
    message = "Delete the apt-get lists after installing something"

    errors = []
    acc = Acc()

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM"):
            parts = instruction.split()
            base_image = {'image': parts[1]}
            acc = remember_stage(line, base_image, acc)
        elif instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not forgot_to_cleanup(args):
                if disabled_docker_clean(args):
                    acc = remember_docker_clean(acc)
                else:
                    acc = remember_line(line, acc)
            elif has_cache_directory("/var/lib/apt/lists", args):
                continue
            elif has_cache_directory("/var/lib/apt", args) and has_cache_directory("/var/cache/apt", args):
                continue
            else:
                acc = remember_line(line, acc)

    for line, from_image in acc.forgets.items():
        errors.append({
            "code": code,
            "severity": severity,
            "message": message,
            "line": line
        })

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "FROM ubuntu:latest",
#     "RUN apt-get update && apt-get install -y curl",
#     "RUN rm -rf /var/lib/apt/lists/*",
#     "RUN apt-get update && apt-get install -y wget"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
