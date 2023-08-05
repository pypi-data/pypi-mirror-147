import logging
import shlex
import subprocess
import sys

log = logging.getLogger(__name__)


def run(cmd):
    log.debug(shlex.join(cmd))
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out, err = proc.communicate()
    return_code = proc.poll()
    out = out.decode(sys.stdin.encoding)
    err = err.decode(sys.stdin.encoding)

    ex = subprocess.CalledProcessError(return_code, cmd=shlex.join(cmd), output=out)
    ex.stdout, ex.stderr = out, err
    log.debug(proc.returncode, err, out)

    if proc.returncode not in [0]:
        raise ex


def main(cfg):

    cmd_sync = [
        "aws",
        "s3",
        "sync",
        str(cfg.app.s3bucket.path_work),
        cfg.app.s3bucket.endpoint,
        "--region",
        "us-west-2",
        "--no-progress",
        "--acl",
        "public-read",
    ]

    raise NotImplementedError
    if not cfg.app.stop_all_uploads:
        run(cmd_sync)
