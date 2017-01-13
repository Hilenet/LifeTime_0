import os
import glob
import pickle
import random
from janome.tokenizer import Tokenizer

""" Generator gens sentence
        from a word
        with internal model
"""

#####

class Generator:
    """integrate gen sentence"""
    def __init__(self):
        # load/create model instance
        path = os.path.dirname(__file__)+'/../dat/model'
        if glob.glob(path):
            self.model = pickle.load(open(path, 'rb'))
            print('model has load')
        else:
            self.model = Model()
            print("model has made")

    def gen(self, word):
        # generate sentence start with arg
        tokens = self.model.first(word)
        
        while tokens[-1] not in ["。", "？", "！", "ー"]:
            tmp = self.model.iterate(tokens[-2], tokens[-1])
            if tmp == []:
                print("can't gen sentence from: ", tokens)
                tokens += self.model.last(tokens[-1])
                break
            tokens += tmp[-1]
        
        return "".join(tokens)


######

class Model:
    """ dump at dat/model
            list: [[tri-gram], [tri-gram]]
    """

    def __init__(self):
        # should use collection?
        self.list = []
        t = Tokenizer()
        self._generate_()
    
    def first(self, word):
        # first token: from a word
        tokens = list(filter(lambda tri: tri[0] == word, self.list))

        if tokens == []: return tokens
        return random.choice(tokens)
   
    def iterate(self, w1, w2):
        tokens = list(filter(lambda tri: (tri[0]==w1 and tri[1]==w2), self.list))

        if tokens == []: return tokens
        return random.choice(tokens)

    def last(self, word):
        tokens = list(filter(lambda tri: (tri[0]==word and tri[2]=="。"), self.list))

        if tokens == []: return "。"
        return "".join(tokens[0][1:3])

    def _generate_(self):
        t = Tokenizer() 
        for file in glob.glob(os.path.dirname(__file__)+'/../text/*'):
            for line in open(file, 'r'):
                self.list += self._parse_(line, t)
            print("proc: ", file)
        # must: sort with overlap num
        self.list.sort()
        with open(os.path.dirname(__file__)+'/../dat/model', 'wb') as f:
            pickle.dump(self, f)

    def _parse_(self, line, t):
        # separate
        tokens = list(map(lambda t: t.surface, t.tokenize(line)))
        buf = []

        if len(tokens) < 3: return buf
        
        # make tri-gram data
        for index in range(0, len(tokens)-2):
            buf += [tokens[index:index+3]]
            
        return buf
