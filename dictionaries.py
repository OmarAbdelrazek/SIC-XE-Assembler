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
      '+ADD': 4, '+SUB': 4,'SUBR': 2,
      'COMP': 3, '+COMP': 4, 'COMPR': 2,
      'J': 3, 'JEQ': 3,'JLT': 3, 'JGT': 3, 'TIX': 3, 'TIXR': 2,
      '+J': 4, '+JEQ': 4,'+JLT': 4, '+JGT': 4, '+TIX': 4,
      'LDA' : 3 , 'STA': 3,'+LDA': 4, '+STA': 4,'LDB': 3, 'STB': 3,'+LDB': 4, '+STB': 4,
      'LDL': 3, 'STL': 3,'+LDL': 4, '+STL': 4,'LDS': 3, 'STS': 3,'+LDS': 4, '+STS': 4,
      'LDX': 3, 'STX': 3,'+LDX': 4, '+STX': 4,'LDT': 3, 'STT': 3,'+LDT': 4, '+STT': 4}

notFormat4 = {"+rmo","+subr","+comr","+tixr"}

format4Only = {"+LDCH","+STCH","+ADD","+SUB","+COMP","+J","+JEQ","+JLT","+JGT","+TIX","+LDA","+STA",
               "+LDA","+STA","+LDL","+STL","+LDS","+STS","+LDT","+STT","+LDX","+STX","+LDB","+STB"}

directives = {"START","END","BYTE","WORD","RESW","RESB","EQU","ORG","BASE"}

instructionDict = {"rmo","lda","+lda","sta","+sta",
                   "ldb","+ldb","stb","+stb","ldx","+ldx","stx","+stx","lds","+lds","sts","+sts",
                   "ldl","+ldl","stl","+stl","ldt","+ldt","stt","+stt",
                   "ldch","+ldch","stch","+stch","add","+add",
                   "sub","+sub","addr","subr","comp","+comp","comr","j",
                   "jeq","+jeq","jlt","+jlt","jgt","+jgt","tix","+tix","tixr","+j","start","end","byte","word","resw",
                   "resb","equ","org","base"}

registers = {"a","b","s","t","x","l"}
ropcodes = {"rmo","tixr","addr","subr","comr"}
