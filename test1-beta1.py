import string
import numbers
from dictionaries import *


def is_hex(s):
    hex_digits = set(string.hexdigits)
    # if s is long, then it is faster to check against a set
    return all(c in hex_digits for c in s)


def is_hex(s):
    try:

        int(s, 16)
        return True
    except ValueError:
        return False

def getPC(op, operand):
    if op.upper() in dict:
        return dict[op.upper()]
    elif op.upper() == 'RESB':
        return int(operand)
    elif op.upper() == 'RESW':
        return 3 * int(operand)
    elif op.upper() == 'WORD':
        y = operand.split(',')
        return 3 * len(y)
    elif op.upper() == 'BYTE':
        if "c'" in str(operand).lower():
            return  len(operand) - 3
        if "x'" in str(operand).lower():
            return int(3*len(operand)-3)+1

    else:
        # print("elseeeee")
        return 0



def readFile():
    global lineCounter, commentCounter,programCounter,foundStart
    file = open('input.txt', 'r')
    for line in file:
        if line[0] == "\n":
            continue
        if line[-1] == "\n":
            line = line[:-1]
        if line[0] == ".":
            comment[lineCounter] = line
            opcode[lineCounter] = 0
            operand[lineCounter] = 0
            label[lineCounter] = 0
            address[lineCounter+1] = programCounter
            commentCounter = commentCounter + 1
            lineCounter = lineCounter + 1
            continue
        elif line[0] == " ":
            line = " " + " ".join(line.split())
        else :
            line = " ".join(line.split())
        fields = line.split(" ")
        if len(fields) < 3:
            operand[lineCounter] = 0
        else:
            operand[lineCounter] = fields[2]
        if len(fields) < 2:
            opcode[lineCounter] = "@"
        else:
            opcode[lineCounter] = fields[1]
        label[lineCounter] = fields[0]
        comment[lineCounter] = 0
        #opcode[lineCounter] = fields[1]
        if opcode[lineCounter].lower() == "start" and foundStart == 0:
            programCounter = int(operand[lineCounter], 16)
            # print(hex(programCounter))
        elif  opcode[lineCounter].lower() == "org":
            programCounter = int(operand[lineCounter], 16)
        else:
            # print(str(opcode[lineCounter]),str(operand[lineCounter]))
            programCounter = programCounter+getPC(opcode[lineCounter],operand[lineCounter])
        lineCounter += 1
        address[lineCounter] = programCounter
        address[0]=address[1]
    file.close()


def writeFile():
    global lineCounter
    file = open('output.txt','w')
    file.write("Symbol table\n")
    file.write("name\taddress")
    for i in range(lineCounter):
        if label[i] != "" and label[i] != 0:
            file.write(str(label[i])+"\t"+str(hex(address[i])).upper()+"\n")

    file.write("*************************************************************\n")
    file.write("Line no.\t" + "Address\t" + "Label\t" + "Op-code\t" + "Operands\t" + "Comments\n")
    for i in range(lineCounter):
        err = checkForError(i)

        if comment[i] == 0:
            if operand[i] != 0:
                file.write(str(i+1) + "\t" + str(hex(address[i])).upper() + "\t" + str(label[i]) + "\t" + str(opcode[i]) + "\t" + str(
                operand[i]) + "\n" )
            else:
                file.write(str(i + 1) + "\t" + str(hex(address[i])).upper() + "\t" + str(label[i]) +"\t" + str(opcode[i]) +"\n")

        else:
            file.write(str(i+1) +"\t"+str(comment[i]) + "\n")
        if err != 0:
            file.write(str(err) + "\n")
    file.close()




def isString(s):
    i = len(s)-1
    print(s[i])
    while i:
        if (s[i] >= "a" and s[i] <= "z") or (s[i] >= "A" and s[i] <= "Z"):
            return "true"
        i -= 1
    return "false"


def checkForError(i):
    global lineCounter
    err = 0

    for j in range(i):
        if label[i] == label[j] and label[j] != 0 and label[j] != "" :
            err = "\t-----ERROR: duplicate label "+label[i]+"-----"
            break

    if label[i] != "" and label[i] !=0 and (str(opcode[i]).lower() == "end" or str(opcode[i]).lower() == "org") :
        err = "\t-----ERROR: this statement can’t have a label "
    elif opcode[i]== "@" :
        err = "\t-----ERROR: missing operation-----"
    elif str(opcode[i]).lower() in directives:
        err = "\t-----ERROR: wrong operation prefix "+opcode[i]+"-----"
    elif str(opcode[i]).lower() not in instructionDict and opcode[i] != 0:
        err = "\t-----ERROR:unrecognized operation code "+opcode[i]+"-----"
    elif isinstance(operand[i],str) and not(is_hex(str(operand[i][2:-1]))) and str(opcode[i]).lower() == "byte":
        err = "\t-----ERROR: not a hexadecimal string " + operand[i]+"-----"
    elif isinstance(opcode[i],str) and opcode[i] in notFormat4:
        err = "\t-----ERROR: cant be format 4: " + operand[i]+"-----"
    elif not("end" in str(opcode).lower()) and i == lineCounter-2:
        err = "\t-----ERROR: missing end statement-----"
    elif operand[i]==0 and not str(opcode[i]).lower()=="base" and not(isinstance(comment[i],str)):
        err = "\t-----ERROR: missing operand-----"
    elif (str(opcode[i]).lower() == "equ" or str(opcode[i]).lower() == "resw" or str(opcode[i]).lower() == "resb"\
            or str(opcode[i]).lower() == "byte" or str(opcode[i]).lower() == "word"):
        if str(label[i]) == "":
            err = "\t-----ERROR: missing label-----"

    elif str(opcode[i]).lower() in ropcodes:
        print (opcode[i])
        register=str(operand[i]).split(',')
        for k in range (len(register)):
            if register[k].lower() not in registers:
                err = "\t-----ERROR: illegal address for register-----"
                break
    elif isinstance(operand[i],str) and isinstance(opcode[i],str)   and not(opcode[i].upper() in directives)\
        and  operand[i][0:1].lower() != "x" and operand[i][0:1].lower() != "c":
            if operand[i][0:1] == "#" :
                if (isString(operand[i][1:]) == "true"):
                    found = 0
                    print(operand[i][1:])
                    for j in range(lineCounter):
                        if isinstance(label[j],int) :
                            continue
                        elif operand[i][1:] == label[j] :
                            print(operand[i] +"    "+label[j])
                            found = 1
                else:
                    found = 1
            elif  operand[i][0:1] != "#" and isString(operand[i][1:]) == "false":
                found = 1
            else :
                found =0
                # print(operand[i])
                for j in range(lineCounter):
                    if operand[i] == label[j]:
                        found = 1


            if found == 0:
                err = "\t-----ERROR: undefined symbol "+operand[i]+"-----"



    return err





readFile()
writeFile()
# for i in range(lineCounter):
#         print(errors[i])

# for i in range(lineCounter):
#     print(str(i)+" "+str(hex(address[i]))+" "+str(label[i])+" "+str(opcode[i])+" "+str(operand[i])+"\t"+str(comment[i]))
