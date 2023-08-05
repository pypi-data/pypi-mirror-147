"""结巴命令行界面"""
import sys
import jieba
from argparse import ArgumentParser
# from ._compat import *

parser = ArgumentParser(usage="%s -m 结巴 [选项] 文件名" % sys.executable, description="结巴命令行界面.", epilog="若未指定文件名, 则使用标准输入(STDIN).")
parser.add_argument("-d", "--delimiter", metavar="DELIM", default=' / ',
                    nargs='?', const=' ',
                    help="使用 DELIM 分隔词语，而不是用默认的' / '。若不指定 DELIM，则使用一个空格分隔。")
parser.add_argument("-p", "--pos", metavar="DELIM", nargs='?', const='_',
                    help="启用词性标注；如果指定 DELIM，词语和词性之间用它分隔，否则用 _ 分隔")
parser.add_argument("-D", "--dict", help="使用 DICT 代替默认词典")
parser.add_argument("-u", "--user-dict",
                    help="使用 USER_DICT 作为附加词典，与默认词典或自定义词典配合使用")
parser.add_argument("-a", "--cut-all",
                    action="store_true", dest="cutall", default=False,
                    help="全模式分词（不支持词性标注）")
parser.add_argument("-n", "--no-hmm", dest="hmm", action="store_false",
                    default=True, help="不使用隐含马尔可夫模型")
parser.add_argument("-q", "--quiet", action="store_true", default=False,
                    help="不打印加载消息到错误输出(stderr)")
parser.add_argument("-V", '--version', action='version',
                    version="Jieba " + jieba.__version__)
parser.add_argument("文件名", nargs='?', help="输入文件")

args = parser.parse_args()

if args.quiet:
    jieba.setLogLevel(60)
if args.pos:
    import jieba.posseg
    posdelim = args.pos
    def cutfunc(sentence, _, HMM=True):
        for w, f in jieba.posseg.cut(sentence, HMM):
            yield w + posdelim + f
else:
    cutfunc = jieba.cut

delim = str(args.delimiter)
cutall = args.cutall
hmm = args.hmm
fp = open(args.文件名, 'r') if args.文件名 else sys.stdin

if args.dict:
    jieba.initialize(args.dict)
else:
    jieba.initialize()
if args.user_dict:
    jieba.load_userdict(args.user_dict)

ln = fp.readline()
while ln:
    l = ln.rstrip('\r\n')
    result = delim.join(cutfunc(ln.rstrip('\r\n'), cutall, hmm))
    # if PY2:
        # result = result.encode(default_encoding)
    print(result)
    ln = fp.readline()

fp.close()
