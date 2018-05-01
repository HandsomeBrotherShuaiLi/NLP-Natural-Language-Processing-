import string
from collections import defaultdict
from zhon.hanzi import punctuation
class self_seg(object):
    def __init__(self):
        self.inputdata=str()
        self.outputdata=str()
        #预先设置n=2,3,4,5,6
        self.ngram=defaultdict(int)
        self.sp=[]
        self.s=[]
        self.s_index=[]
        self.st=str()
        self.roman=["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        self.shuzi=['0','1','2','3','4','5','6','7','8','9']
        self.biaodian=[x for x in punctuation]


    def load_data(self,f):
        self.inputdata=open(f, 'r', encoding='UTF-8').read()
    def self_segmentation(self):
        #对S进行以罗马字符，标点，数字为断点切割,并且切后的字符串保留在self.s中

        res=self.inputdata
        slen=len(res)
        i=0
        j=0

        while(i<slen):
            if res[i] in self.biaodian or res[i] in self.roman or res[i] in self.shuzi or res[i]=='\n':
                self.s.append(res[j:i])
                self.s_index.append(j)
                j=i+1
                while(j<slen and (res[j] in self.biaodian or res[j] in self.roman or res[j] in self.shuzi or res[j]=='\n')):
                    j+=1
                self.sp.append(res[i:j])
                i=j
            else:
                i+=1
        self.s[0]=self.s[0][1:]
        # print('分割')
        # print(self.sp)
        for x in self.s:
            self.st+=x

        #n_gram 应该用dict 一遍扫过去的方法，否则用count的内置函数太耗时间
        stlen=len(self.st)
        i=0
        tmpngram=defaultdict(int)
        while(i<stlen-5):
            tmpngram[self.st[i:i+2]]+=1
            tmpngram[self.st[i:i+3]]+=1
            tmpngram[self.st[i:i+4]]+=1
            tmpngram[self.st[i:i+5]]+=1
            tmpngram[self.st[i:i+6]]+=1
            i+=1
        for x in tmpngram:
            if tmpngram[x]>=2:
                self.ngram[x]=tmpngram[x]

        replenish={}
        for i in range(len(self.s)):
            tmp=[]
            for ng in self.ngram:
                if ng in self.s[i]:
                    tmp.append(ng)
            tmpfinall=[]
            for x in tmp:
                if len(x)>= 3 and self.ngram[x]>=self.ngram[x[1:]] and self.ngram[x]>=self.ngram[x[0:-1]]:
                    tmpfinall.append(x)
                elif len(x)>= 3 and (self.ngram[x]<self.ngram[x[1:]] or self.ngram[x]<self.ngram[x[0:-1]]):
                    if self.ngram[x[1:]]>self.ngram[x[0:-1]]:
                        tmpfinall.append(x[1:])
                    elif self.ngram[x[1:]]<self.ngram[x[0:-1]]:
                        tmpfinall.append(x[0:-1])
                    else:
                        tmpfinall.append(x)
                        # tmpfinall.append(x[0:-1])
                    # tmpfinall.append(x[1:])
                    # tmpfinall.append(x[0:-1])
                #判断2 gram时候，要注意是否存在3 gram 包含 2 gram ，如果不包含，那么就加入备选，否则略过，交给3 gram 处理
                elif len(x)==2:
                    flag=1
                    for w in tmp:
                        if x in w and x!=w:
                            flag=0
                            break
                    if(flag==1):
                        tmpfinall.append(x)
                    else:
                        pass
            replenish[i]=tmpfinall
            #对s 进行切割
            substring=self.s[i]
            rem = []
            for u in tmpfinall:

                post=self.s[i].find(u)
                if post==-1:
                    pass
                else:
                    if post in rem:
                        pass
                    else:
                        self.s[i]= self.s[i][0:post] + '/' + self.s[i][post:]
                        rem.append(post)
            tmps=str()
            ind=0
            while(ind<len(self.s[i])):
                if self.s[i][ind]!='/':
                    tmps+=self.s[i][ind]
                    ind+=1
                else:
                    while(ind<len(self.s[i]) and self.s[i][ind]=='/'):
                        ind+=1
                    tmps+='/'
            self.s[i]=tmps+'/'
            # print(self.s[i])

        self.dictionary=[]
        #tmpdic 记录次数
        tmpdic=defaultdict(int)
        for j in range(len(self.s)):
            for e in replenish[j]:
                tmpdic[e]+=1
        for key in tmpdic:
            if tmpdic[key]>=2:
                self.dictionary.append(key)
        #分割
        # for i in range(len(self.s)):
        #     count=[]
        #     for u in self.dictionary:
        #         post=self.s[i].find(u)
        #         if post==-1:
        #             pass
        #         else:
        #             if post in count:
        #                 pass
        #             else:
        #                 self.s[i] = self.s[i][0:post] + '/' + self.s[i][post:]
        #                 count.append(post)
        #     tmps = str()
        #     ind = 0
        #     while (ind < len(self.s[i])):
        #         if self.s[i][ind] != '/':
        #             tmps += self.s[i][ind]
        #             ind += 1
        #         else:
        #             while (ind < len(self.s[i]) and self.s[i][ind] == '/'):
        #                 ind += 1
        #             tmps += '/'
        #     self.s[i] = tmps
        #     print(self.s[i])
    def output(self):
        #第一个字是汉字
        if self.inputdata[1]>= '\u4e00' and self.inputdata[1]<= '\u9fa5':
            i=0

            while(i<len(self.s) and i<len(self.sp)):
                self.outputdata+=self.s[i]
                self.outputdata+=self.sp[i]
                i+=1
            if i== len(self.s) and i!=len(self.sp):
                self.outputdata+=self.sp[i]
            else:
                self.outputdata+=self.s[i-1]
        else:
            i=0
            while (i < len(self.s) and i < len(self.sp)):
                self.outputdata += self.sp[i]
                self.outputdata += self.s[i]
                i += 1
            if i == len(self.s) and i != len(self.sp):
                self.outputdata += self.sp[i]
            else:
                self.outputdata += self.s[i-1]

if __name__=='__main__':
    m=self_seg()
    path='./icwb2-data/training/pku_training.utf8'
    m.load_data('input.txt')

    m.self_segmentation()
    m.output()
    file=open('./outputdata/out.txt','w',encoding='UTF-8')
    print(m.inputdata[1])
    s=m.outputdata+'\n'
    file.write(s)
    file.close()


