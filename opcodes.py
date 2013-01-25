from memory import memory

def pageBoundaryCycles(address, offset):
    newAddr = address + offset
    if (newAddr & 0xFF00) is not (address & 0xFF00):
        return 1
    return 0

def TAX(cpu, value):
    cpu.X = cpu.A
    cpu.setNZ(cpu.X)

def TAY(cpu, value):
    cpu.Y = cpu.A
    cpu.setNZ(cpu.Y)

def TSX(cpu, value):
    cpu.X = cpu.S
    cpu.setNZ(cpu.X)

def TXS(cpu, value):
    cpu.S = cpu.X
    
def TXA(cpu, value):
    cpu.A = cpu.X
    cpu.setNZ(cpu.A)

def TYA(cpu, value):
    cpu.A = cpu.Y
    cpu.setNZ(cpu.A)

def LAX(cpu, value):
    cpu.A = value
    cpu.X = value
    cpu.setNZ(value)

def LDA(cpu, value):
    cpu.A = value
    cpu.setNZ(value)

def LDX(cpu, value):
    cpu.X = value
    cpu.setNZ(value)

def LDY(cpu, value):
    cpu.Y = value
    cpu.setNZ(value)

def STA(cpu, value):
    memory.write(value, cpu.A)

def STX(cpu, value):
    memory.write(value, cpu.X)

def STY(cpu, value):
    memory.write(value, cpu.Y)

################################################################################
## Flag Operations                                                            ##
################################################################################    
    
def CLC(cpu, value):
    cpu.C = False

def SEC(cpu, value):
    cpu.C = True

def CLI(cpu, value):
    cpu.I = False

def SEI(cpu, value):
    cpu.I = True

def CLV(cpu, value):
    cpu.V = False

def CLD(cpu, value):
    cpu.D = False

def SED(cpu, value):
    cpu.D = True

################################################################################
## Boolean Operations                                                         ##
################################################################################

def condRead(cpu, addr):
    if addr is -1:
        return cpu.A
    return memory.read(addr)

def condWrite(cpu, addr, value):
    if addr is -1:
        cpu.A = value
    else:
        memory.write(addr, value)
    
def AND(cpu, value):
    cpu.A &= value
    cpu.setNZ(cpu.A)

def SAX(cpu, value):
    memory.write(value, cpu.A & cpu.X)

def EOR(cpu, value):
    cpu.A ^= value
    cpu.setNZ(cpu.A)

def ORA(cpu, value):
    cpu.A |= value
    cpu.setNZ(cpu.A)

def ASL(cpu, value):
    temp = condRead(value) << 1
    cpu.c = bool(temp & 0x100);
    temp &= 0xFF
    condWrite(value, temp)
    cpu.setNZ(temp)

def LSR(cpu, value):
    temp = condRead(value)
    cpu.C = bool(temp & 0x01)
    temp >>= 1
    temp &= 0x7F
    condWrite(value, temp)
    cpu.setNZ(temp)

def ROL(cpu, value):
    temp = condRead(value) << 1
    temp += int(cpu.C)
    cpu.C = temp > 0xFF
    temp &= 0xFF
    condWrite(value,temp)
    cpu.setNZ(temp)

def ROR(cpu, value):
    temp = condRead(value)
    if cpu.C:
        temp |= 0x100
    cpu.C = bool(temp & 0x01)
    temp >>= 1
    temp &= 0xFF
    condWrite(value, temp)
    cpu.setNZ(temp)

def SLO(cpu, value):
    ASL(cpu, value)
    ORA(cpu, memory.read(value))

def RLA(cpu, value):
    ROL(cpu, value)
    AND(cpu, memory.read(value))

def SRE(cpu, value):
    LSR(cpu, value)
    EOR(cpu, memory.read(value))

def BIT(cpu, value):
    cpu.Z = not bool(cpu.A & value)
    cpu.V = bool(0x40 & value)
    cpu.N = bool(0x80 & value)

################################################################################
## Stack Operations                                                           ##
################################################################################

def pushToStack(cpu, value):
    memory.write(0x100 | (cpu.S & 0xFF), value)
    cpu.S -= 1

def popFromStack(cpu):
    cpu.S += 1
    return memory.read(0x100 | (cpu.S & 0xFF))

def PHA(cpu, value):
    pushToStack(cpu, cpu.A)

def PLA(cpu, value):
    cpu.A = popFromStack(cpu);
    cpu.setNZ(cpu.A)

def PHP(cpu, value):
    pushToStack(cpu, cpu.getP() | 0x10)
    
def PLP(cpu, value):
    cpu.setP(popFromStack(cpu))

################################################################################
## Arithmetic Operations                                                      ##
################################################################################    
    
def compareWithRegister(cpu, value, reg):
    temp = reg-value
    cpu.C = temp < 0x100
    cpu.N = bool(temp & 0x80)
    cpu.Z = not bool(temp)

def modMemory(cpu, address, dVal):
    value = memory.read(address)
    value += dVal
    memory.write(address, value)
    cpu.setNZ(value)

def ADC(cpu, value):
    temp = value + cpu.A + int(cpu.C)
    cpu.C = temp > 0xFF
    cpu.V = (not ((cpu.A ^ value) & 0x80) and ((cpu.A ^ temp) & 0x80))
    cpu.A = temp & 0xFF
    cpu.N = bool(cpu.A & 0x80)
    cpu.Z = not bool(cpu.A)

def SBC(cpu, value):
    temp = cpu.A - value - int(cpu.C)
    cpu.C = temp < 0x100
    cpu.V = (((cpu.A ^ value) & 0x80) and ((cpu.A ^ temp) & 0x80))
    cpu.A = temp & 0xFF
    cpu.N = bool(cpu.A & 0x80)
    cpu.Z = not bool(cpu.A)

def CMP(cpu, value):
    compareWithRegister(cpu, value, cpu.A)

def CPX(cpu, value):
    compareWithRegister(cpu, value, cpu.X)

def CPY(cpu, value):
    compareWithRegister(cpu, value, cpu.Y)

def DCP(cpu, value):
    modMemory(cpu, value, -1)
    compareWithRegister(cpu, memory.read(value), cpu.A)

def DEC(cpu, value):
    modMemory(cpu, value, -1)

def DEX(cpu, value):
    cpu.X -= 1
    cpu.X &= 0xFF
    cpu.setNZ(cpu.X)

def DEY(cpu, value):
    cpu.Y -= 1
    cpu.Y &= 0xFF
    cpu.setNZ(cpu.Y)

def INC(cpu, value):
    modMemory(cpu, value, 1)

def INX(cpu, value):
    cpu.X += 1
    cpu.X &= 0xFF
    cpu.setNZ(cpu.X)

def INY(cpu, value):
    cpu.Y += 1
    cpu.Y &= 0xFF
    cpu.setNZ(cpu.Y)

def ISB(cpu, value):
    INC(cpu, value)
    SBC(cpu, memory.read(value))

def RRA(cpu, value):
    pass

################################################################################
## Branches and Jumps                                                         ##
################################################################################

def doBranch(cpu, offset):
    cpu.cycles += pageBoundaryCycles(cpu.PC, offset) + 1
    cpu.PC += offset

def JMP(cpu, value):
    cpu.PC = value

def JSR(cpu, value):
    pushToStack(cpu, ((cpu.PC-1) >> 8) & 0xFF)
    pushToStack(cpu, (cpu.PC-1) & 0xFF)
    cpu.PC = value

def RTI(cpu, value):
    cpu.setP(popFromStack(cpu))
    cpu.PC = popFromStack(cpu) + (popFromStack(cpu) << 8)

def RTS(cpu, value):
    cpu.PC = popFromStack(cpu)
    cpu.PC += popFromStack(cpu) << 8 + 1

def BPL(cpu, value):
    if not cpu.N:
        doBranch(cpu, value)

def BMI(cpu, value):
    if cpu.N:
        doBranch(cpu, value)

def BVC(cpu, value):
    if not cpu.V:
        doBranch(cpu, value)

def BVS(cpu, value):
    if cpu.S:
        doBranch(cpu, value)

def BCC(cpu, value):
    if not cpu.C:
        doBranch(cpu, value)

def BCS(cpu, value):
    if not cpu.C:
        doBranch(cpu, value)

def BNE(cpu, value):
    if not cpu.Z:
        doBranch(cpu, value)

def BEQ(cpu, value):
    if cpu.Z:
        doBranch(cpu, value)        

################################################################################
## Interrupts                                                                 ##
################################################################################        
        
def processInterrupt(cpu, vector):
    pushToStack(cpu, (cpu.PC >> 8) & 0xFF)
    pushToStack(cpu, cpu.PC & 0xFF)
    pushToStack(cpu, cpu.getP())
    cpu.I = True
    cpu.PC = vector

def BRK(cpu, value):
    vector = memory.read(VECTOR_BRK) + memory.read(VECTOR_BRK+1)<<8
    processInterrupt(cpu,vector)

def ANC(cpu, value):
    pass
def ALR(cpu, value):
    pass
def ARR(cpu, value):
    pass
def XAA(cpu, value):
    pass
def AHX(cpu, value):
    pass
def TAS(cpu, value):
    pass
def SHY(cpu, value):
    pass
def SHX(cpu, value):
    pass
def LAS(cpu, value):
    pass
def AXS(cpu, value):
    pass
def KIL(cpu, value):
    pass
def NOP(cpu, value):
    pass
