from os import listdir
from os.path import isfile, join
from shutil import move, copyfile

mypath = '/net/home/dakarlss/ml2017/'
destpath = '/net/data1/ml2017/mem_profiles/valid100-3000/'

filenames = [f for f in listdir(mypath) if isfile(join(mypath, f)) and 'mprofile' in f]
filenames.sort()
print(len(filenames))
filenames.pop(0)
filenames.pop(0)

val = 0
for file in filenames:
    val += 100
    with open(file, 'r') as inF:
        for line in inF:
            if 'FUNC' in line:
                print(file)
                entries = line.split()
                time = float(entries[-1]) - float(entries[-3])
                print(time)
    #dest = 'val' + str(val)
    #copyfile(join(mypath, file), join(destpath, dest))
                
