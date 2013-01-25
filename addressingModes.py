from memory import memory
from opcodes import pageBoundaryCycles

def imp(cpu, arg1, arg2):
    cpu.PC += 1
    return 0

def imm(cpu, arg1, arg2):
    cpu.PC += 2
    return arg1

def ZP(cpu, arg1, arg2):
    cpu.PC += 2
    return arg1
def zp(cpu, arg1, arg2):
    return memory.read(arg1)

def ZPX(cpu, arg1, arg2):
    cpu.PC += 2
    return (arg1+cpu.X) & 0xFF
def zpx(cpu, arg1, arg2):
    return memory.read(ZPX(cpu,arg1,arg2))

def ZPY(cpu, arg1, arg2):
    cpu.PC += 2
    return (arg1 + cpu.Y) & 0xFF
def zpy(cpu, arg1, arg2):
    return memory.read(ZPY(cpu,arg1,arg2))

def ABS(cpu, arg1, arg2):
    cpu.PC += 3
    return arg1 + (arg2 << 8)
def abt(cpu, arg1, arg2):
    return memory.read(ABS(cpu,arg1,arg2))

def ABX(cpu, arg1, arg2):
    addr = arg1 + (arg2 << 8)
    cpu.PC += 3
    cpu.cycles += pageBoundaryCycles(addr, cpu.X)
    return (addr + cpu.X) & 0xFFFF
def abx(cpu, arg1, arg2):
    return memory.read(ABX(cpu,arg1,arg2))

def ABY(cpu, arg1, arg2):
    addr = arg1 + (arg2 << 8)
    cpu.PC += 3
    cpu.cycles += pageBoundaryCycles(addr, cpu.Y)
    return (addr + cpu.Y) & 0xFFFF
def aby(cpu, arg1, arg2):
    return memory.read(ABY(cpu,arg1,arg2))

def ind(cpu, arg1, arg2):
    int addrLSB = arg1 + (arg2 << 8)
    int addrMSB = ((arg1 + 1) & 0xFF) + (arg2 << 8)
    cpu.PC += 3
    return memory.read(addrLSB) + (memory.read(addrMSB) << 8)

def INX(cpu, arg1, arg2):
    zpAddr = (arg1 + cpu.X) & 0xFF
    indirectAddress = memory.read(zpAddress) + (memory.read((zpAddress + 1) & 0xFF) << 8)
    cpu.PC += 2
    return indirectAddress
def inx(cpu, arg1, arg2):
    return memory.read(INX(cpu,arg1,arg2))

def INY(cpu, arg1, arg2):
    indirectAddress = memory.read(arg1) + (memory.read((arg1 + 1) & 0xFF) << 8)
    cpu.cycles += pageBoundaryCycles(indirectAddress, cpu.Y)
    cpu.PC += 2
    return (indirectAddress + cpu.Y) & 0xFFFF
def iny(cpu, arg1, arg2):
    return memory.read(INY(cpu,arg1,arg2))

def ACC(cpu, arg1, arg2):
    cpu.PC += 1
    return -1
def acc(cpu, arg1, arg2):
    cpu.PC += 1
    return cpu.A

def rel(cpu, arg1, arg2):
    cpu.PC += 2
    offset = arg1
    if (offset & 0x7F) is not offset:
        offset = (0x7F & offset) - 0x80
    return offset
