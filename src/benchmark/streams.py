from sys import stderr, stdout
from re import compile
import time

start = time.time()
pattern = compile(r'^Triad: +(\d+\.\d+) .*$')
average = 0.0
minimum = 1.0e75
maximum = 0.0

file = open("streams.out")
count = 0
while file :
    line = file.readline()
    if not line :
        break
    elif pattern.match(line) :
        count = count+1
        x = float(pattern.sub(r'\1',line))
        average = average+x
        minimum = min(minimum,x)
        maximum = max(maximum,x)
file.close()
if count != 0 :
    average = average/count
stdout.write("Triad:  %6.1f MB/sec (%d from %.1f to %.1f) Time: %s\n" % \
    (average,count,minimum,maximum, time.time() - start))
