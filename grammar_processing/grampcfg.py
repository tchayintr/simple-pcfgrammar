import time

# rdir = "/Users/AdminZ/Desktop/tree-pdf/Fairytales/sorted_CFG-v2-cut.txt"
# rdir = "/Users/AdminZ/Desktop/workspace/datasets/fairytales/grammar/fairytale_grammar.txt"
# rdir = "/Users/AdminZ/Desktop/tree-pdf/Fairytales/sorted_CFG-v1.txt"

LEFTDIV_SEP = '-->'
RIGHTDIV_SEP = ','
FREQ = 'frequency'
RULE_FREQ = 'rule_frequency'      #
PROBABILITY = 'probability'

class PCFG:
    def __init__(self, grammars):
        # Variables
        self.rules = {}
        self.stats = {}
        self.leftmost = []
        self.rightmost = []
        self.grammars = grammars

        # Functions
        self.distribute_proc()
        # delete each rule_frequency
        self.delby_key(RULE_FREQ)


    def distribute_proc(self):
        for grammar in self.grammars:
            self.calc(grammar)
        self.calc_prob()
        self.print_probability()

    def calc(self, grammar):
        if grammar not in self.stats:
            self.stats[grammar] = {FREQ: 0}
            self.stats[grammar][FREQ] = self.get_freq(self.grammars, grammar)
        self.calc_freq(grammar)

    def calc_freq(self, grammar):
        lhs, sep, rhs = (grammar.partition(LEFTDIV_SEP))
        self.leftmost.append(lhs)
        self.rightmost.append(rhs)

        if lhs not in self.rules:
            self.rules[lhs] = {RULE_FREQ: 0}
        if rhs not in self.rules[lhs]:
            self.rules[lhs][rhs] = {FREQ: 1, PROBABILITY: 0.0}
        else:
            self.rules[lhs][rhs][FREQ] += 1
        # Rule's frequency
        self.rules[lhs][RULE_FREQ] += 1

    def calc_prob(self):
        for lhs in self.rules:
            for rhs in self.rules[lhs]:
                if rhs not in RULE_FREQ:
                    self.rules[lhs][rhs][PROBABILITY] = self.rules[lhs][rhs][FREQ]/self.rules[lhs][RULE_FREQ]

    def get_freq(self, tokens, token):
        return freq(tokens, token)

    def print_probability(self):
        for lhs in self.rules:
            # print(lhs, LEFTDIV_SEP)
            for rhs in self.rules[lhs]:
                if rhs not in RULE_FREQ:
                    # print(rhs, "P: %.5f" % self.rules[lhs][rhs][PROBABILITY])
                    pass

    def sortby_prob(self):
        pass

    def sortby_freq(self):
        pass

    def delby_key(self, key):
        for rule in self.rules:
            # This will return dict[key] if key exists in the dictionary, and None otherwise.
            self.rules[rule].pop(RULE_FREQ, None)

    def get_result(self):
        return self.rules



def freq(tokens, token):
    return tokens.count(token)

# Format: S-->NP,VP.
def read_grammar(rdir):
    with open(rdir, 'r', encoding= 'utf-8') as rfd:
        return rfd.read().splitlines()

def writefile(wdir, data):
    with open(wdir, 'w', encoding= 'utf-8') as wfd:
        for datum in data:
            wfd.write(datum)

def printresult(data):
    # print(result_dict)
    for lhs in result_dict:
        sorted_dict = sorted(result_dict[lhs].items(), key=lambda x: x[1][PROBABILITY], reverse=True)
        for item in sorted_dict:
            rhs = item[0]
            prob = item[1][PROBABILITY]
            freq = item[1][FREQ]
            print("{}{}{} | Prob:{:.5f}, Freq:{}".format(lhs, LEFTDIV_SEP, rhs, prob, freq))

#===========================================================
if __name__ == "__main__":
    #-----------------------
    s_time = time.time()

    result_dict = {}
    grammars = read_grammar(rdir)
    parser = PCFG(grammars)
    result_dict = parser.get_result()

    printresult(result_dict)

    #-----------------------
    e_time = time.time()
    timer = e_time - s_time
    print("Processed in {} second(s)".format(timer))