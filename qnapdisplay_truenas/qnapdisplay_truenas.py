#!/usr/bin/env python3
from qnap_lcd_daemon import QnapLCDDaemon
import argparse
import daemon
import logging
from daemon import pidfile


def start_daemon(pidf, logf):
    print('Starting QNAP Display Daemon')
    print('PID Path: ' + pidf)
    print('Log Path: ' + logf)

    logger = logging.getLogger('qnapdisplay_truenas_daemon')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logf)
    fh.setLevel(logging.INFO)

    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr)

    fh.setFormatter(formatter)

    logger.addHandler(fh)
    qnap_lcd_damon = QnapLCDDaemon(logger)

    with daemon.DaemonContext(pidfile=pidfile.TimeoutPIDLockFile(pidf), ) as context:
        qnap_lcd_damon.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QNAP Display Driver for TrueNAS")
    parser.add_argument('-p', '--pid-file', default='/var/run/qnapdisplay_truenas.pid')
    parser.add_argument('-l', '--log-file', default='/var/log/qnapdisplay_truenas.log')
    args = parser.parse_args()
    start_daemon(pidf=args.pid_file, logf=args.log_file)
