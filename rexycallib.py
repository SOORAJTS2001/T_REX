import pyfirmata
global pin9
board=pyfirmata.Arduino('/dev/ttyUSB0')
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
pin9 = board.get_pin('d:9:s')
pin10 = board.get_pin('d:10:s')
pin11 = board.get_pin('d:11:s')
pin9.write(90)
pin10.write(180)
pin11.write(0)