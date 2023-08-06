import sys
import argparse
import os

def main(args=None):
    parse = argparse.ArgumentParser()
    parse.add_argument('-qh', )
    args = parse.parse_args()
    cmd = "pip install " + args.qh + " -i https://pypi.tuna.tsinghua.edu.cn/simple"
    os.system(cmd)


if __name__ == '__main__':
    sys.exit(main())