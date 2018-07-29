#!/usr/bin/python
#
# Copyright 2012 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import collections
import sys
import yaml
import json
import os

import six


class YamlOrderedLoader(yaml.SafeLoader):
    """Specialized Loader which respects order."""


def construct_mapping(loader, node):
    loader.flatten_mapping(node)
    return collections.OrderedDict(loader.construct_pairs(node))

YamlOrderedLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping)


def yaml_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    def unicode_representer(dumper, uni):
        node = yaml.ScalarNode(tag=u'tag:yaml.org,2002:str', value=uni)
        return node
    OrderedDumper.add_representer(collections.OrderedDict, _dict_representer)
    OrderedDumper.add_representer(collections.defaultdict, _dict_representer)
    OrderedDumper.add_representer(six.text_type, unicode_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


def yaml_load(data):
    return yaml.load_all(data, Loader=YamlOrderedLoader)


def main():
    infile_path = sys.argv[1]
    if infile_path == '-':
        infile = sys.stdin
    else:
        infile = open(infile_path)

    if len(sys.argv) > 2:
        indent = int(sys.argv[2])
    else:
        indent = 2

    intext = infile.read()
    try:
        x = json.loads(intext, object_pairs_hook=collections.OrderedDict)
    except ValueError as e:
        if 'debug' in sys.argv:
            sys.stderr.write(str(e))
        x = yaml_load(intext)
        for doc in x:
            if indent:
                print(json.dumps(doc, indent=indent,
                                 separators=(',', ': '), sort_keys=False,
                                 default=six.text_type))
            else:
                print(json.dumps(doc, sort_keys=False))
    else:
        if 'flow' in sys.argv:
            flow=True
        else:
            flow=False
        print(yaml_dump(x, default_flow_style=flow))


if __name__ == '__main__':
    main()
