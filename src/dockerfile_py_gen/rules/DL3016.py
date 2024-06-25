import re

git_prefixes = ["git://", "git+ssh://", "git+http://", "git+https://"]
path_prefixes = ["/", "./", "../", "~/"]
tarball_suffixes = [".tar", ".tar.gz", ".tgz"]

def strip_install_prefix(args):
    if "install" in args:
        return args[args.index("install") + 1:]
    return args

def has_git_prefix(package):
    return any(package.startswith(prefix) for prefix in git_prefixes)

def has_tarball_suffix(package):
    return any(package.endswith(suffix) for suffix in tarball_suffixes)

def is_folder(package):
    return any(package.startswith(prefix) for prefix in path_prefixes)

def is_versioned_git(package):
    return "#" in package

def has_version_symbol(package):
    return "@" in package.lstrip('@').split('/')[0]

def version_fixed(package):
    return (
        has_git_prefix(package) and is_versioned_git(package) or
        has_tarball_suffix(package) or
        is_folder(package) or
        has_version_symbol(package)
    )

def is_npm_install(cmd):
    return "npm install" in cmd

def install_is_first(cmd):
    args = cmd.split()
    return "install" in args and args.index("install") == 0

def forgot_to_pin_version(cmd):
    return is_npm_install(cmd) and install_is_first(cmd) and not all(version_fixed(pkg) for pkg in strip_install_prefix(cmd.split()))

def fold_arguments(check_func, args):
    return all(check_func(arg) for arg in args.split("&&"))

def check_rule(instructions):
    code = "DL3016"
    severity = "DLWarningC"
    message = (
        "Pin versions in npm. Instead of `npm install <package>` use `npm install "
        "<package>@<version>`"
    )

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip()
            if not fold_arguments(forgot_to_pin_version, args):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
dockerfile_instructions = [
    "RUN npm install somepackage",
    "RUN npm install somepackage@1.0",
    "RUN npm install git+https://github.com/user/repo#commit"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
