#!/usr/bin/env python3
import sys
from daemon import Daemon
from qnapdisplay import QnapDisplay
from qnap_lcd_daemon import QnapLCDDaemon

if __name__ == "__main__":
    daemon = QnapLCDDaemon('/tmp/qnap-lcd-daemon.pid')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
