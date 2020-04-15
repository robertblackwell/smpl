#!/usr/bin/env python3

import sys
import argparse
import datetime
import pprint
import optparse
import os
import subprocess
import json
import yaml
import copy
from types import SimpleNamespace as Namespace


class BasicObject(object):
    def __init__(self):
        pass

    def setKeyValue(self, k, v):
        self.__dict__[k] = v


def parse_to_object(thing):
    if isinstance(thing, dict):
        obj = BasicObject() 
        for k2 in thing:
            obj.setKeyValue(k2, parse_to_object(thing[k2]))
        return obj
    
    elif isinstance(thing, list):
        lst = []
        for ent in thing:
            lst.append(parse_to_object(ent))
        return lst
    
    else:
        return thing


def merge_objects(obj_of_values, obj_of_default_values):
    """
    obj_of_values represents a sub sets of values, for example a selection of options values.
    obj_of_default_values represents the complete list of possible option values and their default values

    returns obj_of_values with all missing properties set to the values in obj_of_default_values.
    """
    if not (isinstance(obj_of_values, object) and isinstance(obj_of_default_values, object)):
        raise ValueError("merge_objects one of the arguments is not an object")
    
    new_obj_of_values = copy.deepcopy(obj_of_values)
    d1 = new_obj_of_values.__dict__
    d2 = obj_of_default_values.__dict__
    keys = list(d2.keys())
    for k in keys:
        v = d2[k]
        if not (k in d1.keys()):
            d1[k] = v
        elif d1[k] is None:
            d1[k] = v
    return new_obj_of_values

