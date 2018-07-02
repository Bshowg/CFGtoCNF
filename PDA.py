import copy

class Rule:
    def __init__(self , variable , productions):
        self.variable   = variable
        self.productions = [productions]

def read_exp():  #Expression is read from 'expression.cfg' into list exp in reverse order, removing whitespace.
    i = 0
    global exp
    exp_file = open("expression.cfg", "rt")
    data = exp_file.read()
    chars = data.split(" ")
    for char in chars[::-1]:
        i = i + 1
        exp.append(char)
    return i

def divide_rules():  # split productions into the rules class by variable
    results = []
    rules_file = open("CNF.txt", "rt")
    data=rules_file.read()
    lines= data.split("\n")
    for line in lines[:-1]:
        line= line.split(" -> ")

        right=line[0]
        left=line[1][:-1].split(" | ")

        for l in left:
            l=' '.join(l)
            rules_input.append(right+" -> "+l)
    print rules_input
    for rule in rules_input:
        found = False
        var = rule.split(" -> ")
        for result in results:
            if result.variable == var[0]:
                result.productions.append(var[1])
                found = True
        if not found:
            results.append(Rule(var[0] , var[1]))
    for result in results:
        print result.variable
        for r in result.productions:
            print r
        print "-----"
    return results

def print_reject():  #Prints Reject and exits program.
    print("\n\n")
    print("************************************")
    print("*             REJECT               *")
    print("************************************")
    exit()

def get_rule(symbol):
    global rules
    for rule in rules:
        if rule.variable == symbol:
            return rule
    return False

def operation(stack, exp):  #Performs the operations of a PDA.  Recursive.
    if len(stack) > len(exp) or (len(stack) == 0 and len(exp) > 0):
        return
    current_symbol = stack.pop()
    if current_symbol == exp[-1]:
        exp.pop()
        test(stack , exp)
        operation(copy.deepcopy(stack) , copy.deepcopy(exp))
    rule = get_rule(current_symbol)
    if rule == False:
        return
    print rule.productions
    for production in rule.productions:
        new_stack = copy.deepcopy(stack)
        for s in production.split(" ")[::-1]:
            new_stack.append(s)
        operation(new_stack, copy.deepcopy(exp))

def test(stack, exp):
    if len(stack) == 0 and len(exp) == 0:
        print("\n\n")
        print("************************************")
        print("*             ACCEPT               *")
        print("************************************")
        exit()
    else:
        return False

def main():
    global length
    global rules
    global var_test

    global exp
    print("Expression:")
    read_exp()
    print(exp)
    rules = divide_rules()
    for rule in rules:
        var_test.append(rule.variable)
    print "variables =", var_test
    stack = []
    stack.append("S")
    print stack
    operation(stack, exp)
    print_reject()

exp = []
var_test = []
rules_input = []
stack = []
var = []
final= []
main()