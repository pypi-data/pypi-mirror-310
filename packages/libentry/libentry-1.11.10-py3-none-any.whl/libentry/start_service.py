#!/usr/bin/env python3

__author__ = "xi"

import os
import subprocess
from cgi import parse
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel, Field

from libentry import ArgumentParser


class Config(BaseModel):
    exec: str = Field()
    envs: Dict[str, str] = Field(default_factory=dict)
    stdout: Optional[str] = Field(default="-")
    stderr: Optional[str] = Field(default="-")


class Status(BaseModel):
    pid: int = Field()


def main():
    parser = ArgumentParser()
    parser.add_argument("--config_dir", "-d")
    parser.add_argument("--config_filename", "-f", default="config.json")
    parser.add_argument("--status_filename", default="status.json")
    args = parser.parse_args()

    config_dir = args.config_dir
    if config_dir is None:
        config_dir = os.getcwd()
    config_dir = os.path.abspath(config_dir)
    os.chdir(config_dir)

    if not os.path.exists(args.config_filename):
        raise FileNotFoundError(f"Cannot find \"{args.config_filename}\".")

    with open(args.config_filename) as f:
        config = Config.model_validate(yaml.safe_load(f))

    if config.stdout == "-":
        stdout = None
    elif config.stdout is None:
        stdout = subprocess.DEVNULL
    else:
        stdout = open(config.stdout, "a")
    if config.stderr == "-":
        stderr = None
    elif config.stderr is None:
        stderr = subprocess.DEVNULL
    else:
        stderr = open(config.stderr, "a")

    process = subprocess.Popen(
        ["/bin/bash", "-c", config["exec"]],
        cwd=os.getcwd(),
        env={**os.environ, **config.envs} if len(config.envs) > 0 else None,
        preexec_fn=os.setpgrp,
        stdout=stdout,
        stderr=stderr
    )
    pgid = os.getpgid(process.pid)
    with open(PID_FILENAME, "w") as f:
        f.write(str(pgid))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
