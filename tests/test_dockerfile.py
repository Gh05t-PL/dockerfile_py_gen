import unittest
from dockerfile_py_gen.dockerfile import Dockerfile

class TestDockerfile(unittest.TestCase):
    def test_dockerfile_generation(self):
        df = Dockerfile()
        df.from_('python:3.9-slim')
        df.label('maintainer', 'you@example.com')
        df.run('apt-get update && apt-get install -y gcc')
        df.copy('.', '/app')
        df.workdir('/app')
        df.run('pip install -r requirements.txt')
        df.cmd('["python", "app.py"]')

        expected_output = (
            "FROM python:3.9-slim\n"
            "LABEL maintainer=\"you@example.com\"\n"
            "RUN apt-get update && apt-get install -y gcc\n"
            "COPY . /app\n"
            "WORKDIR /app\n"
            "RUN pip install -r requirements.txt\n"
            "CMD [\"python\", \"app.py\"]"
        )

        self.assertEqual(df.render(), expected_output)

if __name__ == '__main__':
    unittest.main()
