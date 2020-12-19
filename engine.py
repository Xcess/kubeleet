#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
from helper import Config, log
from pod import Pod
from runtime import Runtime
from redis import Redis

CONF = Config("./kubeleet.conf")


class Engine:
    """ Core logic for handling service run requests on workers. """

    def __init__(
        self,
        runtime: Runtime,
        redis: Redis,
        pending_queue: str,
        running_queue: str,
        containers_set: str,
    ):
        self.runtime = runtime
        self.redis = redis
        self.pending_queue = pending_queue
        self.running_queue = running_queue
        self.containers_set = containers_set

    def start(self, threaded=False):
        """ Start processing service run requests. """

        # TODO: maybe add threading
        # TODO: add stats monitoring
        while True:

            # RQ Start
            # Code path and checks for rq and pq should be diffrenet.
            remaining = self.redis.lrange(self.running_queue, -1, -1)
            if len(remaining) != 0:
                p = Pod.from_json(remaining[0])
            else:
                p = Pod.from_json(
                    self.redis.brpoplpush(self.pending_queue, self.running_queue, 0)
                )
            log("Running {}".format(p.unique_name))
            if p.unique_name in self.runtime.list():
                log("Container {} already exists.".format(p.unique_name))
            else:
                self.runtime.run(p)

            self.redis.sadd(self.containers_set, p.json)

            # RQ Finilize
            self.redis.lrem(self.running_queue, 0, p.json)
