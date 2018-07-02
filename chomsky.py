# coding=utf-8
# coding=utf-8
# Name:        CFG to NCF
# Purpose:     This script transforms a context-free grammar to Normal-Chomsky
# form with order of operation START,TERM,BIN,DEL,UNIT,END
#
# A → BC
# A → a
# S → ε
#
#
# Author:      Gianmarco Biscini
#
# Created:     10/06/2018
# -------------------------------------------------------------------------------

from string import letters
import copy
import re
import string


def START(rules, starting_symbol):
    rules.setdefault('S0', []).append(starting_symbol)
def END(rules,starting_symbol):
    del rules['S0']

    return rules

def TERM(rules, vars, epsilon):    #leva le regole nella forma A ->Bc
    old_rules = {}
    for key, value in rules.iteritems():
        temp = []
        for rule in value:

            if len(rule) > 1:
                temp.append(checkTerminal(old_rules, rule, vars, epsilon)) #itera ricorsivamente su ogni regola
            else:
                temp.append(rule)

        rules.pop(key) #elimina
        #print value
        print temp
        #print old_rules
        for i in range(0, len(temp)): #riaggiungi pulita
            rules.setdefault(key, []).append(temp[i])

    for key, value in old_rules.iteritems():
        for rule in value:
            rules.setdefault(key, []).append(rule)
    return old_rules


def checkTerminal(old_rules, rule, vars, epsilon):
    for letter in rule:
        if letter.islower() and letter != epsilon:
            if letter not in old_rules.values(): #prendi nuova variabile
                l = vars.pop()
                old_rules[l] = letter

            else:
                l = old_rules.keys()[old_rules.values().index(letter)]

            # temp_rules.setdefault(l, []).append(letter)
            rule = checkTerminal(old_rules, rule.replace(letter, l), vars, epsilon)

            return rule

    return rule


def BIN(rules, vars): #leva le regole nella forma A -> BCD...
    temp = {}
    for key, value in rules.iteritems():
        for rule in value:
            if len(rule) > 2:
                new_key = ""

                for j in range(0, len(rule) - 2):
                    # that the first and add a new variable
                    if j == 0:
                        lett = vars.pop()
                        temp.setdefault(key, []).append(rule[0] + lett)
                    #from the second just that the one bofore and add the next var in the rule
                    else:
                        lett = vars.pop()
                        temp.setdefault(new_key, []).append(rule[j] + lett)
                    new_key = lett
                # take the last new variable and add the last part of the rule
                temp.setdefault(new_key, []).append(rule[-2:])
            else:
                temp.setdefault(key, []).append(rule)
        if len(rule) > 2:
            del rule
    # print temp
    rules.update(temp)

    return rules


def DEL(rules, vars, epsilon,starting_simbol):  # rimuove epsilon transition
    epsilon_rules = []

    iter_rule = copy.deepcopy(rules)

    for key, value in iter_rule.iteritems(): #prendi quelle A->e
        if key != starting_simbol:
            for rule in value:
                    # if key gives an empty state and is not in list, add it
                    if rule == epsilon and key not in epsilon_rules and len(rule)==1:
                        epsilon_rules.append(key)
                        # remove empty state
                        rules.get(key).remove(rule)

                    if len(rules[key])==0:
                        del rules[key]
    for key, value in rules.iteritems(): #controlla non ce ne siano altre nullabili
        if key != starting_simbol:
            for rule in value:
                    for i in range(0, len(rule)):
                        if rule[i] not in epsilon_rules:
                            break
                        if i==len(rule)-1 and rule[i] in epsilon_rules and key not in epsilon_rules:

                            epsilon_rules.append(key)
                            DEL(rules,vars,epsilon,starting_simbol)
                            print rule

    print epsilon_rules

    for key, value in iter_rule.iteritems(): #
        for rule in value:
            #combination=[]
            for i in range(0, len(rule)):
                if rule[i] in epsilon_rules:
                    #combination.append(rule[i])
                    new_rule=rule.replace(rule[i],"",1)
                    if new_rule!="" and key!=new_rule:
                        rules.setdefault(key,[]).append(new_rule)

    return rules


def UNIT(rules): #rimuovi le singole
    toDelete = {}
    for key, value in rules.iteritems():
        for rule in value:
            if len(rule) == 1 and rule.isupper():

                merge = rule
                print merge + " "+ str(rules[merge])

                if merge in rules.keys():
                    if merge!=key:
                        add_rule(rules, key, rules[merge])
                        rules.get(key).remove(merge)
                        UNIT(rules)
                    if merge not in toDelete:
                        toDelete.setdefault(key,[]).append(merge)
    #print toDelete
    for key,value in toDelete.iteritems():
        for rule in value:
            if rule in rules.get(key):
                rules.get(key).remove(rule)
    return rules


def add_rule(rules, key, new_rules):
    #print len(new_rules)
    for rule in new_rules:
        rules.setdefault(key, []).append(rule)

    return rules
def Write(rules):
    file = open("CNF.txt","w")
    line=""
    for key, value in rules.iteritems():
        line=key + " -> "
        for rule in value:

            line+=rule+" | "
        line= line[:len(line)-2]
        file.write(line)
        file.write("\n")
    file.close()
def Read(filename):
    rules={}
    with open(filename) as file:
        lines = [line.strip() for line in file if "#" not in line]
        for line in lines:
            key, values=line.split("->")
            key.replace(" ","")
            values=values.split(" ")
            for rule in values:
                if rule!="":
                    rules.setdefault(key,[]).append(rule)
    return rules
def initSymbols(P):
    vars=[]
    voc=[]
    available=[x for x in string.ascii_uppercase]
    for key, value in P.iteritems():
        if key.isupper():             #aggiungi chiavi a lista variabili e vocabolario
            if key not in vars:
                vars.append(key)
        elif key.isupper():
            if key not in voc:
                voc.append(key)

        for rule in value:
            for i in range(0, len(rule)):
                if rule[i].isupper():           #aggiungi right-side
                    if rule[i] not in vars:
                        vars.append(rule[i])
                elif rule[i].isupper():
                    if rule[i] not in voc:
                        voc.append(rule[i])
    for c in vars:
        available.remove(c)
    return vars,voc,available
def preCheck(V,P):
    if 'S' not in V:
        print '--------------------------------ERROR----------------------------------'
        print "| No starting symbol. Make another grammar with S as the starting symbol"
        print '--------------------------------ERROR----------------------------------'
        return 1

    else:
        return 0

def main():
    P = {}
    V = []
    A = []
    epsilon = 'e'
    VARS = []
    start_sym = 'S'

    P=Read("G.txt")  #P=Read(sys.argv[1]
    V,A,VARS=initSymbols(P)
    #print P
    if preCheck(V,P)!=0:
        return 'error'

    START(P, start_sym)
    old_rules = TERM(P, VARS, epsilon)
    #print P
    P = BIN(P, VARS)
    #print P
    P=DEL(P, VARS, epsilon,start_sym)
    print P
    P=UNIT(P)
    P=UNIT(P)

    #print P
    P=END(P,start_sym)
    Write(P)

if __name__ == '__main__':
    main()