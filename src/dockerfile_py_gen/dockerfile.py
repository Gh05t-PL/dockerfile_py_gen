class Dockerfile:
    def __init__(self):
        self.instructions = []

    def _comment(self, comment):
        self.instructions.append(f"# {comment}")

    def _new_line(self):
        self.instructions.append("\n")

    def overrrrride(self, content):
        self.instructions.append(f"{content}")

    def from_(self, base_image):
        self.instructions.append(f"FROM {base_image}")

    def label(self, key, value):
        self.instructions.append(f"LABEL {key}=\"{value}\"")

    def run(self, command):
        self.instructions.append(f"RUN {command}")

    def copy(self, source, destination):
        self.instructions.append(f"COPY {source} {destination}")

    def add(self, source, destination):
        self.instructions.append(f"ADD {source} {destination}")

    def workdir(self, directory):
        self.instructions.append(f"WORKDIR {directory}")

    def cmd(self, command):
        self.instructions.append(f"CMD {command}")

    def entrypoint(self, entrypoint):
        self.instructions.append(f"ENTRYPOINT {entrypoint}")

    def env(self, key, value):
        self.instructions.append(f"ENV {key}={value}")

    def expose(self, port):
        self.instructions.append(f"EXPOSE {port}")

    def volume(self, volume):
        self.instructions.append(f"VOLUME {volume}")

    def user(self, user):
        self.instructions.append(f"USER {user}")

    def arg(self, arg, default_value=None):
        if default_value:
            self.instructions.append(f"ARG {arg}={default_value}")
        else:
            self.instructions.append(f"ARG {arg}")

    def onbuild(self, instruction):
        self.instructions.append(f"ONBUILD {instruction}")

    def healthcheck(self, command, interval=None, timeout=None, start_period=None, retries=None):
        healthcheck_command = f"HEALTHCHECK CMD {command}"
        if interval:
            healthcheck_command += f" --interval={interval}"
        if timeout:
            healthcheck_command += f" --timeout={timeout}"
        if start_period:
            healthcheck_command += f" --start-period={start_period}"
        if retries:
            healthcheck_command += f" --retries={retries}"
        self.instructions.append(healthcheck_command)

    def stop_signal(self, signal):
        self.instructions.append(f"STOPSIGNAL {signal}")

    def shell(self, shell):
        self.instructions.append(f"SHELL {shell}")

    def render(self):
        return "\n".join(self.instructions)

    def save(self, filename="Dockerfile"):
        with open(filename, "w") as f:
            f.write(self.render())
