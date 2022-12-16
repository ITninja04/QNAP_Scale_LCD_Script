#!/usr/bin/python
from qnap_lcd_daemon import QnapLCDDaemon
import argparse
import daemon
from qnapdisplay_logger import generate_logger

def start_daemon(pidf, logf):
    print('Starting QNAP Display Daemon')
    print('PID Path: ' + pidf)
    print('Log Path: ' + logf)
    logger = generate_logger(logf)
    qnap_lcd_damon = QnapLCDDaemon(logger)
    with daemon.DaemonContext():
        qnap_lcd_damon.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QNAP Display Driver for TrueNAS")
    parser.add_argument('-p', '--pid-file', default='/var/run/qnapdisplay_truenas.pid')
    parser.add_argument('-l', '--log-file', default='/var/log/qnapdisplay_truenas.log')
    args = parser.parse_args()
    start_daemon(pidf=args.pid_file, logf=args.log_file)
