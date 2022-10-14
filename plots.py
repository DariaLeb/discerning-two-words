import math

import matplotlib.pyplot as plt


if __name__ == '__main__':

    ns = range(6, 32, 2)
    ms = [4, 5, 5, 6, 7, 7, 7, 8, 8, 9, 9, 9, 10]

    min_s = [4, 4, 4, 6, 6, 6, 4, 8, 8, 12, 12, 8, 16]
    max_s = [4, 6, 8, 8, 8, 12, 12, 8, 16, 14, 20, 20, 18]

    log = [math.log(n) for n in ns]
    half = [n // 2 for n in ns]

    plt.figure()
    plt.plot(ns, ms, label='m')
    plt.plot(ns, min_s, label='min |s|')
    plt.plot(ns, max_s, label='max |s|')
    # plt.plot(ns, log, label='log')
    plt.plot(ns, half, label='n/2')

    plt.xlabel('n')

    plt.legend()
    plt.grid()

    plt.savefig('images/results_sizes.jpg')
    plt.show()

