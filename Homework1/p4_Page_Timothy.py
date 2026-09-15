import matplotlib.pyplot as plt
import math

def plot_function(fun_str, domain, ns):
    xmin, xmax = domain
    step = (xmax - xmin) / (ns - 1)

    xs = []

    for i in range(ns):
        x = xmin + i * step
        xs.append(x)

    ys = []

    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    print("x          y")
    print("--------------------")

    for i in range(ns):
        print("{:10.4f} {:10.4f}".format(xs[i], ys[i]))

    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.show()


fun_str = input("Enter function with variable x: ")
ns = int(input("Enter number of samples: "))
xmin = float(input("Enter xmin: "))
xmax = float(input("Enter xmax: "))

domain = (xmin, xmax)

plot_function(fun_str, domain, ns)