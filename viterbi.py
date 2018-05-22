from collections import defaultdict
import os
from zhon.hanzi import punctuation

ROOT = 'train'
class viterbi(object):
    def __init__(self,test_path):
        self.states=defaultdict(int)#词性统计
        self.words=defaultdict(int)#单词统计
        self.wordset=set()
        self.wordcount=defaultdict(int)
        self.transition_probability=defaultdict(float)#转移概率
        self.output_probability={}#输出概率
        self.pi={}
        self.data = open('training.txt','r').readlines()

        #1-5用做训练，6用作验证
        for i in range(1,6):
            f=os.path.join(ROOT,'TrainningText%d.TXT'%(i))
            # print(f)
            p=open(f,'r',encoding='utf-8').readlines()
            for line in p:
                self.data.append(line)


        self.test=open(test_path,'r',encoding='UTF-8').readlines()

        self.output=None
        self.dictionary=[]
    def process_trainset(self):
        statesnum=0
        for line in self.data:
            line=line.strip().strip('\n').strip('\t')
            dict=line.split( )

            for x in dict:
                i = x.find('/')
                self.dictionary.append(x)
                statesnum+=1
                self.states[x[i + 1:]] += 1
                self.words[(x[0:i], x[i + 1:])] += 1
                self.wordset.add(x[0:i])
                self.wordcount[x[0:i]]+=1
                # print(x[i+1:],x[0:i])
        for x in self.states:
            self.pi[x] = self.states[x] /statesnum
        # p(x/y)=x出现在y之后的次数/y的次数
        maxlen = statesnum
        for i in range(maxlen - 1):
            index = self.dictionary[i + 1].find('/')
            x = self.dictionary[i + 1][index + 1:]
            index = self.dictionary[i].find('/')
            y = self.dictionary[i][index + 1:]
            self.transition_probability[(x, y)] += 1.0 / self.states[y]

        for x in self.wordset:
            for y in self.states.keys():
                if (x, y) in self.words.keys():
                    self.output_probability[(x, y)] = self.words[(x, y)] / self.states[y]
                else:
                    self.output_probability[(x, y)] = 0.0

    def print_result(self):
        self.process_trainset()

        import jieba.posseg as pg

        for line in self.test:
            wordlist=[word for (word,flag) in pg.cut(line.strip('\n').strip('\t').strip('\ufeff'))]

            flags=[flag for (word,flag) in pg.cut(line.strip('\n').strip('\t').strip('\ufeff')) ]
            # wordlist=line.split( )
            wl=len(wordlist)
            ws=len(self.states)
            states=[]
            for st in self.states.keys():
                states.append(st)
            states.append('ul')
            # print(wordlist)
            # print(states)
            # for i in self.wordset:
            #     print(i)


            dp=[[0.000000 for i in range(ws+2)] for i in range(wl+2)]
            position = [['0' for i in range(ws + 2)] for i in range(wl + 2)]
            # print(len(dp[0]))
            #对于dp[1][i]而言 i 0-n-1
            for i in range(len(states)):
                if (wordlist[0],states[i]) in self.output_probability:
                    dp[1][i] = self.pi[states[i]] * self.output_probability[(wordlist[0], states[i])]
                    position[1][i]='0'
                else:
                    dp[1][i] = 0
                    position[1][i] = '0'
                    if states[i]==flags[0]:
                        dp[1][i]=1

            for i in range(2,len(wordlist)+1):
                for j in range(len(states)):
                    flag=states[0]
                    max=dp[i-1][0]*self.transition_probability[(states[j],states[0])]
                    for w in range(len(states)):
                        if dp[i-1][w]*self.transition_probability[(states[j],states[w])]>max:
                            max=dp[i-1][w]*self.transition_probability[(states[j],states[w])]
                            flag=states[w]
                    if (wordlist[i-1],states[j]) in self.output_probability.keys():
                        dp[i][j] = max * self.output_probability[(wordlist[i - 1], states[j])]
                        position[i][j] = flag
                    else:
                        dp[i][j] = max
                        ####i-2 i-1
                        position[i][j] = flag






            maxpro=0.0
            tn=states[0]
            for i in range(len(dp[0])):
                if dp[len(wordlist)][i]>maxpro:
                    maxpro=dp[len(wordlist)][i]
                    tn=position[len(wordlist)][i]
            t=[tn]*(len(wordlist)+1)
            n=len(wordlist)
            while(n>1):
                i=states.index(tn)
                t[n-1]=position[n][i]
                tn=t[n-1]
                n-=1
            # print(t)
            ans=str()
            for i in range(1,len(wordlist)+1):
                if wordlist[i-1] not in punctuation:
                    if wordlist[i-1] in self.wordset:
                        ans += wordlist[i - 1] + '/' + t[i] + ' '
                    else:
                        # print(wordlist[i-1],'不在')
                        ans+=wordlist[i-1]+'/'+flags[i-1]+' '


                else:
                    ans+=wordlist[i-1]+'/w'+' '


            print('自设计词性标注:',ans)
            ans2=str()
            for i in range(len(wordlist)):
                ans2+=wordlist[i]+'/'+flags[i]+' '
            print('jieba词性标注:',ans2)
            print('\n')
    def validation(self):
        import jieba.posseg as pg
        self.process_trainset()
        f=os.path.join(ROOT,'TrainningText6.TXT')
        fd=open(f,'r',encoding='utf-8').readlines()
        count = 0
        right = 0
        for line in fd:
            line=line.strip().strip('\t').strip('\n').strip('\ufeff')
            words=line.split( )
            val_states=[]
            wordlist=[]
            for x in words:
                i=x.find('/')
                wordlist.append(x[0:i])
                val_states.append(x[i+1:])
            line=''.join(wordlist)
            flags = [flag for (word, flag) in pg.cut(line.strip('\n').strip('\t').strip('\ufeff'))]
            # wordlist=line.split( )
            wl = len(wordlist)
            ws = len(self.states)
            states = []
            for st in self.states.keys():
                states.append(st)
            # states.append('ul')



            dp = [[0.000000 for i in range(ws + 2)] for i in range(wl + 2)]
            position = [['0' for i in range(ws + 2)] for i in range(wl + 2)]
            # print(len(dp[0]))
            # 对于dp[1][i]而言 i 0-n-1
            for i in range(len(states)):
                if (wordlist[0], states[i]) in self.output_probability:
                    dp[1][i] = self.pi[states[i]] * self.output_probability[(wordlist[0], states[i])]
                    position[1][i] = '0'
                else:
                    dp[1][i] = 0
                    position[1][i] = '0'
                    if states[i] == flags[0]:
                        dp[1][i] = 1

            for i in range(2, len(wordlist) + 1):
                for j in range(len(states)):
                    flag = states[0]
                    max = dp[i - 1][0] * self.transition_probability[(states[j], states[0])]
                    for w in range(len(states)):
                        if dp[i - 1][w] * self.transition_probability[(states[j], states[w])] > max:
                            max = dp[i - 1][w] * self.transition_probability[(states[j], states[w])]
                            flag = states[w]
                    if (wordlist[i - 1], states[j]) in self.output_probability.keys():
                        dp[i][j] = max * self.output_probability[(wordlist[i - 1], states[j])]
                        position[i][j] = flag
                    #未登录词的处理： 1.输出概率为1    2.极大似然估计
                    else:
                        #1.输出概率为1
                        # dp[i][j] = max
                        # ####i-2 i-1
                        # position[i][j] = flag

                        #2.极大似然估计
                        pro=0
                        for s in self.states.keys():
                            pro=1/self.states[s]
                            sum=0
                            for m in self.states.keys():
                                sum+=(self.words[(wordlist[i-2],m)]/self.wordcount[wordlist[i-2]])*self.transition_probability[(s,m)]
                            pro*=sum
                            self.output_probability[(wordlist[i-1],s)]=pro
                        dp[i][j]=max*self.output_probability[(wordlist[i-1],states[j])]
                        position[i][j] = flag


            maxpro = 0.0
            tn = states[0]
            for i in range(len(dp[0])):
                if dp[len(wordlist)][i] > maxpro:
                    maxpro = dp[len(wordlist)][i]
                    tn = position[len(wordlist)][i]
            t = [tn] * (len(wordlist) + 1)
            n = len(wordlist)
            while (n > 1):
                i = states.index(tn)
                t[n - 1] = position[n][i]
                tn = t[n - 1]
                n -= 1
            # print(t)
            test_states=[]
            for i in range(1, len(wordlist) + 1):
                count+=1
                if wordlist[i - 1] not in punctuation:
                    # test_states.append(t[i])
                    if wordlist[i - 1] in self.wordset:
                        test_states.append(t[i])
                    else:
                        # test_states.append('n')
                        # print(wordlist[i-1],'不在')
                        test_states.append(flags[i - 1])

                else:
                    test_states.append('w')
                if test_states[i-1]==val_states[i-1]:
                    right+=1
        print('accuracy：',right/count)#1.正确率：0.9546  #2.极大似然估计 0.9551

if __name__=='__main__':
    m=viterbi(test_path='input.txt')
    m.validation()
    m.print_result()














