import subprocess
import json
import tempfile
import importlib.resources as pkg_resources


class Hadolint:
    def __init__(self, dockerfile_content=None, failure_threshold='error', trusted_registry=[]):
        self.dockerfile_content = dockerfile_content
        self.failure_threshold = failure_threshold
        self.trusted_registry = trusted_registry
        self.hadolint_path = pkg_resources.files('dockerfile_py_gen.bin') / 'hadolint'

    def __lint(self):

        if not self.dockerfile_content:
            return "Error: No Dockerfile content provided.", 1

        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(self.dockerfile_content.encode())
            temp_file_path = temp_file.name
            temp_file.seek(0)

            try:
                result = subprocess.run(
                    [self.hadolint_path, temp_file_path, '-f', 'json', '-t', self.failure_threshold],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                    text=True
                )

                return json.loads(result.stdout), 0
            except subprocess.CalledProcessError as e:
                if e.returncode == 1:
                    return json.loads(e.stdout), e.returncode
                else:
                    return e.stderr, e.returncode

    def print_issues(self):
        issues, exit_code = self.__lint()
        if exit_code == 0:
            print("No issues found.")
        elif exit_code == 1:
            print("Error parsing Dockerfile:", issues)
        else:
            for issue in issues:
                print(f"Line {issue['line']}: {issue['message']} (rule: {issue['code']})")
            print(f"Total issues found: {len(issues)}")

    def get_issues(self):
        issues, exit_code = self.__lint()
        if exit_code == 0:
            return []
        elif exit_code == 1:
            return issues
        else:
            raise Exception("Can't parse dockerfile", issues, exit_code)
