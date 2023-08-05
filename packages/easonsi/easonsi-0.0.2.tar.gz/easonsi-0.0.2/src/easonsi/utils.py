import json
import os, sys

def LoadJsonsg(fn): return map(json.loads, LoadListg(fn))
def LoadJsons(fn): return list(LoadJsonsg(fn))
def SaveJsons(st, ofn): return SaveList([json.dumps(x, ensure_ascii=False) for x in st], ofn)


def LoadListg(fn):
    with open(fn, encoding="utf-8") as fin:
        for ll in fin:
            ll = ll.strip()
            if ll != '': yield ll

def readJson(path):
    f = open(path, encoding='utf-8')
    jsonData = json.load(f)
    f.close()
    return jsonData


def toJson(dic, path):
    f = open(path, 'w', encoding='utf-8')
    jsonData = json.dumps(dic, indent=4, ensure_ascii=False)
    f.write(jsonData)
    f.close()

def SaveList(st, ofn):
    with open(ofn, "w", encoding = "utf-8") as fout:
        for k in st:
            fout.write(str(k) + "\n")
            
def dcopy(x):
    if type(x) is type(''): return x
    return {x:dcopy(y) for x, y in x.items()}

def LoadCSV(fn, sep="\t"):
    ret = []
    with open(fn, encoding='utf-8') as fin:
        for line in fin:
            lln = line.rstrip('\r\n').split(sep)
            ret.append(lln)
    return ret

def SaveCSV(csv, fn):
    with open(fn, 'w', encoding='utf-8') as fout:
        for x in csv:
            WriteLine(fout, x)

def WriteLine(fout, lst):
    fout.write('\t'.join([str(x) for x in lst]) + '\n')

import six
import numpy as np
import collections

# from tensorflow.keras.preprocessing.sequence import pad_sequences
def pad_sequences(sequences, maxlen=None, dtype='int32',
                  padding='pre', truncating='pre', value=0.):
    if not hasattr(sequences, '__len__'):
        raise ValueError('`sequences` must be iterable.')
    num_samples = len(sequences)

    lengths = []
    sample_shape = ()
    flag = True

    # take the sample shape from the first non empty sequence
    # checking for consistency in the main loop below.

    for x in sequences:
        try:
            lengths.append(len(x))
            if flag and len(x):
                sample_shape = np.asarray(x).shape[1:]
                flag = False
        except TypeError:
            raise ValueError('`sequences` must be a list of iterables. '
                             'Found non-iterable: ' + str(x))

    if maxlen is None:
        maxlen = np.max(lengths)

    is_dtype_str = np.issubdtype(dtype, np.str_) or np.issubdtype(dtype, np.unicode_)
    if isinstance(value, six.string_types) and dtype != object and not is_dtype_str:
        raise ValueError("`dtype` {} is not compatible with `value`'s type: {}\n"
                         "You should set `dtype=object` for variable length strings."
                         .format(dtype, type(value)))

    x = np.full((num_samples, maxlen) + sample_shape, value, dtype=dtype)
    for idx, s in enumerate(sequences):
        if not len(s):
            continue  # empty list/array was found
        if truncating == 'pre':
            trunc = s[-maxlen:]
        elif truncating == 'post':
            trunc = s[:maxlen]
        else:
            raise ValueError('Truncating type "%s" '
                             'not understood' % truncating)

        # check `trunc` has expected shape
        trunc = np.asarray(trunc, dtype=dtype)
        if trunc.shape[1:] != sample_shape:
            raise ValueError('Shape of sample %s of sequence at position %s '
                             'is different from expected shape %s' %
                             (trunc.shape[1:], idx, sample_shape))

        if padding == 'post':
            x[idx, :len(trunc)] = trunc
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc
        else:
            raise ValueError('Padding type "%s" not understood' % padding)
    return x

def get_best_index(prob,n_best_size):
    # 返回 logit 最高的位置
    index_and_score = sorted(enumerate(prob), key=lambda x: x[1], reverse=True)

    best_indexes = []
    for i in range(len(index_and_score)):
        if i >= n_best_size:
            break
        best_indexes.append(index_and_score[i][0])
    return best_indexes

PrelimPrediction = collections.namedtuple(  # pylint: disable=invalid-name
        "PrelimPrediction",
        ["start_index", "end_index", "start_logit", "end_logit"])

def iswrap(start_index,end_index,test_start,test_end):
    # 判断是否嵌套
    if(start_index>=test_end or end_index<=test_start):
        return False
    else:
        return True

def extract_one_by_logits(start_logits,end_logits,sentence_length,threshold,args):      # threshold=12
    # 输入：start_logits,end_logits 两个分布
    # 输出：概率较大的 n_best_size//2 个头尾 span
    # 1. 先取概率最高的 topk 个位置
    start_indexes=get_best_index(start_logits,args.n_best_size)
    end_indexes=get_best_index(end_logits,args.n_best_size)
    prelim_predictions_per_feature=list()
    span_start_end=[]
    # 2. 按照基本的规则筛选头尾 pair，保存在 prelim_predictions_per_feature
    for start_index in start_indexes:
        for end_index in end_indexes:
            if(start_index>=sentence_length or end_index>sentence_length):
                continue
            if(start_index>=end_index):
                continue
            if(end_index-start_index>args.max_answer_length):
                continue
            start_prob=start_logits[start_index]
            end_prob=end_logits[end_index]
            if(start_prob+end_prob<threshold):
                continue
            prelim_predictions_per_feature.append(PrelimPrediction(start_index=start_index,end_index=end_index,start_logit=start_prob,end_logit=end_prob))
    # 这里要看看end_index和start_index的取值，看看end_index代表的token是否包含在答案里面，然后看看+1还是+0....好像没影响，反正所有样本都加的 1
    prelim_predictions_per_feature = sorted(prelim_predictions_per_feature,key=lambda x: (x.start_logit + x.end_logit - (x.end_index - x.start_index + 1)),reverse=True)        # scope 长度施加负向权重
    # 3. 根据概率大输出 span，注意要排除嵌套结构
    while len(prelim_predictions_per_feature)>0:
        if(len(span_start_end)>=(args.n_best_size//2)): # 输出 args.n_best_size//2 个 span
            break
        pred_i=prelim_predictions_per_feature[0]
        span_start_end.append((pred_i.start_index,pred_i.end_index))
        # 排除嵌套的 span
        new_prelim_predictions_pre_feature=list()
        for ii in range(1,len(prelim_predictions_per_feature)):
            cur_pred_i=prelim_predictions_per_feature[ii]
            if(not iswrap(pred_i.start_index,pred_i.end_index,cur_pred_i.start_index,cur_pred_i.end_index)):
                new_prelim_predictions_pre_feature.append(cur_pred_i)
        prelim_predictions_per_feature=new_prelim_predictions_pre_feature
    return span_start_end

def convert_span_start_end_to_text(span_start_end, input_ids, tokenizer, fix_index_bias=0):
    # 返回 span_start_end 列表中所有的 span 所对应的字符串
    result=list()
    for start,end in span_start_end:
        tokens=input_ids[start+fix_index_bias:end+fix_index_bias]
        text=tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(tokens))
        # text=text.replace(" - ","-")
        result.append(text)
    return result

