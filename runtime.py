#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker
from pod import Pod
from abc import ABC, abstractmethod


class Runtime(ABC):
    """ Runtime interface for running Pods. """

    @abstractmethod
    def run(self, srv: Pod):
        """ Run the pod using runtime. """
        pass

    @abstractmethod
    def list(self) -> list:
        """ returns a list of all containers. """
        pass


class DockerRuntime(Runtime):
    """ Docker runtime to run Pods. """

    def __init__(self):
        """ Initialize connection to localhost docker engine. """

        self.client = docker.from_env()
        self._labels = {"orchestrator": "kubeleet"}
        self._restart_policy = {"Name": "always", "MaximumRetryCount": 0}

    def run(self, srv: Pod):
        """ Run the (single-container) pod on current host. """

        container = self.client.containers.run(
            image=srv.image,
            name=srv.unique_name,
            network_mode="host",
            labels=self._labels,
            detach=True,
            restart_policy=self._restart_policy,
        )

    def list(self) -> list:
        """ returns a list of all containers (docker ps). """
        labels = []
        for k, v in self._labels.items():
            labels.append("{}={}".format(k, v))

        #TODO: return names
        containers = self.client.containers.list(filters={"label": labels})
        return list(map(lambda s: s.name, containers))
