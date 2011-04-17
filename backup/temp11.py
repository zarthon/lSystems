import sys
FILENAME="lsystems.txt"
AXIOM=None
RULES={}
ANGLE=None
VARIABLES=None

def file_handle():
    try:
        global AXIOM,RULES,ANGLE
        fin = open(FILENAME,"r")
        lineList = fin.readlines()
        fin.close()
        for line in lineList:
            temp = line.split(";")
            if temp[0] == "Va":
                VARIABLES = temp[1].rstrip()
            elif temp[0] == "Ax":
                AXIOM = temp[1].rstrip()
            elif temp[0] == "Ru":
                key, val = temp[1].rstrip().split(":")[0],temp[1].rstrip().split(":")[1]
                RULES[key] = val
            elif temp[0] == "An":
                ANGLE = int(temp[1].rstrip()) 
    except IOError:
        print "File Not Found"
        sys_exit(1)

file_handle()
print AXIOM
print RULES
print ANGLE
