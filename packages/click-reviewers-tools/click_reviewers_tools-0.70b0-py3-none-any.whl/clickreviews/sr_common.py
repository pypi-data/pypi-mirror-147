'''sr_common.py: common classes and functions'''
#
# Copyright (C) 2013-2016 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import os
import re
import yaml


from clickreviews.common import (
    Review,
    ReviewException,
    error,
    open_file_read,
)

import clickreviews.snapd_base_declaration as snapd_base_declaration


#
# Utility classes
#
class SnapReviewException(ReviewException):
    '''This class represents SnapReview exceptions'''


class SnapReview(Review):
    '''This class represents snap reviews'''
    snappy_required = ["name",
                       "version",
                       ]
    # optional snappy fields here (may be required by appstore)
    snappy_optional = ['apps',
                       'assumes',
                       'architectures',
                       'confinement',
                       'description',
                       'environment',
                       'epoch',
                       'grade',
                       'hooks',
                       'icon',
                       'license-agreement',  # OBSOLETE (LP: #1638303)
                       'license-version',    # OBSOLETE
                       'summary',
                       'type',
                       'plugs',
                       'slots',
                       ]

    apps_required = ['command']
    apps_optional = ['aliases',
                     'completer',
                     'daemon',
                     'environment',
                     'stop-command',
                     'stop-timeout',
                     'restart-condition',
                     'post-stop-command',
                     'plugs',
                     'slots',
                     'ports',
                     'socket',
                     'listen-stream',
                     'socket-user',
                     'socket-group',
                     ]
    hooks_required = []
    hooks_optional = ['plugs']

    # Valid values for 'type' in packaging yaml
    # - app
    # - core
    # - kernel
    # - gadget
    # - os (deprecated)
    valid_snap_types = ['app',
                        'core',
                        'kernel',
                        'gadget',
                        'os',
                        ]

    # https://snapcraft.io/docs/interface-management
    # 'plugs':
    #    'interface': name
    #    'attrib-name': <type>
    # 'slots':
    #    'interface': name
    #    'attrib-name': <type>
    # self.interfaces lists interfaces and the valid attribute names for the
    # interface with the valid python type for the attribute (eg, [], '', {},
    # etc).  # Interfaces with no attributes should specify an empty
    # dictionary.
    #
    # Interfaces are read from the base declaration in __init__() so they don't
    # have to be added to self.interfaces.
    interfaces = dict()

    # interfaces_attribs[iface] contains all known attributes and will be
    # merged into self.interfaces after reading the base declaration since
    # the base declaration doesn't declare all the known attributes.
    interfaces_attribs = {'bool-file': {'path/slots': ""},
                          'browser-support': {'allow-sandbox/plugs': False},
                          'content': {'read/slots': [],
                                      'write/slots': [],
                                      'target/plugs': "",
                                      'default-provider/plugs': "",
                                      'content/plugs': "",
                                      'content/slots': "",
                                      },
                          'dbus': {'name/slots': "",
                                   'bus/slots': "",
                                   'name/plugs': "",
                                   'bus/plugs': "",
                                   },
                          'docker-support': {'privileged-containers/plugs':
                                             False},
                          'gpio': {'number/slots': 0},
                          'hidraw': {'path/slots': "",
                                     'usb-vendor/slots': 0,
                                     'usb-product/slots': 0,
                                     },
                          'i2c': {'path/slots': ""},
                          'iio': {'path/slots': ""},
                          'mpris': {'name/slots': ""},
                          'serial-port': {'path/slots': "",
                                          'usb-vendor/slots': 0,
                                          'usb-product/slots': 0,
                                          },
                          }

    # interfaces_required[iface] lists required attributes as combinations.
    # Eg, ['a', 'b', 'c/d'] means one of 'a', 'b', or 'c and d' is required.
    # This is to avoid situations like:
    # https://forum.snapcraft.io/t/broken-snap-breaking-snapd/401/8
    interfaces_required = {
        'bool-file': {'slots': ['path']},
        'content': {
            'slots': ['read', 'write'],
            'plugs': ['target'],
        },
        'dbus': {
            'slots': ['name/bus'],
            'plugs': ['name/bus'],
        },
        'gpio': {'slots': ['number']},
        'hidraw': {
            'slots': [
                'path',
                'path/!usb-vendor/!usb-product',
                'path/usb-vendor/usb-product'
            ],
        },
        'i2c': {'slots': ['path']},
        'iio': {'slots': ['path']},
        'serial-port': {
            'slots': [
                'path/!usb-vendor/!usb-product',
                'path/usb-vendor/usb-product'
            ],
        },
    }

    # In progress interfaces are those that are not yet in snapd but for
    # some reason we need them. Normally we will never want to do this, but
    # for example the unity8 interface wass in progress and they wanted CI
    # uploads
    inprogress_interfaces = {
        '16': {
            'plugs': {},
            'slots': {},
        }
    }

    def __init__(self, fn, review_type, overrides=None):
        Review.__init__(self, fn, review_type, overrides=overrides)

        if not self.is_snap2:
            return

        snap_yaml = self._extract_snap_yaml()
        try:
            self.snap_yaml = yaml.safe_load(snap_yaml)
        except Exception:  # pragma: nocover
            error("Could not load snap.yaml. Is it properly formatted?")

        # If local_copy is None, then this will check the server to see if
        # we are up to date. However, if we are working within the development
        # tree, use it unconditionally.
        local_copy = None
        branch_fn = os.path.join(os.path.dirname(__file__),
                                 '../data/snapd-base-declaration.yaml')
        if os.path.exists(branch_fn):
            local_copy = branch_fn
        p = snapd_base_declaration.SnapdBaseDeclaration(local_copy)
        # FIXME: don't hardcode series
        self.base_declaration_series = "16"
        self.base_declaration = p.decl[self.base_declaration_series]

        # Add in-progress interfaces
        if self.base_declaration_series in self.inprogress_interfaces:
            rel = self.base_declaration_series
            for side in ['plugs', 'slots']:
                if side not in self.base_declaration or \
                        side not in self.inprogress_interfaces[rel]:
                    continue

                if side == 'plugs':
                    oside = 'slots'
                else:
                    oside = 'plugs'

                for iface in self.inprogress_interfaces[rel][side]:
                    if iface in self.base_declaration[side] or \
                            iface in self.base_declaration[oside]:
                        # don't override anything in the base declaration
                        continue
                    self.base_declaration[side][iface] = \
                        self.inprogress_interfaces[rel][side][iface]

        # to simplify checks, gather up all the interfaces into one dict()
        for side in ['plugs', 'slots']:
            for k in self.base_declaration[side]:
                if k in self.interfaces_attribs:
                    self.interfaces[k] = self.interfaces_attribs[k]
                else:
                    self.interfaces[k] = {}

        # default to 'app'
        if 'type' not in self.snap_yaml:
            self.snap_yaml['type'] = 'app'

        if 'architectures' in self.snap_yaml:
            self.pkg_arch = self.snap_yaml['architectures']
        else:
            self.pkg_arch = ['all']

        self.is_snap_gadget = False
        if 'type' in self.snap_yaml and self.snap_yaml['type'] == 'gadget':
            self.is_snap_gadget = True

        # snapd understands:
        #   plugs:
        #     foo: null
        # but yaml.safe_load() treats 'null' as 'None', but we need a {}, so
        # we need to account for that.
        for k in ['plugs', 'slots']:
            if k not in self.snap_yaml:
                continue
            for iface in self.snap_yaml[k]:
                if not isinstance(self.snap_yaml[k], dict):
                    # eg, top-level "plugs: [ content ]"
                    error("Invalid top-level '%s'"
                          " (not a dict)" % k)  # pragma: nocover
                if self.snap_yaml[k][iface] is None:
                    self.snap_yaml[k][iface] = {}

    # Since coverage is looked at via the testsuite and the testsuite mocks
    # this out, don't cover this
    def _extract_snap_yaml(self):  # pragma: nocover
        '''Extract and read the snappy 16.04 snap.yaml'''
        y = os.path.join(self.unpack_dir, "meta/snap.yaml")
        if not os.path.isfile(y):
            error("Could not find snap.yaml.")
        return open_file_read(y)

    # Since coverage is looked at via the testsuite and the testsuite mocks
    # this out, don't cover this
    def _get_unpack_dir(self):  # pragma: nocover
        '''Get unpack directory'''
        return self.unpack_dir

    def _verify_pkgname(self, n):
        '''Verify package name'''
        # From validSnapName in snapd/snap/validate.go:
        #   "^(?:[a-z0-9]+-?)*[a-z](?:-?[a-z0-9])*$"
        # but this regex is very inefficient and certain names will make python
        # work extremely hard. Instead we use this and make sure the name isn't
        # all digits.
        pat = re.compile(r'^[a-z0-9](?:-?[a-z0-9])*$')

        if pat.search(n) and not n.isnumeric():
            return True
        return False

    def _verify_appname(self, n):
        '''Verify app name'''
        pat = re.compile(r'^[a-zA-Z0-9](?:-?[a-zA-Z0-9])*$')

        if pat.search(n):
            return True
        return False
