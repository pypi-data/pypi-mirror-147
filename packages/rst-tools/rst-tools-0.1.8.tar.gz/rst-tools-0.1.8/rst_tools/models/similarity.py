from pandas import DataFrame

from models.roughsets import RoughSets

class SimilarityRoughSets(RoughSets):

    ''' Creating new instance of Similarity Rough Sets with Dataset (df) and alpha '''
    def __init__(self, df, alpha, attr_type="discrete"):
        super().__init__(df)
        self.alpha = alpha 

    ''' Calculate similarity of two objects o1, and o2 respect to attributes'''
    def similarity(self, o1, o2, attributes):
        sim = [o1[attr] == o2[attr] for attr in attributes].count(True)
        return sim/len(attributes)

    ''' Generate partition subject to attributes'''
    def ind(self, attributes):
        ud = dict()
        R = dict()
        for k, o1 in self.dataset.iterrows():
            ud[k] = list()
            R[k] = dict()
            for k2, o2 in self.dataset.iterrows():
                # print(o2)
                # pass
                if self.similarity(o1, o2, attributes) >= self.alpha:
                    ud[k].append(k2)
                    R[k][k2] = True 
                else :
                    R[k][k2] = False
        
        ud1 = dict() 
        for k, o1 in self.dataset.iterrows():
            for k2, o2 in self.dataset.iterrows():
                if k2 not in ud1:
                    ud1[k2] = list() 
                if R[k2][k] is True:
                    ud1[k2].append(k)

        
        return ud, ud1
    
    '''Generate partition of U subject to decision attribute d'''
    def subsetU(self, decision):
        dfX = DataFrame()
        dfX[decision] = self.dataset[decision]

        X = dict() 

        for index, row in dfX.iterrows():
            if row[decision] in X: 
                l = X[row[decision]]
                l.append(index)
            else: 
                X[row[decision]] = [index]

        return X

    ''' Generate lower and upper approximation'''
    def approximation(self, attributes, decision):
        ind, ind1 = self.ind(attributes)
        lower = dict()
        upper = dict()
        for d, X in self.subsetU(decision).items():
            lower[d] = list()
            upper[d] = list()
            X_set = set(X)
            l = set()
            u = set()
            for o, g in ind.items():
                o_set = set(g)
                if o_set <= X_set:
                    l.update(o_set) 
                
                if len(o_set.intersection(X_set)) > 0:
                    u.update(o_set)

            lower[d] += list(l)
            upper[d] += list(u)

        return lower, upper

    ''' Calculate vagueness of the class '''
    def alph(self, attributes, decision):
        a = dict() 
        lower, upper = self.approximation(attributes, decision)
        for ky, v in lower.items():
            a[ky] = len(v)/len(upper[ky])

        return a

    ''' Calculate the dependency attribute D subject to the C'''
    def gamma(self, attributes, decision):
        k = 0
        lower, upper = self.approximation(attributes, decision)
        
        objects = list()
        for ky, v in lower.items():
            objects += v

        return len(objects)/len(self.dataset);
        


