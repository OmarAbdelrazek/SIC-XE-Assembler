address = {}
label = {}
opcode = {}
operand = {}
comment = {}
lineCounter = 0
commentCounter = 0
commentLocation = {}
programCounter = 0

def readFile():
    global lineCounter,commentCounter
    file = open('input.txt','r')
    for line in file:
        fields = line.split(" ")
        # print(fields)
        if fields[0][:1] == ".":
            temp =' '.join(fields)
            comment[lineCounter] = temp[:-1]
            opcode[lineCounter] = 0
            operand[lineCounter] =0
            commentCounter = commentCounter +1
            # print(comment.get(lineCounter))
            # print(comment[lineCounter])
            lineCounter = lineCounter + 1
            continue

        elif fields[1][:1] != "#" and( fields[0].lower() == "rmo" or fields[0].lower() == "addr"\
                    or  fields[0].lower() == "subr" or  fields[0].lower() == "comr"\
                    or  fields[1].lower() == "start" or fields[1].lower() == "byte" or \
                    fields[1].lower() == "word" or fields[1].lower() == "resw" or \
                    fields[1].lower() == "resb" or fields[1].lower() == "equ" or fields[1].lower() == "lda"):
                label[lineCounter] = fields[0].lower()
                opcode[lineCounter] =fields[1].lower()
                operand[lineCounter]= fields[2][:-1]
                comment[lineCounter] = 0
                # print(str(label.get(lineCounter)) + '\t' + str(opcode.get(lineCounter)) + '\t' + str(
                #     operand.get(lineCounter)))
                lineCounter = lineCounter + 1
                continue
        elif  fields[1][:1]=='#' or fields[0].lower()=='ldr'  or fields[0].lower() == "str"\
            or fields[0].lower() == "ldch" or fields[0].lower() == "stch" \
            or fields[0].lower() == "add" or fields[0].lower() == "sub" or fields[0].lower() == "comp"\
            or fields[0].lower() == "j" or fields[0].lower() == "jeq" or fields[0].lower() == "jlt"\
            or fields[0].lower()=="jgt" or fields[0].lower()=="tix" or fields[0].lower()== "tixr"\
                    or fields[0].lower() == "end":
                label[lineCounter] = 0
                if '\n' in fields[1]:
                    operand[lineCounter]= fields[1][:-1]
                else:
                    operand[lineCounter] = fields[1]
                opcode[lineCounter] =fields[0].lower()
                comment[lineCounter] = 0
                # print(str(opcode.get(lineCounter)) +'\t'+str( operand.get(lineCounter)))

                lineCounter = lineCounter + 1
                continue
    file.close()

def printArr():
    global lineCounter
    print(operand.get(6))
    for i in range(lineCounter):
        if  comment.get(i) != 0:
            print(comment.get(i))

        elif '#' in operand.get(i) or str(opcode.get(i)) =="ldr" or str(opcode.get(i)) == "str"\
            or str(opcode.get(i)) == "ldch" or str(opcode.get(i)) == "stch" \
            or str(opcode.get(i)) == "add" or str(opcode.get(i)) == "sub" or str(opcode.get(i)) == "comp"\
            or str(opcode.get(i)) == "j" or str(opcode.get(i)) == "jeq" or str(opcode.get(i)) == "jlt"\
            or str(opcode.get(i))=="jgt" or str(opcode.get(i))=="tix" or str(opcode.get(i))== "tixr"\
                    or str(opcode.get(i)) == "end":
            print(str(opcode.get(i)) + '\t' + str(operand.get(i)))

        elif i in label and i in operand  and i in operand and (label.get(i))  != 0:
            print(str(label.get(i))+'\t' +str(opcode.get(i))+ '\t'+str(operand.get(i)))







readFile()
printArr()