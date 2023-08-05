import argparse
import logging
import os
import platform
import re
import shlex
import signal
import sys
import tempfile
import time

from subprocess import Popen, PIPE


log = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser()

    # this could be something like "\w+firefox\w+"
    parser.add_argument(
        "--container-name",
        "-n",
        help='name (or python regular expression for the name) of the container(s) to view. Ex: --container-name ".*firefox"',
        default="",
        type=str,
    )

#    parser.add_argument("--restart", "-r",
#                        help="restart the VNC viewers if the session restart within timeout",
#                        action="store_true")
#
#    parser.add_argument("--timeout", "-t",
#                        help="number of seconds to wait for VNC sessions to restart before giving up on reconnecting",
#                        default=3,
#                        type=int)

    parser.add_argument(
        "--verbose",
        "-v",
        help="level of logging verbosity",
        default=3,
        action="count",
    )

    opts = parser.parse_args()
    return opts


def signal_handler(signal, frame):

    log.debug("caught signal: {}".format(signal))

    global vncpwf
    remove_vnc_password_file(vncpwf)

    # kill the processs if they are still running
    log.debug("killing running processes")
    global procs
    for p in procs:
        if p.poll() is None:
            log.debug("killing {}".format(p))
            p.kill()

    log.debug("exiting")
    sys.exit(0)


def remove_vnc_password_file(fname):

    log.debug("removing vnc password file: {}".format(fname))

    if len(fname) == 0:
        return

    try:
        os.remove(fname)
    except OSError:
        # don't complain if file doesnt exist
        pass


def find_vnc_ports(container_name):

    # get the list of running containers
    log.debug("retrieving list of running Docker containers")
    o, e = Popen(["docker", "ps"], stdout=PIPE).communicate()

    # find all selenium/* containers that have a host
    # machine port forwarded to the container's port 5900
    # capture the host machine's port number
    container_re = "\w+/.+0\.0\.0\.0:(\d+)->5900/tcp.*\s+{}".format(
        container_name
    ).encode("utf8")
    log.debug("container_re = {}".format(container_re))
    log.debug("searching for mathing containers running VNC servers")
    ports = re.findall(container_re, o)

    return ports


def generate_vnc_command():

    # tempfile to store vnc password
    global vncpwf
    vncpwf = ""

    # vnc viewer command template, operating system dependent
    cmd_tmpl = ""

    systemName = platform.system()
    if systemName == "Linux":
        log.debug("setting up password file and VNC command for Linux system.")
        # on linux, we need to store the vnc password to a local file.
        # the vnc password is 'secret'
        # the string below was created with the program vnc4passwd
        #   vnc4passwd <password-file>
        # then enter the password twice
        fd, vncpwf = tempfile.mkstemp()
        os.write(fd, b".-\xbfWn\xb0l\x9e")
        os.close(fd)

        cmd_tmpl = "vncviewer -passwd {vncpwf} 127.0.0.1:{port}"

    elif systemName == "Darwin":
        log.debug("setting up VNC command with embedded password for MacOS.")
        # on macos, we can embed the password in the vnc address
        # username is blank
        cmd_tmpl = "open vnc://:secret@localhost:{port}"
    else:
        raise Exception("don't know how to handle vnc on this platform")

    return cmd_tmpl, vncpwf


def launch_vnc_sessions(ports, vncpwf, cmd_tmpl):

    # store our processes
    global procs
    procs = []

    # open a vnc viewer for each port we found.
    for port in ports:

        # convert port back to a str from a bytes if in python3
        port = port.decode("utf8")

        vnccmd = cmd_tmpl.format(port=port, vncpwf=vncpwf)

        log.debug("VNC viewer command: {}".format(vnccmd))

        # convert the command to a list
        vnccmd = shlex.split(vnccmd)

        # start the command
        p = Popen(vnccmd)

        # keep trac of our processes so we can kill them later.
        procs.append(p)

        # slowly open vnc viewers for some macos.
        time.sleep(0.5)

    return procs


def main(opts):

    # shut everything down if we get a SIGINT or SIGTERM
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    ports = find_vnc_ports(opts.container_name)
    cmd_tmpl, vncpwf = generate_vnc_command()
    procs = launch_vnc_sessions(ports, vncpwf, cmd_tmpl)

    # wait for all of the processes to end
    log.debug("waiting for {} VNC sessions to end".format(len(procs)))
    for p in procs:
        p.wait()

    # clean up temp password file
    remove_vnc_password_file(vncpwf)


def cli():

    opts = parse_arguments()

    logging.basicConfig(level=int((6 - opts.verbose) * 10))

    log.debug("opts = {}".format(opts))

    main(opts)

    log.debug("exiting")


if __name__ == "__main__":

    cli()
