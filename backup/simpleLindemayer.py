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

if __name__=='__main__':
    import sys
    temp = Lindenmayer('A',{'A':'B-A-B','B':'A+B+A'})
    for i in range(3):
        t= temp.next()
    print t
    t = t.replace('X','')
    t = t.replace('Y','')
    print t
