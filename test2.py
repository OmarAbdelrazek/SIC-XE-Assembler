def Combine( b1,  b2):

     combined = b1 << 8 | b2
     return combined

x = 0b00010100
y = 0b11000110
print(hex(x))
print(hex(y))
print(hex(Combine(x,y)))