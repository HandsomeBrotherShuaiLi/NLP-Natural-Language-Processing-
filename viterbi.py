from collections import defaultdict

class viterbi(object):
    def __init__(self,train_path,test_path):
        self.states=defaultdict(int)#词性统计
        self.words=defaultdict(int)#单词统计
        self.transition_probability=defaultdict(float)#转移概率
        self.output_probability={}#输出概率
        self.data = open(train_path,'r').read()
        self.data=self.data.strip('\t').strip('\n')
        self.test=open(test_path,'r',encoding='UTF-8').readlines()

        self.output=None
        self.dictionary={}
    def process_trainset(self):
        dict=self.data.split( )
        for x in dict:
            i=x.find('/')
            self.states[x[i + 1:]] += 1
            self.words[(x[0:i],x[i+1:])] += 1

        #p(x/y)=x出现在y之后的次数/y的次数
        maxlen=len(dict)
        for i in range(maxlen-1):
            index=dict[i+1].find('/')
            x=dict[i+1][index+1:]
            index=dict[i].find('/')
            y=dict[i][index+1:]
            self.transition_probability[(x,y)]+=1.0/self.states[y]

        for (x,y) in self.words.keys():#x-单词 y-词性
           self.output_probability[(x,y)]=self.words[(x,y)]/self.states[y]
    def main(self):
        self.process_trainset()
        import jieba
        for line in self.test:
            wordlist=jieba.cut(line,cut_all=False)




if __name__=='__main__':
    m=viterbi(train_path='training.txt',test_path='input.txt')
    m.main()
