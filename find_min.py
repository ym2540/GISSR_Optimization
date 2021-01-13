import numpy as np
d = []
for i in range(1530):
    d.append(np.genfromtxt('n2/'+str(i)))
d = np.array(d)
minv = d[0,3]
mini = 0
for i in range(1530):
    if (d[i,3] < minv):
        minv = d[i,3]
        mini = i

print(mini)
print(minv)
