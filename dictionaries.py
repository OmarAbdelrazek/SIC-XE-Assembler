address = {}
label = {}
opcode = {}
operand = {}
comment = {}
errors = {}
objectCodeList = {}
lineCounter = 0
errorFound = 0
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
      'LDX': 3, 'STX': 3,'+LDX': 4, '+STX': 4,'LDT': 3, 'STT': 3,'+LDT': 4, '+STT': 4,'RESW':0 ,'EQU':0 ,'RESB':0 ,'ORG':0 ,
      'WORD':0 ,'BYTE':0}

notFormat4 = {"+rmo","+subr","+comr","+tixr"}

format4Only = {"+LDCH","+STCH","+ADD","+SUB","+COMP","+J","+JEQ","+JLT","+JGT","+TIX","+LDA","+STA",
               "+LDA","+STA","+LDL","+STL","+LDS","+STS","+LDT","+STT","+LDX","+STX","+LDB","+STB"}

directives = {"START","END","BYTE","WORD","RESW","RESB","EQU","ORG","BASE"}

instructionDict = {"rmo","lda","+lda","sta","+sta",
                   "ldb","+ldb","stb","+stb","ldx","+ldx","stx","+stx","lds","+lds","sts","+sts",
                   "ldl","+ldl","stl","+stl","ldt","+ldt","stt","+stt",
                   "ldch","+ldch","stch","+stch","add","+add",
                   "sub","+sub","addr","subr","comp","+comp","compr","j",
                   "jeq","+jeq","jlt","+jlt","jgt","+jgt","tix","+tix","tixr","+j","start","end","byte","word","resw",
                   "resb","equ","org","base"}

registers = {"a","b","s","t","x","l"}
ropcodes = {"rmo","tixr","addr","subr","compr"}

obTable = {"ADD"  :"00011000" ,"ADDR"  :"10010000","COMP" :"00101000","COMPR" :"10100000","J":"00111100","JEQ" : "00110000","JGT"  :"00110100",
"JLT" :"00111000","LDA"  :"00000000" ,"LDB" :"01101000","LDCH" :"01010000", "LDL"  :"00001000","LDS"  :"01101100","LDT"  :"01110100"
,"LDX"  :"00000100","RMO"  :"10101100","STA"  :"00001100","STB" :"01111000","STCH" :"01010100","STL"  :"00010100","STS" :"01111100","STT":"10000100","STX"  :"00010000",
"SUB" :"00011100","SUBR"  :"10010100","TIX" :"00101100","TIXR"  :"10111000",
"+ADD"  :"00011000" ,"+COMP" :"00101000","+J":"00111100","+JEQ" : "00110000","+JGT"  :"00110100","+JLT" :"00111000",
"+LDA"  :"00000000" ,"+LDB" :"01101000","+LDCH" :"01010000", "+LDL"  :"00001000","+LDS"  :"01101100","+LDT"  :"01110100"
,"+LDX"  :"00000100","+STA"  :"00001100","+STB" :"01111000","+STCH" :"01010100","+STL"  :"00010100","+STS" :"01111100",
"+STT":"10000100","+STX"  :"00010000","+SUB" :"00011100","+TIX" :"00101100","TIXR"  :"10111000"}


registersOpcode = {'A': '0000', 'X': '0001', 'I': '0010', 'B': '0011', 'S': '0100', 'T': '0101', 'F': '0110'}

flagsBits = {'directformat3': '110000', 'directformat4': '110001', 'directindexed12': '111000',
                   'directindexed20': '111001',
                   'simplesicinstruction': '000', 'address+indexvalue': '001', 'indirectformat3': '10000',
                   'indirectformat4': '100001'
    , 'immediateformat3': '010000', 'immediateformat4': '010001'}

binToHex={"0000":"0","0001":"1","0010":"2","0011":"3","0100":"4","0101":"5","0110":"6","0111":"7","1000":"8",
          "1010":"A","1011":"B","1100":"C","1101":"D","1110":"E","1111":"F","1001":"9"}


obTableHex = {"ADD"  :0x18 ,"ADDR"  :0x90,"COMP" :0x28,"COMPR" :0xA0,"J":0x3C,"JEQ" : 0x30,"JGT"  :0x34,
"JLT" :0x38,"LDA"  :0x00 ,"LDCH" :0x50, "LDL"  :0x08,"LDS"  :0x6C,"LDT"  :0x74
,"LDX"  :0x04,"RMO"  :0xAC,"STA"  :0x0C,"STB" :0x78,"STCH" :0x54,"STL"  :0x14,"STS" :0x7C,"STT":0x84,"STX"  :0x10,
"SUB" :0x1C,"SUBR"  :0x94,"TIX" :0x2C,"TIXR"  :0x88,"LDB"  :0x68}
registersOpcodeHex = {'A': '0', 'X': '1', 'I': '2', 'B': '3', 'S': '4', 'T': '5', 'F': '6'}