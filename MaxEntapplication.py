from maxent.python.maxent import MaxentModel
from zhon.hanzi import punctuation
class MaxEntapplication:
    def __init__(self):
        pass
    def tag6_training_processing(self,file,tag_traing_set_file):
        self.contents=open(file,'r',encoding='UTF-8').read()

        self.contents=self.contents.replace(u"\r",'')
        self.contents=self.contents.replace(u'\n','')
        self.words=self.contents.split(' ')
        self.tag_words=[]
        i=0
        for word in self.words:
            i+=1
            if(i%100==0):
                self.tag_words.append('\r')
            if(len(word)==0):
                continue
            if(len(word)==1):
                tag_word=word+'/S'
            elif(len(word)==2):
                tag_word=word[0]+'/B'+word[1]+'E'
            elif(len(word)==3):
                tag_word=word[0]+'/B'+word[1]+'/C'+word[2]+'/E'
            elif(len(word)==4):
                tag_word=word[0]+'/B'+word[1]+'/C'+word[2]+'/D'+word[3]+'/E'
            else:
                tag_word=word[0]+'/B'+word[1]+'/C'+word[2]+'/D'
                mid_words=word[3:-1]
                for mid_word in mid_words:
                    tag_word+=mid_word+'/M'
                tag_word+=word[-1]+'/E'
            self.tag_words.append(tag_word)
        whole_tag_words=''.join(self.tag_words)
        fileout=open(tag_traing_set_file,'w',encoding='UTF-8')
        fileout.write(whole_tag_words)
        fileout.close()
        return (self.words,self.tag_words)

    def tag4_training_processing(self,file,tag_traning_set_file):
        filein=open(file,'r',encoding='UTF-8')
        self.contents=filein.read()
        filein.close()
        self.contents=self.contents.replace('\r','')
        self.contents=self.contents.replace('\n','')
        self.words=self.contents.split(' ')
        self.tag_words=[]
        i=0
        for word in self.words:
            i+=1
            if(i%100==0):
                self.tag_words.append('\r')
            if(len(word)==0):
                continue
            if(len(word)==1):
                tag_word=word+'/S'
            elif(len(word)==2):
                tag_word=word[0]+'/B'+word[1]+'/E'
            else:
                tag_word=word[0]+'/B'
                mid_words=word[1:-1]
                for mid_word in mid_words:
                    tag_word+=mid_word+'/M'
                tag_word+=word[-1]+'/E'
            self.tag_words.append(tag_word)
        whole_tag_words=''.join(self.tag_words)
        fileout=open(tag_traning_set_file,'w',encoding='UTF-8')
        fileout.write(whole_tag_words)
        fileout.close()
        return (self.words,self.tag_words)
    def get_near_char(self,contents,i,times):
        words_len=len(contents)/times
        if(i<0 or i>words_len-1):
            return '_'
        else:
            return contents[i*times]
    def get_near_tag(self,contents,i,times):
        words_len=len(contents)/times
        if i<0 or i>words_len-1:
            return '_'
        else:
            return contents[i*times*2]
    def ispunctuation(self,char):
        if char in punctuation:
            return '1'
        else:
            return '0'
    def get_class(self,char):
        zh_num = [u'零', u'○', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'百', u'千', u'万']
        ar_num = [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'.', u'０', u'１', u'２', u'３', u'４', u'５',
                  u'６', u'７', u'８', u'９']
        date = [u'日', u'年', u'月']
        letter = ['a', 'b', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'g', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                  't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        if char in zh_num or char in ar_num:
            return '1'
        elif char in date:
            return '2'
        elif char in letter:
            return '3'
        else:
            return '4'


    #获得训练集特征
    def get_train_set_feats(self,tag_file_path,feats_file_path):
        file=open(tag_file_path,'r',encoding='UTF-8')
        contents=file.read()
        file.close()
        contents=contents.replace('\r','').replace('\n','')
        word_len=int(len(contents)/3)
        self.train_set_feats=[]
        for i in range(word_len):
            pre_char=self.get_near_char(contents,i-1,3)
            pre_pre_char=self.get_near_char(contents,i-2,3)
            cur_char=self.get_near_char(contents,i,3)
            next_char=self.get_near_char(contents,i+1,3)
            next_next_char=self.get_near_char(contents,i+2,3)
            self.train_set_feats.append(
                contents[i * 3 + 2] + ' '
                + 'C-2=' + pre_pre_char + ' ' + 'C-1=' + pre_char + ' '
                + ' ' + 'C0=' + cur_char + ' '
                + 'C1=' + next_char + ' ' + 'C2=' + next_next_char + ' '
                + 'C-2=' + pre_pre_char + 'C-1=' + pre_char + ' '
                + 'C-1=' + pre_char + 'C0=' + cur_char + ' '
                + 'C0=' + cur_char + 'C1=' + next_char + ' '
                + 'C1=' + next_char + 'C2=' + next_next_char + ' '
                + 'C-1=' + pre_char + 'C1=' + next_char + ' '
                + 'C-2=' + pre_pre_char + 'C-1=' + pre_char + 'C0=' + cur_char + ' '
                + 'C-1=' + pre_char + 'C0=' + cur_char + 'C1=' + next_char + ' '
                + 'C0=' + cur_char + 'C1=' + next_char + 'C2=' + next_next_char + ' '
                + 'Pu=' + self.ispunctuation(cur_char) + ' '
                + 'Tc-2=' + self.get_class(pre_pre_char) + 'Tc-1=' + self.get_class(pre_char)
                + 'Tc0=' + self.get_class(cur_char) + 'Tc1=' + self.get_class(next_char)
                + 'Tc2=' + self.get_class(next_next_char) + ' '
                + '\r'
            )

        fileout=open(feats_file_path,'w',encoding='utf-8')
        for i in self.train_set_feats:
            fileout.write(i)
        fileout.close()


    #得到测试集特征
    def get_test_set_feats(self,test_file_path,feats_file_path):
        file=open(test_file_path,'r',encoding='UTF-8')
        contents=file.read()
        contents=contents.replace('\r','').replace('\n','')
        file.close()
        #诡吊的部分
        i=0
        word_len = int(len(contents) / 3)
        self.test_set_feats=[]
        for i in range(word_len):
            pre_char = self.get_near_char(contents, i - 1, 3)
            pre_pre_char = self.get_near_char(contents, i - 2, 3)
            cur_char = self.get_near_char(contents, i, 3)
            next_char = self.get_near_char(contents, i + 1, 3)
            next_next_char = self.get_near_char(contents, i + 2, 3)
            self.test_set_feats.append(
                contents[i * 3 + 2] + ' '
                + 'C-2=' + pre_pre_char + ' ' + 'C-1=' + pre_char + ' '
                + ' ' + 'C0=' + cur_char + ' '
                + 'C1=' + next_char + ' ' + 'C2=' + next_next_char + ' '
                + 'C-2=' + pre_pre_char + 'C-1=' + pre_char + ' '
                + 'C-1=' + pre_char + 'C0=' + cur_char + ' '
                + 'C0=' + cur_char + 'C1=' + next_char + ' '
                + 'C1=' + next_char + 'C2=' + next_next_char + ' '
                + 'C-1=' + pre_char + 'C1=' + next_char + ' '
                + 'C-2=' + pre_pre_char + 'C-1=' + pre_char + 'C0=' + cur_char + ' '
                + 'C-1=' + pre_char + 'C0=' + cur_char + 'C1=' + next_char + ' '
                + 'C0=' + cur_char + 'C1=' + next_char + 'C2=' + next_next_char + ' '
                + 'Pu=' + self.ispunctuation(cur_char) + ' '
                + 'Tc-2=' + self.get_class(pre_pre_char) + 'Tc-1=' + self.get_class(pre_char)
                + 'Tc0=' + self.get_class(cur_char) + 'Tc1=' + self.get_class(next_char)
                + 'Tc2=' + self.get_class(next_next_char) + ' '
                + '\r'
            )
        fileout=open(feats_file_path,'w',encoding='UTF-8')
        for i in self.test_set_feats:
            fileout.write(i)
        fileout.close()

    def split_by_blank(self,line):
        line_list=[]
        line_len=len(line)
        i=0
        while i<line_len:
            line_list.append(line[i])
            i+=2
        return line_list























