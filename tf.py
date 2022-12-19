a=dict()
a[9]=[2,3]
a[5]='8'
a[2]='2'
a[3]='5'

b=sorted(a)
a.pop(list(a)[0])
print (a)