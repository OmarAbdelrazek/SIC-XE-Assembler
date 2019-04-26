address = {}
label = {}
opcode = {}
operand = {}
comment = {}
errors = {}
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
notFormat4 = {"+rmo","+subr","+comr","+tixr"}
format4Only = {"+LDr","+STr","+LDCH","+STCH","+ADD","+SUB","+ADDR","+COMP","+J","+JEQ","+JLT","+JGT","+TIX","+LDA","+STA"}
directives = {"START","END","BYTE","WORD","RESW","RESB","EQU","ORG","BASE"}
instructionDict = {"rmo","ldr","+ldr","str","+str","ldch","+ldch","stch","+stch","add","+add","lda","+lda","sta","+sta"
                   "sub","+sub","addr","+addr","subr","+subr","comp","+comp","comr","j","ldx","+ldx"
                   "jeq","+jeq","jlt","+jlt","jgt","+jgt","tix","+tix","tixr","+j","start","end","byte","word","resw",
                   "resb",
                   "equ","org","base"}