#!/usr/bin/python
import re
from up2Utils import up2Utils as u
from up2Translate import up2Translate as t

class up2Assemble:
    ''' Assembler for up2 files '''

    def __init__(self, in_file, out_file):
        self.u = u()
        self.in_file = in_file
        self.out_file = out_file
        self.code = open(in_file, "r").read()
        self.resetErrorsAndWarnings()

    def resetErrorsAndWarnings(self):
        self.error = False
        self.warning = 0

    def printInfo(self, info):
        if "INFO" in self.print_option:
            print "    INFO: " + info

    def printWarning(self, warn):
        if "WARNING" in self.print_option:
            print " WARNING: " + warn
        self.warning += 1

    def printError(self, err):
        print "   ERROR: " + err
        self.error = True

    def printFinish(self):
        ''' Last line depends on errors and warnings '''
        if "INFO" in self.print_option:
            print "FINISHED:",
        if(self.error):
            print "ERROR"
            return False
        else:
            if "INFO" in self.print_option:
                if(0 == self.warning):
                    print "No warnings"
                elif(1 == self.warning):
                    print "1 warning"
                else:
                    print str(self.warning) + " warnings"
                return True

    def printStart(self):
        if "INFO" in self.print_option:
            print "   START: up2 assembler"

    def printHex(self):
        ''' Print output hexadecimal in a 16 wide grid '''
        top = "-"
        for i in range(0,len(self.out) / 256):
            top += "-"
        for i in range(0,16):
            top +=  "-" + str(hex(i))[2:]
        self.printInfo(top)
        line = "0"
        while len(line) != 2 + len(self.out) / 256:
            line += "-"
        for i in range(0,len(self.out)):
            line += self.out[i] + " "
            if (0 == (i + 1) % 16) and (0 != i) and (i+1 != len(self.out)):
                self.printInfo(line)
                line = str(hex((i + 1) / 16))[2:]
                while len(line) != 2 + len(self.out) / 256:
                    line += "-"
        self.printInfo(line)

    def writeHex(self):
        self.printInfo("Writing " + str(self.out_file))
        open(self.out_file, "w").write(self.out)

    def removeWhiteSpace(self, line):
        return line.replace(" ","").replace("\t","")

    def assemble(self, print_option):
        ''' Set print option '''
        self.print_option = print_option

        ''' Run the assembler sequence '''
        self.printStart()
        self.resetErrorsAndWarnings()
        code = self.code.split("\n")
        self.out = ""

        ''' Determine suitable memory size to use'''
        mem_size = 16
        done = False
        while not done:
            labels = {}
            address_width = self.u.clog2(mem_size)
            nibbles = self.u.fitNibbles(address_width)
            self.printInfo("Using a width of " + str(address_width) + " inside " + str(nibbles) + " nibbles to provide a memory size of " + str(mem_size))
            required_mem_size = 0
            for line in code:
                line = self.removeWhiteSpace(line.split("#")[0])
                if ":" in line:
                    label = line.split(':')[0]
                    if label in labels:
                        self.printError("label \'" + label + "\' declared more than once")
                        done = True
                    labels[label] = required_mem_size
                for mux in t.use_muxes:
                    if mux in line:
                        required_mem_size += 2
                for single in t.is_single:
                    if single in line:
                        required_mem_size += 1
                for address in t.use_address:
                    if address in line:
                        required_mem_size += (1 + nibbles)
            if self.error:
                done = True
            else:
                if required_mem_size <= mem_size:
                    for label in labels:
                        self.printInfo("Label \'" + label + "\' assigned address " + str(hex(labels[label])))
                    done = True
                else:
                    self.printInfo("Required memory size calculated as " + str(required_mem_size))
                    mem_size = required_mem_size
        ''' Check for invalid labels '''
        for label in labels:
            for c in t.cmds:
                if c in label:
                    self.printError("Invalid label")


        ''' Keep track of labels used '''
        unused_labels = labels.copy()

        ''' Turn operations in to hex '''
        for ptr in range(0,len(code)):
            if False == self.error:
                line = code[ptr]
                self.printInfo("Assembling line " + str(ptr))
                found = 0

                ''' Remove white space '''
                line = self.removeWhiteSpace(line)
                self.printInfo("\t" + line)

                ''' Remove comments '''
                if 1 < len(line.split('#')):
                    self.printInfo("\tRemoving comment")
                    line = line.split('#')[0]
                    self.printInfo("\t" + line)

                ''' Remove label declarations '''
                if ":" in line:
                    line = line.split(":")[1]

                ''' Mux operation '''
                for op in t.use_muxes:
                    for mux in t.muxes:
                        if (op in line) and (mux in line):
                            add = t.cmds[op] + t.muxes[mux]
                            self.out += add
                            self.printInfo("\tAppending output hex with " + add)
                            found += 1

                    ''' Try looking for shorts '''
                    if 0 == found:
                        for short in t.short_muxes:
                            if (op in line) and (short in line):
                                swap = t.short_muxes[short]
                                self.printInfo("\tReplacing " + short + " with" + swap)
                                add = t.cmds[op] + t.muxes[swap]
                                self.out += add
                                self.printInfo("\tAppending output hex with " + add)
                                found += 1

                    ''' Try mixing the mux select '''
                    if 0 == found:
                        for mux in t.muxes:
                            seg = mux.split(",")
                            mix = seg[0] + "," + seg[2] + "," + seg[1]
                            if (op in line) and (mix in line):
                                add = t.cmds[op] + t.muxes[mux]
                                self.out += add
                                self.printWarning("\tUsing " + mux + " instead of " + mix)
                                self.printInfo("\tAppending output hex with " + add)
                                temp_line = line.replace(mix,mux)
                                self.printInfo("\t" + temp_line)
                                found += 1

                ''' Address operations '''
                for address in t.use_address:
                    for label in labels:
                        if (address + label) == line:
                            self.printInfo("\tLabel \'" + label + "\' points to address " + str(labels[label]))
                            add = t.cmds[address] + hex(labels[label])[2:].zfill(nibbles).upper()
                            self.out += add
                            self.printInfo("\tAppending output hex with " + add)
                            if label in unused_labels:
                                del unused_labels[label]
                            found += 1

                ''' Single nibble operations '''
                for single in t.is_single:
                    if single in line:
                        add = t.cmds[single]
                        self.out += add
                        self.printInfo("\tAppending output hex with " + add)
                        found += 1

                ''' Check assembled as expected '''
                if 1 != found:
                    if 0 != len(line):
                        self.printError("\tMalformed assembly")

        ''' Check labels used '''
        for label in unused_labels:
            self.printWarning("Label \'" + label + "\' decalred but not referenced")

        ''' Output file if no errors '''
        if(False == self.error):
            self.writeHex()
            self.printHex()

        return self.printFinish()






