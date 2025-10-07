import smbus
class MCP4725:
    def __init__(self, dynamic_range, adress=0x61, verbose = True):
        self.bus = smbus.SMBus(1)
        self.adress = adress
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dynamic_range = dynamic_range
    def deinit(self):
        self.bus.close()
    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4752 (12 бит)")
        first_byte = self.wm | self.pds | number >> 8
        second_byte = number & 0xFF
        self.bus.write_byte_data(0x61, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по IC2 данные: [0x{(self.adress << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")
    def set_voltage(self,voltage):
        if not(0 <= voltage <= self.dynamic_range):
            print("Не то напряжение!!!!!")
            return

        digital_value = int((voltage / self.dynamic_range) * 4095)
        digital_value = max(0, min(4095, digital_value))
        self.set_number(digital_value)
if __name__ == "__main__":
    try:
        dac = MCP4725(dynamic_range=5.11, verbose=True)
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах:"))
                dac.set_voltage(voltage)
            except ValueError:
                print("не то число")
    finally:
        dac = MCP4725(dynamic_range=5.11, verbose=True)
        dac.deinit()