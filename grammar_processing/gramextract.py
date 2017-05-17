#! /usr/bin/env python3
import sys, getopt

PAIR_LIST = []      # Keeping POS/TERM
RULE = []           # Keeping all processed rule
MAXLEVEL = 0
LEVEL = 0
GRAM = 1

r_dir = None
w_dir = "./output/gram.txt"
dict_wdir = "./output/dict.txt"

class Parser:
    def __init__(self, data):
        self.data = data
        self.stack = []
        self.pos = 0
        self.level = 0

    def parse(self):
        rule = []
        BEGIN_FLAG = False
        CLOSED_TERM = False
        global MAXLEVEL
        for index, cur_char in enumerate(self.data):
            if cur_char == '[':
                if BEGIN_FLAG == True:
                    gram = ''.join(self.stack)
                    if isNotEmpty(gram):
                        content = (self.level, gram)
                        rule.append(content)
                elif BEGIN_FLAG == False: BEGIN_FLAG = True

                if self.stack:
                    self.stack[:] = []
                self.level+=1
                if self.level > MAXLEVEL: MAXLEVEL = self.level

            elif cur_char == ']':
                if self.level == MAXLEVEL:
                    term_gram = ''.join(self.stack)
                    extract_term(term_gram)
                    content = (self.level, term_gram)
                    rule.append(content)
                    CLOSED_TERM = True
                else:
                    term_gram = ''.join(self.stack)
                    if isNotEmpty(term_gram):
                        extract_term(term_gram)
                        content = (self.level, term_gram)
                        rule.append(content)
                self.stack[:] = []
                self.level-=1
            else:
                self.stack.append(cur_char)
        self.stack[:] = []
        return rule

def readfile(rdir):
    with open(rdir, 'r', encoding='utf-8') as rfd:
        return rfd.read().splitlines()

def writefile(wdir, data):
    with open(wdir, 'w', encoding='utf-8') as wfd:
        for datum in data:
            wfd.write(datum + '\n')

def extract_term(string):
    TERM_SEP = ' '
    pos, sep, term = string.partition(TERM_SEP)
    PAIR_LIST.append(pos+'/'+term)

def isNotEmpty(s):
    return bool(s and s.strip())

def conduct_gram(data, depth=1):
    global MAXLEVEL
    stack = []
    data_size = len(data)
    itr = 0
    ROOT = True

    while itr < data_size:
        tmp_stack = []
        prev_level = 0
        depth_pointer = -1

        for datum in data:
            if datum[LEVEL] < prev_level and ROOT is False:
                break
            elif datum[LEVEL] > prev_level:
                if depth_pointer < depth:
                    tmp_stack.append((datum[LEVEL] ,datum[GRAM].split(' ')[0]))        # remove text in a terminal grammar
                    depth_pointer+=1
                    prev_level = datum[LEVEL]
            else:
                tmp_stack.append((datum[LEVEL] ,datum[GRAM].split(' ')[0]))
                depth_pointer += 1


        if tmp_stack: stack.append(tmp_stack)
        if data: data.pop(0)
        itr+=1
        ROOT = False
    format_gram(stack)

def format_gram(data):
    for datum in data:
        if len(datum) > 1 and not all_same_level(datum):
            lhs = datum.pop(0)[GRAM]
            datum = [gram[1:][0] for gram in datum]     # remove 1st element in every tuple
            cfg = (lhs + '-->' + ','.join(datum) + '.')
            # print(cfg)
            RULE.append(cfg)

# Returning True They are same otherwise false
def all_same_level(items):
    return all(x[0] == items[0][LEVEL] for x in items)


def main(argv):
    global r_dir, w_dir, dict_wdir, RULE, PAIR_LIST
    dict = False
    unique = False

    try:
        opts, args = getopt.getopt(argv, "i:o::du", ["ifile=", "ofile=", "dict", "unique"])
    except getopt.GetoptError:
        print('gramextract.py -i <inputfile> -o <outputfile> -d <outputdict?> -u <unique sorting?>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('gramextract.py -i <inputfile> -o <outputfile> -d <outputdict?> -u <unique sorting?>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            r_dir = arg
        elif opt in ("-o", "--ofile"):
            w_dir = arg
        elif opt in ("-d", "--dict"):
            dict = True
        elif opt in ("-u", "--unique"):
            unique = True
        else:
            print('gramextract.py -i <inputfile> -o <outputfile> -d <outputdict?> -u <unique sorting?>')

    if r_dir:
        lbrackets = readfile(r_dir)
        for lb in lbrackets:
            parser = Parser(lb)
            raw_rule = parser.parse()
            conduct_gram(raw_rule)
        if unique is True:
            RULE = sorted(set(RULE))
            PAIR_LIST = sorted(set(PAIR_LIST))
        writefile(w_dir, RULE)
        if dict is True: writefile(dict_wdir, PAIR_LIST)

        print("Extracted: {} grammar(s), {} word(s), Dict={}, Unique={}".format(len(RULE), len(PAIR_LIST), dict, unique))

    else:
        print('gramextract.py -i <inputfile> -o <outputfile> -d <outputdict?> -u <unique sorting?>')

if __name__ == '__main__':
    main(sys.argv[1:])