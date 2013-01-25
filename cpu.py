from opcodes import *

VECTOR_NMI = 0xFFFA
VECTOR_RESET = 0xFFFC
VECTOR_BRK = 0xFFFE

class CPU:
    def __init__(self):
        self.A = 0
        self.X = 0
        self.Y = 0
        self.S = 0xFD
        self.PC = 0
        self.N = False
        self.Z = False
        self.C = False
        self.I = False
        self.D = False
        self.V = False
        self.B = False

        self.opcodes = [BRK, ORA, KIL, SLO, NOP, ORA, ASL, SLO, PHP, ORA, ASL, ANC, NOP, ORA, ASL, SLO,
                        BPL, ORA, KIL, SLO, NOP, ORA, ASL, SLO, CLC, ORA, NOP, SLO, NOP, ORA, ASL, SLO,
                        JSR, AND, KIL, RLA, BIT, AND, ROL, RLA, PLP, AND, ROL, ANC, BIT, AND, ROL, RLA,
                        BMI, AND, KIL, RLA, NOP, AND, ROL, RLA, SEC, AND, NOP, RLA, NOP, AND, ROL, RLA,
                        RTI, EOR, KIL, SRE, NOP, EOR, LSR, SRE, PHA, EOR, LSR, ALR, JMP, EOR, LSR, SRE,
                        BVC, EOR, KIL, SRE, NOP, EOR, LSR, SRE, CLI, EOR, NOP, SRE, NOP, EOR, LSR, SRE,
                        RTS, ADC, KIL, RRA, NOP, ADC, ROR, RRA, PLA, ADC, ROR, ARR, JMP, ADC, ROR, RRA,
                        BVS, ADC, KIL, RRA, NOP, ADC, ROR, RRA, SEI, ADC, NOP, RRA, NOP, ADC, ROR, RRA,
                        NOP, STA, NOP, SAX, STY, STA, STX, SAX, DEY, NOP, TXA, XAA, STY, STA, STX, SAX,
                        BCC, STA, KIL, AHX, STY, STA, STX, SAX, TYA, STA, TXS, TAS, SHY, STA, SHX, AHX,
                        LDY, LDA, LDX, LAX, LDY, LDA, LDX, LAX, TAY, LDA, TAX, LAX, LDY, LDA, LDX, LAX,
                        BCS, LDA, KIL, LAX, LDY, LDA, LDX, LAX, CLV, LDA, TSX, LAS, LDY, LDA, LDX, LAX,
                        CPY, CMP, NOP, DCP, CPY, CMP, DEC, DCP, INY, CMP, DEX, AXS, CPY, CMP, DEC, DCP,
                        BNE, CMP, KIL, DCP, NOP, CMP, DEC, DCP, CLD, CMP, NOP, DCP, NOP, CMP, DEC, DCP,
                        CPX, SBC, NOP, ISB, CPX, SBC, INC, ISB, INX, SBC, NOP, SBC, CPX, SBC, INC, ISB,
                        BEQ, SBC, KIL, ISB, NOP, SBC, INC, ISB, SED, SBC, NOP, ISB, NOP, SBC, INC, ISB]
        self.addressingModes = [imp, inx, imp, INX, zp,  zp,  ZP,  ZP,  imp, imm, ACC, imm, abt, abt, ABS, ABS,
                                rel, iny, imp, INY, zpx, zpx, ZPX, ZPX, imp, aby, imp, ABY, abx, abx, ABX, ABX,
                                ABS, inx, imp, INX, zp,  zp,  ZP,  ZP,  imp, imm, ACC, imm, abt, abt, ABS, ABS,
                                rel, iny, imp, INY, zpx, zpx, ZPX, ZPX, imp, aby, imp, ABY, abx, abx, ABX, ABX,
                                imp, inx, imp, INX, zp,  zp,  ZP,  ZP,  imp, imm, ACC, imm, ABS, abt, ABS, ABS,
                                rel, iny, imp, INY, zpx, zpx, ZPX, ZPX, imp, aby, imp, ABY, abx, abx, ABX, ABX,
                                imp, inx, imp, inx, zp,  zp,  ZP,  zp,  imp, imm, ACC, imm, ind, abt, ABS, abt,
                                rel, iny, imp, iny, zpx, zpx, ZPX, zpx, imp, aby, imp, aby, abx, abx, ABX, abx,
                                imm, INX, imm, INX, ZP,  ZP,  ZP,  ZP,  imp, imm, acc, imm, ABS, ABS, ABS, ABS,
                                rel, INY, imp, iny, ZPX, ZPX, ZPY, ZPY, imp, ABY, acc, aby, abx, ABX, aby, aby,
                                imm, inx, imm, inx, zp,  zp,  zp,  zp,  imp, imm, acc, imm, abt, abt, abt, abt,
                                rel, iny, imp, iny, zpx, zpx, zpy, zpy, imp, aby, acc, aby, abx, abx, aby, aby,
                                imm, inx, imm, INX, zp,  zp,  ZP,  ZP,  imp, imm, acc, imm, abt, abt, ABS, ABS,
                                rel, iny, imp, INY, zpx, zpx, ZPX, ZPX, imp, aby, imp, ABY, abx, abx, ABX, ABX,
                                imm, inx, imm, INX, zp,  zp,  ZP,  ZP,  imp, imm, imp, imm, abt, abt, ABS, ABS,
                                rel, iny, imp, INY, zpx, zpx, ZPX, ZPX, imp, aby, imp, ABY, abx, abx, ABX, ABX]
        self.cycleMap = [7, 8, 0, 8, 3, 3, 5, 5, 3, 2, 2, 2, 4, 4, 6, 6,
                         2, 5, 0, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
                         6, 6, 0, 8, 3, 3, 5, 5, 4, 2, 2, 2, 4, 4, 6, 6,
                         2, 5, 0, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
                         6, 6, 0, 8, 3, 3, 5, 5, 3, 2, 2, 2, 3, 4, 6, 6,
                         2, 5, 0, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
                         6, 6, 0, 8, 3, 3, 5, 5, 4, 2, 2, 2, 5, 4, 6, 6,
                         2, 5, 0, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
                         2, 6, 2, 6, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
                         2, 6, 0, 6, 4, 4, 4, 4, 2, 5, 2, 5, 5, 5, 5, 5,
                         2, 6, 2, 6, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
                         2, 5, 0, 5, 4, 4, 4, 4, 2, 4, 2, 4, 4, 4, 4, 4,
                         2, 6, 2, 8, 3, 3, 5, 5, 2, 2, 2, 2, 4, 4, 6, 6,
                         2, 5, 0, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
                         2, 6, 2, 8, 3, 3, 5, 5, 2, 2, 2, 2, 4, 4, 6, 6,
                         2, 5, 0, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7]
    def setNZ(self, value):
        value &= 0xFF
        self.N = not bool(value & 0x80)
        self.Z = not bool(value)
    def setP(self, value):
        self.C = ((self.P & 0x01) != 0)
        self.Z = ((self.P & 0x02) != 0)
        self.I = ((self.P & 0x04) != 0)
        self.D = ((self.P & 0x08) != 0)
        self.V = ((self.P & 0x40) != 0)
        self.N = ((self.P & 0x80) != 0)
    def getP(self):
        P = 0x20;
        if self.C:
            P |= 0x01;
        if self.Z:
            P |= 0x02;
        if self.I:
            P |= 0x04;
        if self.B:
            P |= 0x10;
        if self.V:
            P |= 0x40;
        if self.N:
            P |= 0x80;
        if self.D:
            P |= 0x08;
        return P
