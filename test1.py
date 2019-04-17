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
            #print(comment[lineCounter])
            lineCounter = lineCounter + 1
            continue


        else:

            label[lineCounter] = fields[0]
            if fields[1][:1] != "#":
                opcode[lineCounter] =fields[1]
                operand[lineCounter]= fields[2][:-1]
                comment[lineCounter] = 0
                lineCounter = lineCounter + 1
                continue
                # print(label.get(lineCounter) + '\t' + opcode.get(lineCounter) + '\t' + operand.get(lineCounter))
            else:
                operand[lineCounter]= fields[1]
                opcode[lineCounter] =0
                comment[lineCounter] = 0
                lineCounter = lineCounter + 1
                continue
                # print(label.get(lineCounter) + '\t'  + operand.get(lineCounter))
    file.close()

def printArr():
    global lineCounter

    for i in range(lineCounter):
        if  comment.get(i) != 0:
            print(comment.get(i))

        elif '#' in operand.get(i):
            print(str(label.get(i)) + '\t' + str(operand.get(i)))

        elif i in label and i in operand  and i in operand :
            print(str(label.get(i))+'\t' +str(opcode.get(i))+ '\t'+str(operand.get(i)))







readFile()
printArr()