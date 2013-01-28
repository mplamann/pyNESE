import pickle

class Mapper:
    def __init__(self, file_buffer):
        self.nPrgBanks = file_buffer[4]
        self.nChrBanks = 2*file_buffer[5]

        self.prgBanks = [[0] for x in range(self.nPrgBanks)]
        self.chrBanks = [[0] for x in range(self.nChrBanks)]
        self.mirroring = file_buffer[6] & 0x9
        self.batteryBacked = bool(file_buffer[6] & 0x2)

        self.prgBankIndexes = [0,0]
        self.chrBankIndexes = [0,0]
        
        self.prgRamEnabled = False
        self.prgRam = [0]*0x2000

        index = 16
        for i in range(self.nPrgBanks):
            self.prgBanks[i] = file_buffer[index:index+16*1024]
            index += 16*1024
        for i in range(self.nChrBanks):
            self.chrBanks[i] = file_buffer[index:index+4*1024]
            index += 4*1024

    def read(self, addr):
        if self.nPrgBanks is 0:
            return 0
        if addr < 0xC000:
            return self.prgBanks[self.prgBankIndexes[0]][addr-0x8000]
        return self.prgBanks[self.prgBankIndexes[1]][addr-0xC000]

    def write(self, addr, value):
        if not self.prgRamEnabled or addr not in range(0x6000,0x8000):
            return
        self.prgRam[addr-0x6000] = value

    def ppuRead(self, addr):
        if addr < 4*1024:
            return self.chrBanks[self.chrBankIndexes[0]][addr]
        return self.chrBanks[self.chrBankIndexes[1]][addr-4*1024]

    def ppuWrite(self, addr, value):
        if self.nChrBanks is not 0:
            return
        bank = self.chrBanks[self.chrBankIndexes[int(addr>=4*1024)]]
        bank[addr % (4*1024)] = value & 0xFF

    def saveBattery(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.prgRam, f)

    def loadBattery(self, filename):
        with open(filename, 'rb') as f:
            self.prgRam = pickle.load(f)
