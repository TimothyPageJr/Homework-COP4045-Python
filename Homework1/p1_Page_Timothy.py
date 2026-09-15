import matplotlib.pyplot as plt
import math

while True:
    a_input = input("Enter a: ")

    if a_input == "":
        break

    a = float(a_input)
    b = float(input("Enter b: "))
    c = float(input("Enter c: "))

    discriminant = b ** 2 - 4 * a * c

    # Determine and display the roots
    if discriminant < 0:
        print("no real solutions")

    elif discriminant == 0:
        x1 = -b / (2 * a)
        print(f"one solution: {x1:.5f}")

    else:
        x1 = (-b - math.sqrt(discriminant)) / (2 * a)
        x2 = (-b + math.sqrt(discriminant)) / (2 * a)
        print(f"two solutions: x1={x1:.5f} x2={x2:.5f}")

    # Choose the graph domain
    if discriminant < 0:
        xopt = -b / (2 * a)
        xmin = xopt - 5
        xmax = xopt + 5

    elif discriminant == 0:
        xmin = x1 - 5
        xmax = x1 + 5

    else:
        xmin = min(x1, x2) - 2
        xmax = max(x1, x2) + 2

    # Generate exactly 150 x-values
    step = (xmax - xmin) / 149
    xs = []

    for i in range(150):
        x = xmin + i * step
        xs.append(x)

    # Calculate the matching y-values
    ys = []

    for x in xs:
        y = a * x ** 2 + b * x + c
        ys.append(y)

    # Plot the quadratic
    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"y = {a}x^2 + {b}x + {c}")
    plt.grid(True)
    plt.show()