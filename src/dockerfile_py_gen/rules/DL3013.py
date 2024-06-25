import re

vcs_schemes = [
    "git+file", "git+https", "git+ssh", "git+http", "git+git", "git",
    "hg+file", "hg+http", "hg+https", "hg+ssh", "hg+static-http",
    "svn", "svn+svn", "svn+http", "svn+https", "svn+ssh",
    "bzr+http", "bzr+https", "bzr+ssh", "bzr+sftp", "bzr+ftp", "bzr+lp"
]

def strip_install_prefix(args):
    if "install" in args:
        return args[args.index("install") + 1:]
    return args

def is_vcs(package):
    return any(package.startswith(scheme) for scheme in vcs_schemes)

def has_version_symbol(package):
    version_symbols = ["==", ">=", "<=", ">", "<", "!=", "~=", "==="]
    return any(symbol in package for symbol in version_symbols)

def is_local_package(package):
    local_package_file_extensions = [".whl", ".tar.gz"]
    return any(package.endswith(ext) for ext in local_package_file_extensions)

def is_no_vcs_path_source(package):
    return "/" in package and not is_vcs(package)

def version_fixed(package):
    return has_version_symbol(package) or is_vcs(package) or is_local_package(package) or is_no_vcs_path_source(package)

def requirement_install(args):
    return any(arg in ["--requirement", "-r", "."] for arg in args)

def forgot_to_pin_version(args):
    return (
        "pip" in args and "install" in args and not requirement_install(args)
        and not any(version_fixed(package) for package in strip_install_prefix(args))
    )

def check_rule(instructions):
    code = "DL3013"
    severity = "DLWarningC"
    message = (
        "Pin versions in pip. Instead of `pip install <package>` use `pip install "
        "<package>==<version>` or `pip install --requirement <requirements file>`"
    )

    errors = []

    for line_num, instruction in enumerate(instructions):
        line = line_num + 1
        if instruction.startswith("RUN"):
            args = instruction.split(" ", 1)[1].strip().split()
            if forgot_to_pin_version(args):
                errors.append({
                    "line": line,
                    "code": code,
                    "severity": severity,
                    "message": message
                })

    return errors

# Example usage
dockerfile_instructions = [
    "RUN pip install somepackage",
    "RUN pip install somepackage==1.0",
    "RUN pip install -r requirements.txt"
]

errors = check_rule(dockerfile_instructions)
for error in errors:
    print(f"Error at line {error['line']}: {error['message']} ({error['code']})")
