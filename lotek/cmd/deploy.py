import subprocess

from lotek.lib.colors import green, red
from lotek.lib.dirs import dirs
from lotek.cmd.build import cmd_build

def read_env():
    env_path = dirs.CWD / ".env"
    if not env_path.exists():
        return {}
    env = {}
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


def cmd_deploy(skip_build=False):
    env = read_env()
    user, host, path = (
        env.get("DEPLOY_USER"),
        env.get("DEPLOY_HOST"),
        env.get("DEPLOY_PATH"),
    )
    if not all([user, host, path]):
        print(red("Missing DEPLOY_USER, DEPLOY_HOST, or DEPLOY_PATH in .env"))
        return 1
    if not skip_build:
        print(green("Building..."))
        rc = cmd_build()
        if rc != 0:
            return rc
    dest = f"{user}@{host}:{path}/"
    print(green(f"Deploying to {dest}"))
    result = subprocess.run(
        [
            "rsync",
            "-avz",
            "--exclude=.env",
            "--exclude=*.pyc",
            "--exclude=__pycache__",
            "--exclude=output",
            "output/",
            dest,
        ]
    )
    if result.returncode != 0:
        print(red("Deploy failed"))
        return result.returncode
    print(green("Deployed successfully"))
    return 0
