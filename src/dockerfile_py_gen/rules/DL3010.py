import re
from collections import defaultdict

class Acc:
    def __init__(self, archives=None, extracted=None):
        self.archives = archives if archives is not None else set()
        self.extracted = extracted if extracted is not None else set()

def is_archive(src):
    archive_extensions = [".tar", ".gz", ".bz2", ".xz", ".zip", ".rar", ".7z"]
    return any(src.endswith(ext) for ext in archive_extensions)

def basename(path):
    return path.split('/')[-1].split('\\')[-1]

def drop_quotes(text):
    return text.strip('"').strip("'")

def remember_archives(line, srcs, target, acc):
    if is_archive(target):
        acc.archives.add((line, basename(target)))
    else:
        for src in srcs:
            if is_archive(src):
                acc.archives.add((line, basename(src)))
    return acc

def mark_extracted(extracted_archives, acc):
    acc.extracted.update(extracted_archives)
    return acc

def extracts_this_archive(archive, cmd):
    cmd_name, *args = cmd.split()
    is_tar_cmd = cmd_name == "tar" and any(flag in args for flag in ["--extract", "--get", "-x"])
    is_unzip_cmd = cmd_name in ["unzip", "gunzip", "bunzip2", "unlzma", "unxz", "zgz", "uncompress", "zcat", "gzcat"]
    return is_tar_cmd or is_unzip_cmd

def get_extracted_archives(archives, shell_cmds):
    extracted_archives = set()
    for archive in archives:
        for cmd in shell_cmds:
            if extracts_this_archive(archive, cmd):
                extracted_archives.add(archive)
    return extracted_archives

def check_rule(instructions):
    code = "DL3010"
    severity = "DLInfoC"
    message = "Use `ADD` for extracting archives into an image"

    errors = []
    acc = Acc()

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("FROM"):
            acc = Acc()
        elif instruction.startswith("COPY"):
            parts = instruction.split()
            srcs = parts[1:-1]
            target = parts[-1]
            acc = remember_archives(line, srcs, target, acc)
        elif instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            extracted_archives = get_extracted_archives(acc.archives, args.split("&&"))
            acc = mark_extracted(extracted_archives, acc)

    for archive in acc.archives:
        if archive not in acc.extracted:
            errors.append({
                "line": archive[0],
                "code": code,
                "severity": severity,
                "message": message
            })

    return errors
#
# # Example usage
# dockerfile_instructions = [
#     "FROM ubuntu:latest",
#     "COPY file.tar.gz /tmp/",
#     "RUN tar -xzf /tmp/file.tar.gz"
# ]
#
# errors = check_rule(dockerfile_instructions)
# for error in errors:
#     print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
