import subprocess

from lotek.lib.logger import log
from lotek.cmd.build import cmd_build

def read_env(dirs):
    env_path = dirs.CWD / ".env"
    if not env_path.exists():
        return {}
    env = {}
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


def cmd_deploy(dirs, skip_build=False):
    env = read_env(dirs)
    user, host, path = (
        env.get("DEPLOY_USER"),
        env.get("DEPLOY_HOST"),
        env.get("DEPLOY_PATH"),
    )
    if not all([user, host, path]):
        log.error("Missing DEPLOY_USER, DEPLOY_HOST, or DEPLOY_PATH in .env")
        return 1
    if not skip_build:
        log.info("Building...")
        rc = cmd_build(dirs)
        if rc != 0:
            return rc
    dest = f"{user}@{host}:{path}/"
    log.info("Deploying to %s", dest)
    result = subprocess.run(s
        [
            "rsync",
            "-avz",
            "--exclude=.env",
            "--exclude=*.pyc",
            "--exclude=__pycache__",
            "--exclude=output",
            "output/",
            dest,
        ],
        check=False
    )
    if result.returncode != 0:
        log.error("Deploy failed %s: %s", result.returncode, result.stderr.decode())
        return result.returncode
    log.info("Deployed successfully")
    return 0
