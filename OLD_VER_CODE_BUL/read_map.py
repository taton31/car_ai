track = []

def read_track():
    z_f=[]
    z_s=[]
    flag_ = True

    with open ('res/track2.txt', 'r') as f:
        for line in f:
            if line.strip() == '':
                flag_ = False
                continue

            if flag_:
                z_f.append(list(map(lambda x: int(x), line.strip().split(','))))
            else:
                z_s.append(list(map(lambda x: int(x), line.strip().split(','))))
            

    track.append(z_f)
    track.append(z_s)

    return track

if __name__ == "__main__":
    read_track()