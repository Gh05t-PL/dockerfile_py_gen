import unittest
from dockerfile_py_gen.hadolint import Hadolint


class TestHadolint(unittest.TestCase):
    def dockerfile_1(self):
        return (
            'FROM python:3.9-slim\n'
            'LABEL maintainer="you@example.com"\n'
            'RUN apt-get update && apt-get install -y gcc\n'
            'COPY . /app\n'
            'WORKDIR /app\n'
            'RUN pip install -r requirements.txt\n'
            'CMD ["python", "app.py"]\n'
        )

    def dockerfile_2(self):
        return (
            'FROM python:3.9-slim\n'
            'LABEL maintainer="you@example.com"\n'
            'RUN apt-get update && apt-get install -y gcc\n'
            'COPY . /app\n'
            'WORKDIR /app\n'
            'RUN pip install -r requirements.txt\n'
            'CMD ["python", "app.py"]\n'
            'Hello Error'
        )

    def test_lint_error(self):
        hadolint = Hadolint(self.dockerfile_2())
        issues = hadolint.get_issues()

        self.assertIsInstance(issues, list)
        self.assertEqual(issues[0]['level'], 'error')
        self.assertEqual(issues[0]['line'], 8)
        self.assertEqual(len(issues), 1)

    def test_lint_pass(self):
        hadolint = Hadolint(self.dockerfile_1())
        issues = hadolint.get_issues()

        self.assertIsInstance(issues, list)
        self.assertEqual(len(issues), 0)


if __name__ == '__main__':
    unittest.main()
