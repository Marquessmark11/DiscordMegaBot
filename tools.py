class tools:
    def __init__(self):
        pass
    def strl(self, a:list):
        h = ""
        for g in a:
            h+=g
        return h
    def addChar(self, char:str, adder:list, referencer:list):
        for x in range(len(referencer)):
            if referencer[x] == char:
                adder[x] = char
        return adder
    def strd(self, a:list):
        h = ""
        for g in a:
            h+=(str(g)+'\n')
        return h
helper = tools()
