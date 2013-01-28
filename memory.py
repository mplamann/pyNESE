memory = Memory()

class Memory:
    def __init__(self):
        self.isPpuScrollOnX = True
        self.isPpuAddrHigh = True
        self.PPUSCROLLX = 0
        self.PPUSCROLLY = 0
        self.RAM = [0]*0x800
        self.palette = [0]*0x20
        self.nametables = [[0]*0x400,[0]*0x400]

        self.ppuDataBuffer = 0

        self.OAM = [0]*256
        self.JOYSTROBE = 0
        
    def read(self, addr):
        if addr < 0x2000:
            return self.RAM[addr % 0x800]
        if addr is 0x2002: # PPUSTATUS
            self.isPpuAddrHigh = True
            temp = self.PPUSTATUS & 0xFF
            self.PPUSTATUS &= 0x7F  # Reset NMI flag
            temp |= (self.PPU_LAST_WRITE & 0x1F)
            return temp
        if addr is 0x2004:
            return self.OAM[self.OAMADDR]
        if addr is 0x2007:
            temp = None
            if self.PPUADDR >= 0x3F00:
                temp = self.ppuRead(self.PPUADDR)
            else:
                temp = self.ppuDataBuffer
                ppuDataBuffer = self.ppuRead(self.PPUADDR)
            PPUADDR += 1
            return temp
        if addr is 0x4016:
            return self.gamepad.readPlayer1() | 0x40
        if addr is 0x4017:
            return self.gamepad.readPlayer2() | 0x40
        return self.mapper.read(address)

    def write(self, addr, value):
        if addr < 0x2000:
            self.RAM[addr % 0x800]
        if addr is 0x2000:
            self.PPUCTRL = value & 0xFF
        if addr is 0x2001:
            self.PPUMASK = value & 0xFF
        if addr is 0x2003:
            self.OAMADDR = value & 0xFF
        if addr is 0x2004:
            self.OAM[self.OAMADDR] = value & 0xFF
            self.OAMADDR = (self.OAMADDR + 1) % 0xFF
        if addr is 0x2005:
            if self.isPpuScrollOnX:
                self.PPUSCROLLX = value & 0xFF
            elif (value & 0xFF) < 240:
                self.PPUSCROLLY = value & 0xFF
            self.isPpuScrollOnX = not self.isPpuScrollOnX
        if addr is 0x2006:
            if self.isPpuAddrHigh:
                self.PPUADDR = (value & 0xFF) << 8
            else:
                self.PPUADDR += (value & 0xFF)
                if self.PPUADDR is 0:
                    self.PPUSCROLLX = 0
                    self.PPUSCROLLY = 0
                    self.PPUCTRL &= 0xFC
            self.isPpuAddrHigh = not self.isPpuAddrHigh
        if addr is 0x2007:
            self.ppuWrite(self.PPUADDR, value)
            if not (self.PPUCTRL & 0x04):
                self.PPUADDR += 1
            else:
                self.PPUADDR += 32
        if addr is 0x4014:
            self.DMA(value)
        if addr is 0x4016:
            if self.JOYSTROBE is 1 and value is 0:
                self.gamepad.strobe()
            self.JOYSTROBE = value
        if addr in range(0x2000,0x2008):
            self.PPU_LAST_WRITE = value
        if addr >= 0x5000:
            self.mapper.write(addr, value)
            
