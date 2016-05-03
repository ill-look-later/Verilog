#!/usr/bin/python
import os
import platform
import subprocess
from optparse import OptionParser




if "__main__" == __name__:
    parser = OptionParser(usage="runsim.py [-m module] [-s do a sim] [-w view waves]" )
    parser.add_option("-m", "--module", dest="module", help="module to simulate - should not be defined if program is")
    parser.add_option("-s", "--sim", action="store_true", dest="sim")
    parser.add_option("-w", "--waves", action="store_true", dest="waves")
    parser.add_option("-y", "--synth",action="store_true", dest="synth")
    (options, args) = parser.parse_args()

    sim = str(options.module)

    move = "cd " + sim
    os.chdir(sim)

    temp =  str(sim) + "_runsim.txt"

    yosys = str(sim) + "_yosys.ys"

    yosys_out = str(sim) + "_yosys_out.txt"

    print
    print "--- runsim.py ---"
    print "  Module: "+ sim
    print "    Move: " + move + "/"

    if((options.sim == None) and (options.waves == None)):
        print "    Info: You must specify and operation"


    if(options.sim):
        print "    Info: Searching for simulation dependants"
        code = "code"
        if(os.path.isdir(code)):
            os.chdir(code)
            print "    Move: " + code + "/"
            for file in os.listdir("."):
                if file.endswith(".asm"):
                    cmd = "python assembler.py -c " + str(file) + " > " + str(file).replace(".asm",".txt")
                    print "     Cmd: " + cmd
                    os.system(cmd)
            os.chdir("..")



        print "    Info: Simulate " + str(sim)
        cmd = "iverilog -o " + str(sim) + ".dat -c " + str(sim) +"_filelist.txt"
        print "     Cmd: " + cmd
        os.system(cmd)



        cmd = "vvp " + str(sim) + ".dat -vcd > " + temp
        print "     Cmd: " + cmd
        os.system(cmd)


        print "    Info: Head of " + temp
        f = open(temp)
        count = 1
        for line in f:
            print "    Info: " + line,
            count = count + 1
            if(count > 15):
                break


    if(options.synth):
        print "    Info: Synth"
        f = open(yosys, "w")
        f.write("read_verilog " + sim + ".v")
        f.close()
        cmd = "yosys " + yosys + " > " + yosys_out
        print "     Cmd: " + cmd
        os.system(cmd)


    if(options.waves):
        cmd = "gtkwave " + str(sim) +".vcd"
        print "     Cmd: " + cmd
        os.system(cmd)

    print
    print "DONE"
    print
