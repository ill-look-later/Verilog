#!/usr/bin/python
import random
from up2Utils import *

class up2Execute:
    ''' Model of the up2 processor execute section '''

    def __init__(self):
        ''' Register block '''
        self.regs = []
        self.regs.append(1)
        for i in range(1,5):
            self.regs.append(random.randint(0,15))

        ''' Mux setup '''
        self.a = random.randint(0,1)
        self.b = random.randint(2,3)
        self.c = random.randint(1,4)

        ''' Flags '''
        self.z = 0

        ''' Model assertions '''
        assert len(self.regs) == 5, 'Fixed length of registers'
        assert self.regs[0] == 1, 'Fixed +1 reg assigned'
        for i in range(1,5):
            assert self.regs[i] < 16,'Overflow'
            assert self.regs[i] >= 0, 'Underflow'

    def writeRegs(self, regs):
        self.regs = regs

    def readRegs(self):
        return self.regs

    def add(self):
        ''' Add with overflow wrap around '''
        self.regs[self.c] = self.regs[self.b] + self.regs[self.a]
        if self.regs[self.c] > 15:
            self.regs[self.c] -= 16
            self.updateOverflowFlag(True)
        else:
            self.updateOverflowFlag(False)
        self.updateZeroFlag()

    def sub(self):
        ''' Sub with underflow wrap around '''
        self.regs[self.c] = self.regs[self.b] - self.regs[self.a]
        if self.regs[self.c] < 0:
            self.regs[self.c] += 16
            self.updateUnderflowFlag(True)
        else:
            self.updateUnderflowFlag(False)
        self.updateZeroFlag()

    def oor(self):
        ''' OR '''
        self.regs[self.c] = self.regs[self.b] | self.regs[self.a]
        self.updateZeroFlag()

    def copy(self):
        ''' COPY '''
        self.regs[self.c] = self.regs[self.b]
        self.updateZeroFlag()

    def xor(self):
        ''' XOR '''
        self.regs[self.c] = self.regs[self.b] ^ self.regs[self.a]
        self.updateZeroFlag()

    def nan(self):
        ''' NAND '''
        self.regs[self.c] = ~(self.regs[self.b] & self.regs[self.a])
        self.updateZeroFlag()

    def lsl(self):
        ''' Logical shift left '''
        self.updateOverflowFlag( self.regs[self.a] & 8)
        self.regs[self.c] = int("F",16) & (self.regs[self.a] << 1)
        self.updateZeroFlag()

    def lsr(self):
        ''' Logical shift right '''
        self.updateUnderflowFlag( self.regs[self.a] & 1)
        self.regs[self.c] = int("F",16) & (self.regs[self.a] >> 1)
        self.updateZeroFlag()

    def updateZeroFlag(self):
        '''Flag after ALU update '''
        if 0 == self.regs[self.c]:
            self.z = 1
        else:
            self.z = 0

    def updateOverflowFlag(self, overflow):
        ''' Flag after ALU update'''
        if overflow:
            self.o = 1
        else:
            self.o = 0

    def updateUnderflowFlag(self, underflow):
        ''' Flag after ALU update'''
        if underflow:
            self.u = 1
        else:
            self.u = 0

    def readZeroFLag(self):
        return self.z

    def readOverflowFlag(self):
        return self.o

    def readUnderflowFlag(self):
        return self.u

    def setRegOut1(self):
        self.a = 0

    def setRegOutR0(self):
        self.a = 1

    def setRegOutR1(self):
        self.b = 2

    def setRegOutR2(self):
        self.b = 3

    def setRegInR0(self):
        self.c = 1

    def setRegInR1(self):
        self.c = 2

    def setRegInR2(self):
        self.c = 3

    def setRegInCmp(self):
        self.c = 4

    def getR0(self):
        return self.regs[1]

    def setR0(self, data):
        self.regs[1] = data

class up2RegStack:
    ''' Model of the up2 processor register stack sections '''

    def __init__(self, length):
        self.stack = []
        self.length = length
        for i in range(0,self.length):
            self.stack.append([1,0,0,0,0])
        self.p = 0

        ''' Model assertions '''
        assert self.p >= 0, 'Stack out of range'

    def setInc(self):
        self.p_new = self.p - 1

    def setDec(self):
        self.p_new = self.p + 1

    def swap(self, reg):
        self.stack[self.p] = reg
        self.p = self.p_new
        if self.p == self.length:
            self.p = self.p - 1
        if self.p == -1:
            self.p = 0
        return self.stack[self.p]

    def printStack(self):
        print self.stack

class up2PcStack:
    ''' Model of the up2 processor PC stack sections '''

    def __init__(self, length):
        self.stack = []
        self.length = length
        for i in range(0,self.length):
            self.stack.append(0)
        self.p = 0

        ''' Model assertions '''
        assert self.p >= 0, 'Stack out of range'

    def push(self, reg):
        self.stack[self.p] = reg
        self.p += 1
        if self.p == self.length:
            self.p = 0
        return self.stack[self.p]

    def pop(self):
        self.p -= 1
        if self.p == -1:
            self.p = self.length -1
        return self.stack[self.p]

    def printStack(self):
        print self.stack


class up2Fetch:
    ''' Model of the up2 processor fetch section '''

    def __init__(self, codes):
        self.u = up2Utils()
        self.N = len(codes)
        self.pc = 0
        self.index = 0
        self.code = [0] * self.N

        ''' Turn input string in to array '''
        i = 0
        for code in codes:
            self.code[i] = int(code,16)
            i += 1

        ''' Model assertions '''
        assert (self.pc + self.index) < len(self.code), 'Entered invalid code space'

    def ir(self):
        return self.code[self.pc + self.index]

    def getNibble(self):
        return self.code[self.pc]

    def getStrNibble(self):
        return str(hex(self.code[self.pc])[2]).upper()

    def getPc(self):
        return self.pc

    def incPc(self):
        self.pc += 1

    def relPc(self):
        self.pc += self.ir(1)

    def absPc(self):
        self.pc = self.calcAbsPc()

    def calcAbsPc(self):
        pc = 0
        for i in range(1, self.u.fit(self.N,4)+1):
            pc = (pc << 4) + self.ir(i)
        return pc

    def setPc(self, pc):
        self.pc = pc

    def printCode(self):
        print "        POS:",
        for i in range(0,len(self.code)):
            print i,
            #self.u.padding(len(str(i)))
        print
        print "       CODE:",
        for i in range(0,len(self.code)):
            print str(self.code[i]) + self.u.padding(len(str(i))-len(str(self.code[i]))-1),
        print
        print "CODE LENGTH: " + str(len(self.code))
        print "      CLOG2: " + str(self.u.clog2(len(self.code)))

    def printState(self):
        print "N=" + str(self.N),
        print "FIT=" + str(self.u.fit(self.N,4)),
        print "PC=" + str(self.pc),
        print "IR0=" + str(self.ir(0)),
        print "ABS=" + str(self.calcAbsPc()),
        print

class up2Main:
    ''' Model of the up2 processor main memory section '''

    def __init__(self, addr_nibbles, data_nibbles):
        self.u = up2Utils()
        self.mem_addr = int(self.u.pow2(addr_nibbles * 4))
        self.mem_data = int(self.u.pow2(data_nibbles * 4))
        self.mem = [0] * self.mem_addr
        self.addr_nibbles = addr_nibbles
        self.data_nibbles = data_nibbles
        self.addr = 0
        self.data = 0

        ''' Model Asertions '''
        assert self.addr < self.mem_addr, "Address out of range"
        assert self.data < self.mem_data, "Data out of range"

    def shift(self, data):
        # Create masks
        addr_mask = int(self.u.pow2(self.addr_nibbles*4) - 1)
        data_mask = int(self.u.pow2(self.data_nibbles*4) - 1)
        # Access top nibbles
        out_addr = self.addr >> (4 * (self.addr_nibbles - 1))
        out = self.data >> (4 * (self.data_nibbles - 1))
        # Shift in new data
        self.addr = ((self.addr << 4) & (addr_mask)) | data
        self.data = ((self.data << 4) & (data_mask)) | out_addr
        return out

    def swap(self):
        data = self.mem[self.addr]
        self.mem[self.addr] = self.data
        self.data = data

    def printShift(self):
        print "Shift: ",
        print "Addr: " + str(hex(self.addr)) + "\t",
        print "Data: " + str(hex(self.data))

    def printMain(self):
        for i in range(0, len(self.mem)):
            print hex(i).split('x')[1].upper() , hex(self.mem[i]).split('x')[1].upper()


