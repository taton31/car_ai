import numpy as np
import re

def read_par():


    with open ('good_par/1.txt', 'r') as f:
        a = f.read().strip().split('\n\n')[-1]
        a = a.replace('[[',']]').split(']]')[1:]
        
        a.pop(1)
        a[0] = re.sub(" +", " ", a[0])
        a[0] = a[0].split(']\n [')
        a[0] = list(map(lambda x: x.strip().split(' '), a[0]))
        a[0] = np.array(list(map(lambda x: list(map(lambda y: float(y), x)), a[0])))
        # print(a[0])

        a[1] = re.sub(" +", " ", a[1])
        a[1] = a[1].split(']\n [')
        a[1] = list(map(lambda x: x.strip().split(' '), a[1]))
        a[1] = np.array(list(map(lambda x: list(map(lambda y: float(y), x)), a[1])))

        a[2] = re.sub(" +", " ", a[2])
        a[2] = a[2].replace('[', '').replace(']', '').strip().split(' ')
        a[2] = list(map(lambda x: float(x), a[2]))
        a[2] = np.array(a[2])

        # print(a[2])
        # np.fromstring('[' + a[0].replace('\n',',') + ']', dtype=float, sep=' ')
        # a = list(map(lambda x: x.replace('[', '').replace(']', ''), a))
        # a = list(filter(None, list(map(lambda x: x.split('\n'), a))))

        # a = list(filter(None, list(map(lambda x: x.split(' '), a[0]))))
        # print(f.readlines()[2])
        # print(list(map(lambda x: x, f.readlines()[2])))

            # if flag_:
            #     z_f.append(list(map(lambda x: int(x), line.strip().split(','))))
            # else:
            #     z_s.append(list(map(lambda x: int(x), line.strip().split(','))))
            

    # track.append(z_f)
    # track.append(z_s)

    return a[0], a[1], a[2]


def read_par_2(str):


    with open (f'good_par/{str}.txt', 'r') as f:
        b = f.read().strip().split('\n\n')[-3:-1]
        c=[]
        for a in b:
            a = a.replace('[[',']]').split(']]')[1:]
            
            a.pop(1)
            a[0] = re.sub(" +", " ", a[0])
            a[0] = a[0].split(']\n [')
            a[0] = list(map(lambda x: x.strip().split(' '), a[0]))
            a[0] = np.array(list(map(lambda x: list(map(lambda y: float(y), x)), a[0])))
            # print(a[0])

            a[1] = re.sub(" +", " ", a[1])
            a[1] = a[1].split(']\n [')
            a[1] = list(map(lambda x: x.strip().split(' '), a[1]))
            a[1] = np.array(list(map(lambda x: list(map(lambda y: float(y), x)), a[1])))

            a[2] = re.sub(" +", " ", a[2])
            a[2] = a[2].replace('[', '').replace(']', '').strip().split(' ')
            a[2] = list(map(lambda x: float(x), a[2]))
            a[2] = np.array(a[2], dtype= float)
            c.append([a[0], a[1], a[2]])

    return c

if __name__ == "__main__":
    # print(read_par())
    a = read_par_2('1')

            
    # b = [a[0][0] - a[1][0], a[0][1] - a[1][1], a[0][2] - a[1][2]]
    # # print (read_par('tst')[0])
    # for i in b:
    #     print (i)
    #     print ()
    # w1_1, w2_1, b_1 = 
    # w1_2, w2_2, b_2