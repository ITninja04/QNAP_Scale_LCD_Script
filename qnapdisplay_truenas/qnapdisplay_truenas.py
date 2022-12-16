#!/usr/bin/env python3
from qnap_lcd_daemon import QnapLCDDaemon
import argparse
import daemon
import logging
from daemon import pidfile


def start_daemon(pidf, logf):
    logger = logging.getLogger('qnapdisplay_truenas_daemon')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logf)
    fh.setLevel(logging.INFO)

    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr)

    fh.setFormatter(formatter)

    logger.addHandler(fh)
    ### This launches the daemon in its context
    global debug_p
    qnap_lcd_damon = QnapLCDDaemon(logger)

    if debug_p:
        print("qnapdisplay_truenas: entered run()")
        print("qnapdisplay_truenas: pidf = {}    logf = {}".format(pidf, logf))
        print("qnapdisplay_truenas: about to start daemonization")
    with daemon.DaemonContext(pidfile=pidfile.TimeoutPIDLockFile(pidf), ) as context:
        qnap_lcd_damon.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example daemon in Python")
    parser.add_argument('-p', '--pid-file', default='/var/run/qnapdisplay_truenas.pid')
    parser.add_argument('-l', '--log-file', default='/var/log/qnapdisplay_truenas.log')
    args = parser.parse_args()
    start_daemon(pidf=args.pid_file, logf=args.log_file)
