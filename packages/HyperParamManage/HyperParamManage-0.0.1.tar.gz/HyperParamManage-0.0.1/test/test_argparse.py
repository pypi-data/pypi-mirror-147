import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.hmm import HyperParams
hmm = HyperParams(a=2,d=[1,2,3])


if __name__ == '__main__':
    opt = hmm.to_arg_parser()
    hmm.update_from_arg_parser(opt)
    print(hmm)
    print(hmm())
