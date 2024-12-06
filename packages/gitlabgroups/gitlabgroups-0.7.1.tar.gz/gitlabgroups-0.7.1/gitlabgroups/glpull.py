#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2018 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
#

""" gitlab group tools for pulling all repositories"""

from urllib.request import urlopen, Request
import subprocess
import json
import os
import sys
import argparse


class GLPull(object):

    """ GitLab Clone all group repositories"""

    def __init__(self, options):
        """ the main program function

        :param options: parser options
        :type options: :class:`argparse.Namespace`
        """
        self.__grpurl = options.grpurl
        gfilters = options.args or ["tango-ds"]
        self.__filters = [gf.lower() for gf in gfilters]
        self.__token = ""
        if options.tokenfile:
            with open(options.tokenfile) as fl:
                self.__token = fl.read().strip()

    def run(self):
        """ the main program function
        """
        # fetch all subgroups
        groups = []
        page = 1
        while page:
            gurl = Request("%s?page=%s" % (self.__grpurl, page))
            if self.__token:
                gurl.add_header('PRIVATE-TOKEN', self.__token)
            glst = json.loads(urlopen(gurl).read().decode())
            if glst:
                groups.extend(glst)
                page += 1
            else:
                page = 0
        for sg in groups:
            found = False
            for flt in self.__filters:
                if sg["full_path"].lower().startswith(flt):
                    found = True
            if found:
                filepath = sg["full_name"].replace(" / ", "/")
                urlpath = sg["full_name"].replace(
                    " / ", "%2F").replace(" ", "%20")
                if os.path.exists(filepath):
                    print("checking %s" % filepath)
                projects = []
                page = 1
                while page:
                    sgurl = Request("%s/%s/projects?page=%s"
                                    % (self.__grpurl, urlpath, page))
                    if self.__token:
                        sgurl.add_header('PRIVATE-TOKEN', self.__token)
                    plst = json.loads(urlopen(sgurl).read().decode())
                    if plst:
                        projects.extend(plst)
                        page += 1
                    else:
                        page = 0
                    # fetch all projects of the current subgroup
                    for pr in projects:
                        purl = pr["http_url_to_repo"]
                        if os.path.exists("%s/%s" % (filepath, pr["name"])):
                            try:
                                pullcmd = "cd %s/%s; git pull" % (
                                    filepath, pr["name"])
                                print(pullcmd)
                                process = subprocess.Popen(
                                    pullcmd,
                                    stdout=subprocess.PIPE,
                                    shell=True)
                                proc_stdout = process.communicate()[0].strip()
                                print(proc_stdout)
                            except Exception as e:
                                print("Error on %s: %s" % (purl, str(e)))


def main():
    """ the main program function
    """

    #: pipe arguments
    pipe = ""
    if not sys.stdin.isatty():
        pp = sys.stdin.readlines()
        #: system pipe
        pipe = "".join(pp)

    description = "Command-line tool for pulling all repositories " \
                  "of gitlab (sub-)group"

    epilog = 'examples:\n' \
        '  glpull  -a \n\n' \
        '    - pull all repositories of "tango-ds" group\n\n' \
        '  glpull tango-ds/DeviceClasses \n\n' \
        '    - pull all repositories of "tango-ds/DeviceClasses" ' \
        'subgroup\n\n'

    parser = argparse.ArgumentParser(
        description=description, epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        'args', metavar='filter', type=str, nargs='?',
        help='group filter, e.g. "tango-ds"')
    parser.add_argument(
        "-t", "--token-file",
        help="token file",
        dest="tokenfile", default="")
    parser.add_argument(
        "-g", "--groupurl",
        help='default: "https://gitlab.desy.de/api/v4/groups"',
        dest="grpurl", default="https://gitlab.desy.de/api/v4/groups")
    parser.add_argument(
        "-a", "--all", action="store_true",
        default=False, dest="all",
        help="set filter to 'tango-ds'")

    try:
        options = parser.parse_args()
    except Exception as e:
        sys.stderr.write("Error: %s\n" % str(e))
        sys.stderr.flush()
        parser.print_help()
        print("")
        sys.exit(255)

    #: command-line and pipe arguments
    parg = []
    if hasattr(options, "args"):
        parg = [options.args] if options.args else []
    if pipe:
        parg.append(pipe)
    if options.all:
        parg.append("tango-ds")
    options.args = parg

    if not options.args:
        parser.print_help()
        print("")
        sys.exit(255)

    try:
        command = GLPull(options)
        command.run()
    except Exception as e:
        sys.stderr.write("Error: glpull interrupted with:")
        sys.stderr.write(str(e))
        sys.stderr.flush()
        sys.exit(255)


if __name__ == "__main__":
    main()
