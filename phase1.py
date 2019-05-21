import string
import re
import ast
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

    if op.upper() == 'RESB':
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
    elif op.upper() in dict:
        return dict[op.upper()]

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
    file.write("\t\t\tSymbol table\n")
    file.write("\t\t"+"name\t\taddress\n")
    for i in range(lineCounter):
        if label[i] != "" and label[i] != 0:
            # file.write("\t\t"+str(label[i])+"        "+str(hex(address[i])).upper()+"\n")
            file.write('\t\t{} \t\t{}'.format(str(label[i]), str(hex(address[i])).upper())+"\n")
    file.write("*************************************************************\n")
    file.write("Line no.\t" + "Address\t" + "Label\t" + "Op-code\t" + "\t\tOperands\t" + "Comments\t"+"\n")
    for i in range(lineCounter):
        err = checkForError(i)

        if comment[i] == 0:
            if operand[i] != 0:
                if opcode[i].lower()=="equ":
                    file.write(str(i + 1) + "\t\t" + str(hex(address[i-1])).upper() + "\t\t" + str(label[i]) + "\t\t\t\t" + str(
                        opcode[i]) + "\t\t" + str(
                        operand[i]) + "\n")

                else:
                    file.write(str(i+1) + "\t\t" + str(hex(address[i])).upper() + "\t\t" + str(label[i]) + "\t\t" + str(opcode[i]) + "\t\t\t\t" + str(
                    operand[i]) + "\t\t"+"\n" )
            else:
                file.write(str(i + 1) + "\t\t" + str(hex(address[i])).upper() + "\t\t" + str(label[i]) +"\t\t" + str(opcode[i]) +"\n")

        else:
            file.write(str(i+1) +"\t\t"+str(comment[i]) +"\t\t"+ "\n")
        if err != 0:
            file.write(str(err) + "\n")
    file.close()

def isString(s):
    for i in range(0 , len(s)):
        if (s[i] >= "a" and s[i] <= "z") or (s[i] >= "A" and s[i] <= "Z"):
            return  "true"
            continue

        else:
            return "false"



def checkForError(i):
    global lineCounter,errorFound
    err = 0

    for j in range(i):
        if label[i] == label[j] and label[j] != 0 and label[j] != "" and isinstance(opcode[i],str) and opcode[i].lower() != "equ" :
            errorFound = 1
            err = "\t-----ERROR: duplicate label "+label[i]+"-----"
            break

    if label[i] != "" and label[i] !=0 and (str(opcode[i]).lower() == "end" or str(opcode[i]).lower() == "org") :
        errorFound = 1
        err = "\t-----ERROR: this statement can’t have a label "
    elif opcode[i]== "@" :
        errorFound = 1
        err = "\t-----ERROR: missing operation-----"
    elif str(opcode[i]).lower() in directives:
        errorFound = 1
        err = "\t-----ERROR: wrong operation prefix "+opcode[i]+"-----"
    elif str(opcode[i]).lower() not in instructionDict and opcode[i] != 0:
        errorFound = 1
        err = "\t-----ERROR:unrecognized operation code "+opcode[i]+"-----"
    elif isinstance(operand[i],str) and not(is_hex(str(operand[i][2:-1]))) and str(opcode[i]).lower() == "byte":
        errorFound = 1
        err = "\t-----ERROR: not a hexadecimal string " + operand[i]+"-----"
    elif isinstance(opcode[i],str) and opcode[i] in notFormat4:
        errorFound = 1
        err = "\t-----ERROR: cant be format 4: " + operand[i]+"-----"
    elif not("end" in str(opcode).lower()) and i == lineCounter-2:
        errorFound = 1
        err = "\t-----ERROR: missing end statement-----"
    elif operand[i]==0 and not str(opcode[i]).lower()=="base" and not(isinstance(comment[i],str)):
        errorFound = 1
        err = "\t-----ERROR: missing operand-----"
    elif (str(opcode[i]).lower() == "equ" or str(opcode[i]).lower() == "resw" or str(opcode[i]).lower() == "resb"\
            or str(opcode[i]).lower() == "byte" or str(opcode[i]).lower() == "word"):
        if str(label[i]) == "":
            errorFound = 1
            err = "\t-----ERROR: missing label-----"

    elif str(opcode[i]).lower() in ropcodes:
        # print (opcode[i])
        register=str(operand[i]).split(',')
        for k in range (len(register)):
            if register[k].lower() not in registers:
                errorFound = 1
                err = "\t-----ERROR: illegal address for register-----"
                break
    elif isinstance(operand[i], str) and isinstance(opcode[i], str) and not (opcode[i].upper() in directives) \
            and operand[i][0:1].lower() != "x" and operand[i][0:1].lower() != "c":

        err = undeinedCheck(i)
    return err




def undeinedCheck(i):
    global errorFound
    if "+" in operand[i] or "-" in operand[i]:
        splittedOperand = re.split("[+ -]",operand[i])
        # print((splittedOperand))
        for j in range(len(splittedOperand)):
            if isinstance(splittedOperand[j], str) and isinstance(opcode[i], str) and not (opcode[i].upper() in directives) \
                    and splittedOperand[j][0:1].lower() != "x" and splittedOperand[j][0:1].lower() != "c":
                if isString(splittedOperand[j]) == "false":
                    found = 1
                    break
                else:

                    err = 0
                    # print("111111")

                    if   splittedOperand[j][0:1] == "#" or  splittedOperand[j][0:1] == "@" :
                        if (isString(splittedOperand[j][1:]) == "true"):

                            found = 0
                            # print(operand[i][1:])
                            for k in range(lineCounter):
                                if isinstance(label[k], int):
                                    continue
                                elif splittedOperand[k][1:] == label[k]:
                                    # print(operand[i] +"    "+label[j])
                                    found = 1
                        else:
                            found = 1

                    elif splittedOperand[j][0:1] != "#" and isString(splittedOperand[j][1:]) == "false":
                        found = 1

                    else:

                        found = 0
                        # print(operand[i])
                        print(splittedOperand[j])
                        for l in range(lineCounter):
                            if splittedOperand[j] == label[l]:
                                found = 1
                    if found == 0:
                        errorFound = 1

                        err = "\t-----ERROR: undefined symbol " + splittedOperand[j] + "-----"
                        break


        return err
    else:
        sop = operand[i]
        if ",x" in operand[i] :
            sop = operand[i].replace(",x",'')
        if  ",X" in operand[i]:
            sop = operand[i].replace(",X", '')
        if isinstance(sop, str) and isinstance(opcode[i], str) and not (opcode[i].upper() in directives) \
                and sop[0:1].lower() != "x" and sop[0:1].lower() != "c":
            err = 0
            if sop[0:1] == "#" or sop[0:1] == "@":
                if (isString(sop[1:]) == "true"):
                    found = 0
                    # print(sop[1:])
                    for j in range(lineCounter):
                        if isinstance(label[j], int):
                            continue
                        elif sop[1:] == label[j]:
                            # print(sop +"    "+label[j])
                            found = 1
                else:
                    found = 1
            elif sop[0:1] != "#" and isString(sop[1:]) == "false":
                found = 1
            else:
                found = 0
                # print(operand[i])
                for j in range(lineCounter):
                    if sop == label[j]:
                        found = 1

            if found == 0:
                errorFound = 1
                err = "\t-----ERROR: undefined symbol " + sop + "-----"
        return err














def headerRecord():
    global lineCounter
    header = "H^"
    for i in range(lineCounter):
        if label[i] != "" and label[i] != 0 and opcode[i].lower() == "start":
            header = header + str(label[i])+"^"+str(operand[i])+"^"
    header = header + str(hex(address[lineCounter]-address[0]))[2:]
    return header

def endRecord():
    return "E^"+str(hex(address[0]))[2:].upper()

def getObjectCode(format,i):
    if format == 2:
        objectCode = str(hex(obTableHex.get(opcode[i].upper())))[2:].upper()
        splittedOperand = operand[i].split(',')
        opject = objectCode + str(registersOpcodeHex.get(splittedOperand[0].upper())).upper() +\
                     str(registersOpcodeHex.get(splittedOperand[1].upper())).upper()
        # print(objectCode)

    else:
        objectCode = obTable.get(opcode[i].upper())
        print(opcode[i])
        objectCode=objectCode[0:6]
        flg="000000"
        flags=list(flg)
        opr=operand[i]
        if operand[i][0]=="@":
            flags[0]="1"
            opr=opr[1:]
        elif operand[i][0]=="#":
            flags[1]="1"
            opr=opr[1:]
        if ",X" in operand[i]:
            flags[2]="1"
            opr=opr.replace(",X",'')
        if ",x" in operand[i]:
            flags[2]="1"
            opr=opr.repLDBlace(",x",'')
        label_found=0
        for j in range(lineCounter):
            if label[j] == opr.upper():
                adr = address[j]
                label_found=1
                break
        if label_found==0:
            oprcheck = re.split("[+ -]",opr)
            if len(oprcheck) > 1:
                adr = simpleExpressionEvaluation(i)
                print("lllllllll")
                print(str(hex(adr)))
            else:
                adr=int(opr,10)
        if format==3:
            if flags[0]=="0" and flags[1]=="0":
                flags[0]="1"
                flags[1]="1"
            flags[5]="0"
            if operand[i][0]=="#" and label_found==0:
                disp=adr
                disp=hex(disp).upper()
                disp=disp[2:]
            else:
                disp=adr-address[i+1]
                if disp<2047 or disp >-2048:
                    flags[4]="1"
                    flags[3]="0"
                elif disp<4095 and disp >0:
                    return "error in displacment"
                    flags[3]="1"
                    flags[4]="0"
                disp=hex(disp).upper()
                disp=disp[2:]
            while len(disp)<3:
                disp="0"+disp
            disp=disp[-3:]
            flg="".join(flags)
            opcodeWflag=getHexa(objectCode+flg)
            opject=opcodeWflag+disp
            # print(opcode[i])
            # print(opject)
        elif format==4:
            flags[5]="1"
            flags[3]="0"
            flags[4]="0"
            if flags[0] == "0" and flags[1] == "0":
                flags[0] = "1"
                flags[1] = "1"
            if operand[i][0] == "#" and label_found == 0:
                disp = adr
                disp = hex(disp).upper()
                disp = disp[2:]
            else:
                disp = hex(adr).upper()
                disp = disp[2:]
            while len(disp) < 5:
                disp = "0" + disp
            disp = disp[-5:]
            flg = "".join(flags)
            opcodeWflag = getHexa(objectCode + flg)
            opject = opcodeWflag + disp
            # print(opcode[i])
            # print('format 44:   '+opject)
    return opject



def getAddress(i):
    global lineCounter
    if operand[i][0:1] == "@":
        indirectFlag = 1
    if operand[i][0:1] == "#" or operand[i][0:1] == "@":
        target = operand[i][1:]
    else:
        target = operand[i]
    for j in range(lineCounter):
        if isinstance(label[j], str) and label[j].lower() == target.lower() :
            return address[j]

    return 0

def getB(i):
    global lineCounter
    value = 0
    if operand[i][0:1] == "#" or operand[i][0:1] == "@":
        target = operand[i][1:]

    for j in range(i,0,-1):
        if   opcode[j].lower() == "ldb":
            # print("innnnn")
            if isString(operand[j][1:]) == "true":
                value = getAddress(j)
                return value


            else:
                # print("in elseeee")
                value = operand[j][1:]
                return value







def textRecord(startAddress , endAddress):
    global lineCounter
    length = 0
    textR = "T^"+str(hex(startAddress))[2:]
    for i in range(lineCounter):
        if opcode[i] == 0 or opcode[i].lower() == "start" or opcode[i].lower() == "resw" or opcode[i].lower() == "resb"\
                or opcode[i].lower()=="word" or opcode[i].lower()=="end" or opcode[i].lower() == "equ"or opcode[i].lower() == "byte"\
                or opcode[i].lower() == "org":
            objectCodeList[i] = ""
            continue
        else:
            format = dict.get(opcode[i].upper())
            objectCode = getObjectCode(format,i)
            objectCodeList[i] = objectCode
            textR = textR + "^"+objectCode
            if  (i+1) < lineCounter :
                if opcode[i+1] == 0:
                    length = length + 0
                    continue
                # writeFile()(dict.get(opcode[i+1].upper()))
                print(opcode[i+1])
                length = length + dict.get(opcode[i+1].upper())
                print(length)
            if  length >= 30 :
                textR = textR + "\n" +  "T^"+str(hex(address[i]))[2:]
                length=0
    return textR


def getHexa(s):
    s = [s[i:i + 4] for i in range(0, len(s), 4)]
    out = binToHex.get(s[0]) + binToHex.get(s[1]) + binToHex.get(s[2])
    return  out

def objectFile():
    file=open("objFile.txt","w")
    global lineCounter
    h = headerRecord()
    e = endRecord()
    t = textRecord(address[0],address[lineCounter])
    file.write(h+"\n"+t+"\n"+e)


def getAddress(i):
    global lineCounter
    if operand[i][0:1] == "@":
        indirectFlag = 1
    if operand[i][0:1] == "#" or operand[i][0:1] == "@":
        target = operand[i][1:]
    else:
        target = operand[i]
    for j in range(lineCounter):
        if isinstance(label[j], str) and label[j].lower() == target.lower() :
            return address[j]

    return 0
def addressSearch(lbl):
    global lineCounter
    # print(lbl)
    for i in range(lineCounter):
        if isinstance(label[i],str) and label[i] == lbl:
            return address[i]
    return 0

def checkForEqu():
    global lineCounter
    for i in range(lineCounter):
        if isinstance(opcode[i],str) and opcode[i].lower() == "equ":
            adrs = getAddress(i)
            address[i] = adrs

def simpleExpressionEvaluation(i):
    strExpression = ""
    splittedOperando = re.split("([+ -])", operand[i].replace(" ", ""))
    for f in range(len(splittedOperando)):
        if splittedOperando[f] == "+":
            strExpression = str(strExpression) + "+"
        elif splittedOperando[f] == "-":
            strExpression = str(strExpression) + "-"
        elif isString(splittedOperando[f]) == "true":
            strExpression = strExpression + str(hex(addressSearch(splittedOperando[f])))
        elif isString(splittedOperando[f]) == "false":
            strExpression = strExpression + str(splittedOperando[f])
    print(strExpression)
    return (ast.literal_eval(str(strExpression)))


readFile()
for i in range(lineCounter):
    print(opcode[i])
checkForEqu()
if errorFound == 0:
    objectFile()
writeFile()
print("object code list")