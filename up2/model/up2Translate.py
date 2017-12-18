#!/usr/bin/python

class up2Translate:

    cmds={
        "ADD"           :   "0",
        "SUB"           :   "1",
        "OOR"           :   "2",
        "NOR"           :   "3",
        "XOR"           :   "4",
        "NAN"           :   "5",
        "LSL"           :   "6",
        "LSR"           :   "7",
        "BNE"           :   "8",
        "BEQ"           :   "9",
        "JMP"           :   "A",
        "INT"           :   "B",
        "SHM"           :   "C",
        "MEM"           :   "D",
        "DSP"           :   "E",
        "PSP"           :   "F"
    }

    muxes={
        "R0,1,R1"       :   "0",
        "R1,1,R1"       :   "1",
        "R2,1,R1"       :   "2",
        "R?,1,R1"       :   "3",
        "R0,R0,R1"      :   "4",
        "R1,R0,R1"      :   "5",
        "R2,R0,R1"      :   "6",
        "R?,R0,R1"      :   "7",
        "R0,1,R2"       :   "8",
        "R1,1,R2"       :   "9",
        "R2,1,R2"       :   "A",
        "R?,1,R2"       :   "B",
        "R0,R0,R1"      :   "C",
        "R1,R0,R1"      :   "D",
        "R2,R0,R1"      :   "E",
        "R?,R0,R1"      :   "F"
    }

    use_muxes={
        "ADD",
        "SUB",
        "OOR",
        "NOR",
        "XOR",
        "NAN",
        "LSL",
        "LSR"
    }

    use_address={
        "BNE",
        "BEQ",
        "JMP"
    }

    is_single={
        "INT",
        "SHM",
        "MEM",
        "DSP",
        "PSP"
    }