import os
# a=list(map(lambda x: int(x[:x.find('.')]), os.listdir('par')))

print(max(list(map(lambda x: int(x[:x.find('.')]), os.listdir('par')))))