import numpy as np
from collections import defaultdict
import math
from nltk.classify import MaxentClassifier
class ME(object):

    def __init__(self):
        self.features=defaultdict(int)
        self.trainset=[]
        self.labels=set()

    def load_data(self,f):
        file=open(f)
        for line in file:
            fields=line.strip().split()
            if len(fields)<2:
                continue
            label=fields[0]
            self.labels.add(label)
            for feature in set(fields[1:]):
                self.features[(label,feature)]+=1
            self.trainset.append(fields)
        file.close()

    def initparams(self):
        self.size=len(self.trainset)
        self.M=max([len(record)-1 for record in self.trainset])
        self.ep_=[0.0]*len(self.features)
        for i, f in enumerate(self.features):
            self.ep_[i]=float(self.features[f])/self.size
            self.features[f]=i
        self.w=[0.0]*len(self.features)
        self.lastw=self.w



    def probwgt(self,feats,label):
        wgt=0.0
        for f in feats:
            # print(self.features[(label,f)])
            if (label,f) in self.features:
                wgt+=self.w[self.features[(label,f)]]
        return math.exp(wgt)

    def calprob(self, features):
        wgts = [(self.probwgt(features, l), l) for l in self.labels]
        Z = sum([w for w, l in wgts])
        prob = [(w / Z, l) for w, l in wgts]
        return prob

    def featureExp(self):
        res=[0.0]*len(self.features)
        for i in self.trainset:
            features=i[1:]
            prob=self.calprob(features)
            for f in features:
                for w,l in prob:
                    if (l,f) in self.features:
                        j=self.features[(l,f)]
                        res[j] += w*(1.0/self.size)
        return res

    def convergence(self,lastw,w):
        for w1,w2 in zip(lastw,w):
            if(abs(w1-w2)>=0.01):
                return False
        return True

    def train(self,max_itera=10000):
        self.initparams()
        for i in range(max_itera):
            # print('第%d次迭代'%(i+1))
            self.ep=self.featureExp()
            self.lastw=self.w[:]
            for i,w in enumerate(self.w):
                delta=1.0/self.M*math.log(self.ep_[i]/self.ep[i])
                self.w[i]+=delta
            if self.convergence(self.lastw,self.w):
                break

    def prediction(self,data):
        features=data.strip().split()
        prob=self.calprob(features)
        prob.sort(reverse=True)

        return prob
if __name__=="__main__":
    maxent=ME()
    maxent.load_data("input.txt")
    maxent.train(100)
    prob=maxent.prediction("Sunny Sad")
    print(prob)






