import sys

delta = int(sys.argv[1])
vol = int(sys.argv[2])
time = (delta*10**-6*vol)/(.1/60)

print(time, " at 100 mL/min")
