s = "#test"
a = "#100"
def isString(s):
    i = len(s)-1
    print(s[i])
    while i:
        if (s[i] >= "a" and s[i] <= "z") or (s[i] >= "A" and s[i] <= "Z"):
            return "true"
        i -= 1
    return "false"


print(isString(a[1:]))


