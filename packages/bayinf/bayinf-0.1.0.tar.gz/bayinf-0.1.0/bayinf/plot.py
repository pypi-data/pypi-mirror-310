import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def beta(alpha, beta, title):
    """
    Plot the Beta distribution with given alpha and beta parameters.
    
    :param alpha: Alpha parameter of the Beta distribution.
    :param beta: Beta parameter of the Beta distribution.
    :param title: Title of the plot.
    """
    x = np.linspace(0, 1, 1000)
    y = stats.beta.pdf(x, alpha, beta)
    plt.plot(x, y, label=f'Beta({alpha}, {beta})')
    plt.title(title)
    plt.xlabel('θ (Probability of Success)')
    plt.ylabel('Density')
    plt.legend()
    plt.show()

def gamma(alpha, beta, title):
    """
    Plot the Gamma distribution with given alpha and beta parameters.
    
    :param alpha: Shape parameter of the Gamma distribution.
    :param beta: Rate parameter of the Gamma distribution.
    :param title: Title of the plot.
    """
    x = np.linspace(0, 10, 1000)
    y = stats.gamma.pdf(x, alpha, scale=1/beta)
    plt.plot(x, y, label=f'Gamma({alpha}, {beta})')
    plt.title(title)
    plt.xlabel('λ (Rate Parameter)')
    plt.ylabel('Density')
    plt.legend()
    plt.show()

def normal(mean, precision, title):
    """
    Plot the Normal distribution with given mean and precision.
    
    :param mean: Mean of the Normal distribution.
    :param precision: Precision (1/variance) of the Normal distribution.
    :param title: Title of the plot.
    """
    variance = 1 / precision
    std_dev = np.sqrt(variance)
    x = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 1000)
    y = stats.norm.pdf(x, mean, std_dev)
    plt.plot(x, y, label=f'Normal({mean}, {1/precision})')
    plt.title(title)
    plt.xlabel('μ (Mean)')
    plt.ylabel('Density')
    plt.legend()
    plt.show()
