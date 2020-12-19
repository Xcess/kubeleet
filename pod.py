#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from hashlib import shake_256


class Pod:
    """ Represents a service in orchestrator. """

    def __init__(self, name, uuid, image, replica, json=""):

        self.name = name
        self.uuid = uuid
        self.image = image
        self.replica = replica
        self.json = json

        self.hash = shake_256(self.json.encode()).hexdigest(8)
        self.unique_name = "{}-{}-{}".format(self.name, self.replica, self.hash)[-200:]


    @classmethod
    def from_json(cls, obj):

        pod_dict = json.loads(obj)
        return cls(
            name=pod_dict["name"],
            uuid=pod_dict["uuid"],
            image=pod_dict["image"],
            replica=pod_dict["replica"],
            json=obj,
        )
