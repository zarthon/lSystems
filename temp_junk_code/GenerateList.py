'''
rules: Dict of rules
axiom: Initial starting condition
'''

def Lindenmayer(axiom,rules):
    rules = rules.items()
    def apply_rule(axiom,(symbol,replacement)):
        
        print "axiom",axiom
        print "symbol",symbol
        print "replacement",replacement
        return axiom.replace(symbol,replacement.lower())

    while True:
        # Create a generator function
        yield axiom
        #get the next iteration of the system
        axiom = reduce(apply_rule,rules,axiom).upper()

class GenerateList(object):
    def __init__(self,generator):
        self.__generator = generator
        self.__list = []

    #to store the previous iterations
    def __getitem__(self,index):
        for i in range(index-len(self.__list) +1):
            self.__list.append(self.__generator.next())
        return self.__list[index]


