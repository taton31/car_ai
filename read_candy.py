

def read_candy():
    z_f=[]
    candy = []

    with open ('res/candy.txt', 'r') as f:
        for line in f:
            if line.strip() == '':
                candy.append(z_f.copy())
                z_f.clear()
            else:
                z_f.append(list(map(lambda x: int(x), line.strip().split(','))))
            
            
    return candy

if __name__ == "__main__":
    print(read_candy())