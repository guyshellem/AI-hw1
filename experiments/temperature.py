import numpy as np
from matplotlib import pyplot as plt

X = np.array([400, 450, 900, 390, 550])

# TODO: Write the code as explained in the instructions

alpha = min(X)
P = []
T = list(map(lambda x: 0.01+x*(4.99/100), range(101)))
for t in T:
    sum_of_prob = sum(list(map(lambda x: (x/alpha)**(-1/t), X)))
    P += [np.array(list(map(lambda x: round(((x/alpha)**(-1/t))/sum_of_prob, 2), X)))]



#raise NotImplemented()  # TODO: remove!

print(P)

for i in range(len(X)):
    plt.plot(T, P[:, i], label=str(X[i]))

plt.xlabel("T")
plt.ylabel("P")
plt.title("Probability as a function of the temperature")
plt.legend()
plt.grid()
plt.show()
exit()
