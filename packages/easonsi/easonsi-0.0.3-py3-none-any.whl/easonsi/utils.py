from .util.io import *
from .util.network import *
from .util.file import *

def IsChsStr(z):
    """ 中文字符: [\u4e00-\u9fa5] """
    return re.search('^[\u4e00-\u9fa5]+$', z) is not None

def FreqDict2List(dt):
    """ 将 Counter 按照 value 排序, 转为 list
    例如输出 [("value_1", 3), ("value_2", 2)]"""
    return sorted(dt.items(), key=lambda d:d[-1], reverse=True)

def CalcF1(correct, output, golden):
    """ 输入: TP, P, T
    输出: 指标的描述 """
    prec = correct / max(output, 1);  reca = correct / max(golden, 1);
    f1 = 2 * prec * reca / max(1e-9, prec + reca)
    pstr = 'Prec: %.4f %d/%d, Reca: %.4f %d/%d, F1: %.4f' % (prec, correct, output, reca, correct, golden, f1)
    return pstr

class TokenList:
    """ 定义 token 列表 """
    def __init__(self, file, low_freq=2, source=None, func=None, save_low_freq=2, special_marks=[]):
        """ 
        file: 每一行为 `token\tfrequence`
        以下参数仅在 file 为 None 时有效
            source 为所有原始词的列表; func 对每个词进行筛选; 最终 source 处理后词频 >=save_low_freq 的保留
            special_marks: 额外定义的特殊 token"""
        if not os.path.exists(file):
            tdict = defaultdict(int)
            # 设置 special_marks 一个较高的频次, 以保留
            for i, xx in enumerate(special_marks): tdict[xx] = 100000000 - i
            for xx in source:
                for token in func(xx): tdict[token] += 1
            tokens = FreqDict2List(tdict)
            tokens = [x for x in tokens if x[1] >= save_low_freq]
            SaveCSV(tokens, file)
        self.id2t = ['<PAD>', '<UNK>'] + \
            [x for x,y in LoadCSV(file) if float(y) >= low_freq]
        self.t2id = {v:k for k,v in enumerate(self.id2t)}
    def get_id(self, token): return self.t2id.get(token, 1)
    def get_token(self, ii): return self.id2t[ii]
    def get_num(self): return len(self.id2t)

