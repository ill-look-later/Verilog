#!/usr/bin/python
import os
from os import listdir
from os.path import isfile, join

nm2hex = {
    'ADD'	: '0',
    'SUB'	: '1',
    'MUL'	: '2',
    'NAND'	: '3',
    'SW01'	: '4',
	'SW12'	: '5',
    'SW23'	: '6',
    'BE'	: '7',
    'POPC'	: '8',
    'PUSHC'	: '9',
    'POP'	: 'A',
    'PUSH'	: 'B',
    'LDW'	: 'C',
    'STW'	: 'D',
    'REF'	: 'E',
    'INT'	: 'F'
}


c = open("code.asm","r")
hx = ['0'] * 256


i = 0;
for line in c:
    if(i < 8):
        hx[i] = line.rstrip()
    else:
        hx[i] = nm2hex[line.rstrip()]


    if(i == 9):
        print ""
        print "Reg R0:  \t0x" + hx[0] +  hx[1]
        print "Reg R1:  \t0x" + hx[2] +  hx[3]
        print "Reg R2:  \t0x" + hx[6] +  hx[7]
        print "Int Vect: \t0x" + hx[4] +  hx[5]
        print ""

    i = i + 1

print hx

v = open("up_memory.v", "wb")

# Write header
v.write("module up_memory(\n")
v.write("\tinput  wire\t\t\tclk,\n")
v.write("\tinput  wire\t\t\tnRst,\n")
v.write("\tinput  wire\t[7:0]   in,\n")
v.write("\tinput  wire\t[7:0]   address,\n")
v.write("\tinput  wire\t\t\twe,\n")
v.write("\toutput wire\t[7:0]   out,\n")
v.write("\toutput wire\t\t\tre\n")
v.write(");\n\n")

v.write("\treg [7:0] mem [255:0];\n\n")

v.write("\tassign out = mem[address];\n")
v.write("\tassign re = 1'b1;\n\n")

v.write("\talways@(posedge clk or negedge nRst) begin\n")
v.write("\t\tif(!nRst) begin\n")

for i in range(0,128):
	v.write("\t\t\tmem[" + str(i) +"] <= 8'h" + str(hx[(i*2)]) + str(hx[(i*2) + 1]) + ";\n")

v.write("\t\tend else begin\n")
v.write("\t\t\tif(we) mem[address] <= in;\n")
v.write("\t\tend\n")
v.write("\tend\n")

#
v.write("\nendmodule")


v.close()



