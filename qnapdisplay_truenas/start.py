from qnapdisplay_truenas import QnapLCDDaemon
from qnapdisplay_logger import generate_logger


def main_program():
    pidf = '/var/run/qnapdisplay_truenas.pid'
    logf = '/var/log/qnapdisplay_truenas.log'
    logger = generate_logger(logf)
    logger.info("PID Path: " + pidf)
    qnap_lcd_damon = QnapLCDDaemon(logger)
    qnap_lcd_damon.run()


main_program()
