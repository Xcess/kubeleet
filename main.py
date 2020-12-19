#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
from runtime import DockerRuntime
from engine import Engine
from helper import Config, log

CONF = Config("./kubeleet.conf")

PENDING_QUEUE = CONF.get("redis", "pending_queue")
RUNNING_QUEUE = CONF.get("redis", "running_queue")
CONTAINERS_SET = CONF.get("redis", "containers_set")

if CONF.has_option("redis", "password"):
    REDIS_PASSWORD = CONF.get("redis", "password")
else:
    REDIS_PASSWORD = None
REDIS = redis.Redis(
    host=CONF.get("redis", "host"),
    port=CONF.get("redis", "port"),
    db=CONF.getint("redis", "db"),
    password=REDIS_PASSWORD,
    decode_responses=True,
)


def main():
    """ Init. function of kubeleet. """
    docker_runtime = DockerRuntime()
    engine = Engine(
        runtime=docker_runtime,
        redis=REDIS,
        pending_queue=PENDING_QUEUE,
        running_queue=RUNNING_QUEUE,
        containers_set=CONTAINERS_SET,
    )
    log("Starting listening for events...")
    engine.start()


if __name__ == "__main__":
    main()