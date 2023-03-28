import re

f = open('flag.txt', 'r')

line = f.readline()

bins = []

for num in line.split():
    bin = f'{int(num, 16):08b}'
    bins.append(bin)

# lazy coding, haha
rotated = [''.join(list(i)[::-1]) for i in zip(*bins)]
rotated = [''.join(list(i)[::-1]) for i in zip(*rotated)]
rotated = [''.join(list(i)[::-1]) for i in zip(*rotated)]

sol = '\n'.join(rotated)
sol = re.sub('0', ' ', sol)
sol = re.sub('1', '■', sol)
print(sol)