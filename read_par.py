import numpy as np
import re
from constans import LENGTH_CHROM
def read_par(str):


    with open (f'par/{str}.txt', 'r') as f:
        a = f.read().strip().split('\n\n')[-1]
        a = a[a.find('[')+1:a.find(']')].replace('\n', ' ')
        a = re.sub(" +", " ", a)
        a=np.fromstring(a, count = LENGTH_CHROM, sep=' ')
        return a

if __name__ == "__main__":
    a = read_par('44')
    print(a)