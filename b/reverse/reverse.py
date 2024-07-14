from z3 import * 

s = Solver()

# From the analysis length of the string is 30 
len = 29 # One is for end character \0
str = []
for i in range(len):
    str.append(BitVec(f"str-{i}", 8))

# Size of value is 4 bytes and intial value is 0
val = BitVecVal(0, 32)

newline_char = BitVecVal(10, 32)
newline = Bool('newline')
s.add(newline == False)

# Adding logic found from the analysis
for i in range(len):
    # Adding constraints for the string by ASCII values
    s.add(Or( str[i] == 10,And(str[i] >= 32, str[i] <= 126)))

    # Extending the character of string to 32 bits because the value is 32 bits
    str_32 = ZeroExt(24, str[i]) 
    i_32 = BitVecVal(i, 32)

    newline = Or(newline, str_32 == newline_char)
    val = If(newline, val, val + ((str_32 * str_32) + (str_32 * (100 - i_32)) + i_32 + (str_32 * 7) + ((str_32|i_32)&(i_32+3))) -  ((str_32 * str_32) % (i_32 + 1 )))

# Adding constraint for the hardcoded value
s.add(val == 315525)

if s.check() == sat:
    solution = s.model()
    string = ""
    for i in range(len):
        if (solution[str[i]].as_long() == 10):
            break
        string += chr(solution[str[i]].as_long())
    print(string)
else:
    print("No solution found")

