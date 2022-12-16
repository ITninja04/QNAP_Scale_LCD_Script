import serial


class QnapDisplay:
    # Qnap connects its serial to ttys1
    ser = serial.Serial('/dev/ttyS1', 1200)

    # 8 bit keycodes from serial controller
    down = [b'S\x05\x00\x02S\x05\x00\x00', b'S\x05\x00\x00S\x05\x00\x02', b'S\x05\x00\x02S\x05\x00\x00']
    up = [b'S\x05\x00\x01S\x05\x00\x00', b'S\x05\x00\x00S\x05\x00\x01', b'S\x05\x00\x01S\x05\x00\x00']
    both = [b'S\x05\x00\x01S\x05\x00\x03', b'S\x05\x00\x02S\x05\x00\x03', b'S\x05\x00\x03S\x05\x00\x00']

    def init(self):
        self.ser.write(b'M\0')
        initlcd = self.ser.read(4)
        if initlcd == 'S\x01\x00}':
            return True

    def write(self, row, text):
        if row == 0:
            initrow = 'M\f\0\20'
        elif row == 1:
            initrow = 'M\f\1\20'
        writerow = '%s%s' % (initrow, text.ljust(16)[:16])
        self.ser.write(b'M^\1')
        self.ser.write(writerow.encode())

    def read(self):
        key = self.ser.read(8)
        if key in self.down:
            state = 'Down'
        elif key in self.up:
            state = 'Up'
        elif key in self.both:
            state = 'Both'
            self.ser.read(8)
        else:
            print("Unknown key")
            state = 'unknown'
        return state

    def enable(self):
        self.ser.write(b'M^\1\n')

    def disable(self):
        self.ser.write(b'M^\0\n')
