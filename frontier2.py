import sys
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def show_frontier(symbol1, symbol2, interval='MONTHLY'):
    returns1 = alpha_vantage.get_stock_returns_history(symbol1, interval)
    returns2 = alpha_vantage.get_stock_returns_history(symbol2, interval)

    if len(returns1) > len(returns2):
        returns1 = returns1[-len(returns2):]

    if len(returns2) > len(returns1):
        returns2 = returns2[-len(returns1):]

    mean_returns1 = np.mean(returns1)
    variance1 = np.var(returns1)
    standard_deviation1 = np.sqrt(variance1)

    print('Mean returns (%s) = %f' % (symbol1, mean_returns1))
    print('Varince (%s) = %f' % (symbol1, variance1))
    print('Standard Deviation (%s) = %f' % (symbol1, standard_deviation1))

    mean_returns2 = np.mean(returns2)
    variance2 = np.var(returns2)
    standard_deviation2 = np.sqrt(variance2)

    print('Mean returns (%s) = %f' % (symbol2, mean_returns2))
    print('Varince (%s) = %f' % (symbol2, variance2))
    print('Standard Deviation (%s) = %f' % (symbol2, standard_deviation2))

    correlation = np.corrcoef(returns1, returns2)[0][1]
    print('Corellation = %f' % correlation)

    weights = []

    for n in range(0, 101):
        weights.append((1 - 0.01 * n, 0 + 0.01 * n))

    returns = []
    standard_deviations = []

    portfolio_50_50_standard_deviation = None
    portfolio_50_50_returns = None

    for w1, w2 in weights:
        returns.append(w1 * mean_returns1 + w2 * mean_returns2)

        variance = w1**2 * standard_deviation1**2 + w2**2 * standard_deviation2**2 + 2 * w1 * w2 * standard_deviation1 * standard_deviation2 * correlation
        standard_deviation = np.sqrt(variance)
        standard_deviations.append(standard_deviation)

        plt.scatter(standard_deviations[-1], returns[-1], color='blue')

        if w1 == 0.5 and w2 == 0.5:
            portfolio_50_50_standard_deviation = standard_deviations[-1]
            portfolio_50_50_returns = returns[-1]

    plt.scatter(portfolio_50_50_standard_deviation, portfolio_50_50_returns, marker='x', color='red', alpha=1)
    plt.text(portfolio_50_50_standard_deviation, portfolio_50_50_returns, '50/50', fontsize=9)

    x_padding = np.average(standard_deviations) / 25
    plt.xlim(min(standard_deviations) - x_padding, max(standard_deviations) + x_padding)

    y_padding = np.average(returns) / 25
    plt.ylim(min(returns) - y_padding, max(returns) + y_padding)

    plt.gca().set_xticklabels(['{:.2f}%'.format(x*100) for x in plt.gca().get_xticks()])
    plt.gca().set_yticklabels(['{:.2f}%'.format(y*100) for y in plt.gca().get_yticks()])

    plt.title('Efficient Frontier (%s and %s)' % (symbol1, symbol2))

    plt.xlabel('Risk')
    plt.ylabel('Return')

    plt.show()

show_frontier(sys.argv[1], sys.argv[2])
