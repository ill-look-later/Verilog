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
        self.updateZeroFlag()

    def sub(self):
        ''' Sub with underflow wrap around '''
        self.regs[self.c] = self.regs[self.b] - self.regs[self.a]
        if self.regs[self.c] < 0:
            self.regs[self.c] += 16
        self.updateZeroFlag()

    def updateZeroFlag(self):
        '''Flag after ALU update '''
        if 0 == self.regs[self.c]:
            self.z = 1
        else:
            self.z = 0

    def readZeroFLag(self):
        return self.z

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

class up2Stack:
    ''' Model of the up2 processor stack sections '''

    def __init__(self):
        self.stack = []
        self.p = 0

        ''' Model assertions '''
        assert self.p >= 0, 'Stack out of range'

    def push(self, reg):
        if len(self.stack) == self.p:
            self.stack.append(reg)
        else:
            self.stack[self.p] = reg
        self.p += 1

    def pop(self):
        if 0 < self.p:
            self.p -= 1
        reg = self.stack[self.p]
        return reg

    def ptr(self):
        return self.p

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

    def ir(self, index):
        self.index = index
        return self.code[self.pc + self.index]

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




