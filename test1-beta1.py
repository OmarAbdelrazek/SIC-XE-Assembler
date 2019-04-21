address = {}
label = {}
opcode = {}
operand = {}
comment = {}
lineCounter = 0
commentCounter = 0
commentLocation = {}
programCounter = 0
currentAddress = 0
foundStart = 0

dict={'RMO': 2, 'LDCH': 3, 'STCH': 3, '+LDCH': 4, '+STCH': 4, 'ADD': 3, 'SUB': 3, 'ADDR': 3,
      '+ADD': 4, '+SUB': 4, '+ADDR': 4,'SUBR': 2,
      'COMP': 3, '+COMP': 4, 'COMPR': 2,
      'J': 3, 'JEQ': 3,'JLT': 3, 'JGT': 3, 'TIX': 3, 'TIXR': 2,
      '+J': 4, '+JEQ': 4,'+JLT': 4, '+JGT': 4, '+TIX': 4,
      'LDA' : 3 , 'STA': 3,'+LDA': 4, '+STA': 4,'LDB': 3, 'STB': 3,'+LDB': 4, '+STB': 4,
      'LDL': 3, 'STL': 3,'+LDL': 4, '+STL': 4,'LDS': 3, 'STS': 3,'+LDS': 4, '+STS': 4,
      'LDX': 3, 'STX': 3,'+LDX': 4, '+STX': 4,'LDT': 3, 'STT': 3,'+LDT': 4, '+STT': 4}

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
        if "c'" in operand:
            return  len(operand) - 3
    else:
        # print("elseeeee")
        return 0



def readFile():
    global lineCounter, commentCounter,programCounter,foundStart
    file = open('input.txt', 'r')
    for line in file:
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
        label[lineCounter] = fields[0]
        comment[lineCounter] = 0
        opcode[lineCounter] = fields[1]
        if opcode[lineCounter].lower() == "start" and foundStart == 0:
            programCounter = int(operand[lineCounter],16)
            # print(hex(programCounter))
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
        print("OUTPUT")
        if comment[i] == 0:
            if operand[i] != 0:
                file.write(str(i+1) + "\t" + str(hex(address[i])).upper() + "\t" + str(label[i]) + "\t" + str(opcode[i]) + "\t" + str(
                operand[i]) + "\n" )
            else:
                file.write(str(i + 1) + "\t" + str(hex(address[i])).upper() + "\t" + str(label[i]) +"\t" + str(opcode[i]) +"\n")

        else:
            file.write(str(i+1) +"\t"+str(comment[i]) + "\n")
    file.close()


readFile()
writeFile()
# for i in range(lineCounter):
#     print(str(i)+" "+str(hex(address[i]))+" "+str(label[i])+" "+str(opcode[i])+" "+str(operand[i])+"\t"+str(comment[i]))