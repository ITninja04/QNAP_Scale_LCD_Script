import daemon
from qnapdisplay_truenas import QnapLCDDaemon
from qnapdisplay_logger import generate_logger


def main_program():
    pidf = '/var/run/qnapdisplay_truenas.pid'
    logf = '/var/log/qnapdisplay_truenas.log'

    print('Starting QNAP Display Daemon')
    print('PID Path: ' + pidf)
    print('Log Path: ' + logf)
    logger = generate_logger(logf)
    qnap_lcd_damon = QnapLCDDaemon(logger)
    qnap_lcd_damon.run()

with daemon.DaemonContext():
    main_program()
