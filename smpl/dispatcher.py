import argparse
import pprint
import os
import json
from typing import Any, List, Union

import yaml
from types import SimpleNamespace as Namespace

from smpl.boost import Boost
from smpl.openssl import OpenSSL
from smpl.cert_lib import CertLib
from smpl.simple_buffer import SimpleBuffer
from smpl.trog import Trog
from smpl.http_parser import HttpParser
from smpl.nodejs_http_parser import NodeJsHttpParser
from smpl.nodejs_llhttp import NodeJsLLHttp
from smpl.uri_parser import UriParser
from smpl.cxxurl import CxxUrl
from smpl.catch2 import Catch2
from smpl.nlohmann_json import NLohmannJson
from smpl.doctest import Doctest
from smpl.cli_package import CLIPackage
from smpl.ncurses import NCurses
import smpl.clean as clean

import smpl.config_file as configuration

pp = pprint.PrettyPrinter(indent=4)

handler_table = {
    "boost": lambda name, parms, cfg_obj: Boost(name, parms, cfg_obj),
    "openssl": lambda name, parms, cfg_obj: OpenSSL(name, parms, cfg_obj),
    "cert_lib": lambda name, parms, cfg_obj: CertLib(name, parms, cfg_obj),
    "simple_buffer": lambda name, parms, cfg_obj: SimpleBuffer(name, parms, cfg_obj),
    "trog": lambda name, parms, cfg_obj: Trog(name, parms, cfg_obj),
    "http_parser": lambda name, parms, cfg_obj: HttpParser(name, parms, cfg_obj),
    "nodejs_http_parser": lambda name, parms, cfg_obj: NodeJsHttpParser(name, parms, cfg_obj),
    "nodejs_llhttp": lambda name, parms, cfg_obj: NodeJsLLHttp(name, parms, cfg_obj),
    "uri-parser": lambda name, parms, cfg_obj: UriParser(name, parms, cfg_obj),
    "cxxurl": lambda name, parms, cfg_obj: CxxUrl(name, parms, cfg_obj),
    "catch2": lambda name, parms, cfg_obj: Catch2(name, parms, cfg_obj),
    "doctest": lambda name, parms, cfg_obj: Doctest(name, parms, cfg_obj),
    "nlohmann_json": lambda name, parms, cfg_obj: NLohmannJson(name, parms, cfg_obj),
    "cli11": lambda name, parms, cfg_obj: CLIPackage(name, parms, cfg_obj),
    "ncurses": lambda name, parms, cfg_obj: NCurses(name, parms, cfg_obj),
}


def package_handler(name: str, parms: Any, cfg_obj: configuration.ConfigObject) -> Any:
    if name not in handler_table:
        raise ValueError("invalid action name={}".format(name))

    handler = handler_table[name](name, parms, cfg_obj)
    return handler


def dispatch_all(subcmd, cfg_obj):
    if subcmd == "clean":
        clean.clean_install_dirs(cfg_obj)
    else:
        for pkg in cfg_obj.dependencies:
            parms = cfg_obj.dependencies[pkg]
            dispatch_package(pkg, subcmd, parms, cfg_obj)

def dispatch_package(package_name: str, subcmd: str, parms: Any, cfg_obj: configuration.ConfigObject) -> None:
    h = package_handler(package_name, parms, cfg_obj)
    if subcmd == "all":
        h.get_package()
        h.stage_package()
        h.install_package()
    elif subcmd == "download":
        h.get_package()
    elif subcmd == "build":
        h.stage_package()
    elif subcmd == "install":
        h.install_package()
    elif subcmd == "list":
        print(h.list_package())
    pass

def dispatch(subcmd: str, arg: Union[str, None], cfg_obj: configuration.ConfigObject) -> None:
    if subcmd not in ["download", "build", "all", "install", "clean", "list"]:
        raise ValueError("subcmd : {} is invalid".format(subcmd))
    if subcmd in ["clean","list"] and arg is not None:
        raise ValueError("subcmd clean/list cannot have an argument - given {} is invalid".format(arg))
    if arg is not None:
        if arg not in handler_table:
            raise ValueError("arg {} is an invalid package name - unknown to smpl".format(arg))
        if arg not in cfg_obj.dependencies:
            raise ValueError("arg {} is an invalid package name - not in the config file".format(arg))

    ok: bool = True
    msg: str = ""
    for n in cfg_obj.dependencies:
        if n not in handler_table:
            print("package name : {} in config file is invalid".format(n))
            ok = False
    if not ok:
        raise ValueError("one or more packages named in the config file are invalid names")
    if arg is None:
        dispatch_all(subcmd, cfg_obj)
    else:
        parms: Any = cfg_obj.dependencies[arg]
        dispatch_package(arg, subcmd, parms, cfg_obj)
    pass
