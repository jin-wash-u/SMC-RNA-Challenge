import sys
import os
import math
import getopt
import warnings
from collections import Counter 
from collections import defaultdict
from scipy import stats

def usage():
    print """
    quantificationEvaluator -t <truth-tsv>  -i <input-tsv>
    
    Requested Parameters:
        -t/--truth-tsv    [string:    path to truth tsv]
        -i/--input-tsv         [string:    path to input tsv]

    Version:                    1.0.0
          """


#parameters
inFile = ''               #input tsv
inTruthFile = ''          #input truth tsv

def getParameters(argv):
    try:
        opts, args = getopt.getopt(argv,"ht:i:",["help",
                                                 "truth-tsv=",
                                                 "input-tsv="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            usage()
            sys.exit(1)
        elif opt in ("-i", "--input-tsv"):
            global inFile
            inFile= arg
        elif opt in ("-t","--truth-tsv"):
            global inTruthFile
            inTruthFile = arg



input_values_dic = defaultdict(lambda: 0.0)

def getInputDic():
    infile = "%s" % inFile
    f=open(infile,"r")
    while True:
        line=f.readline()
        if line=="":
            break
        else:
            tmp=line.split("\t")
            name=tmp[0]
            value=float(tmp[1][0:len(tmp[1])-1])
            input_values_dic[name]=value

truth_values = []
input_values = []

def getBothValues():
    infile = "%s" % inTruthFile
    f=open(infile,"r")
    while True:
        line=f.readline()
        if line=="":
            break
        else:
            tmp=line.split("\t")
            name=tmp[0]
            value=float(tmp[1][0:len(tmp[1])-1])
            truth_values.append(value)
            input_values.append(input_values_dic[name])

def calculateCor():
    cor,p_value=stats.spearmanr(truth_values,input_values)
    print "spearman\tp-value" 
    print("%s\t%s" % (cor,p_value))

def main(argv):
    getParameters(argv[1:])
    if inFile=='' or inTruthFile=='':
        usage()
        return 1
    getInputDic()
    getBothValues()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        calculateCor()
    return 0
    
if __name__ == '__main__':
    sys.exit(main(sys.argv))
