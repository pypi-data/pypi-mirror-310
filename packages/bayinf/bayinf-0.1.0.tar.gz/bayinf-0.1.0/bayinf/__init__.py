import numpy as np
import scipy.stats as stats

def infer_binomial(data, prior_alpha=2, prior_beta=2):
    """
    Perform Bayesian inference for a binomial likelihood with a beta prior.
    
    :param data: List of observed data (1 for success, 0 for failure).
    :param prior_alpha: Alpha parameter of the Beta prior. Default is 2.
    :param prior_beta: Beta parameter of the Beta prior. Default is 2.
    :return: Posterior alpha and beta parameters.
    """
    heads = sum(data)
    tails = len(data) - heads
    posterior_alpha = prior_alpha + heads
    posterior_beta = prior_beta + tails
    return posterior_alpha, posterior_beta

def infer_poisson(data, prior_alpha=1, prior_beta=1):
    """
    Perform Bayesian inference for a Poisson likelihood with a gamma prior.
    
    :param data: List of observed data (counts).
    :param prior_alpha: Shape parameter of the Gamma prior. Default is 1.
    :param prior_beta: Rate parameter of the Gamma prior. Default is 1.
    :return: Posterior alpha and beta parameters.
    """
    total_counts = sum(data)
    n = len(data)
    posterior_alpha = prior_alpha + total_counts
    posterior_beta = prior_beta + n
    return posterior_alpha, posterior_beta

def infer_normal_known_variance(data, known_variance, prior_mean=0, prior_precision=1):
    """
    Perform Bayesian inference for a normal likelihood with a normal prior and known variance.
    
    :param data: List of observed data.
    :param known_variance: Known variance of the likelihood.
    :param prior_mean: Mean of the Normal prior. Default is 0.
    :param prior_precision: Precision (1/variance) of the Normal prior. Default is 1.
    :return: Posterior mean and precision.
    """
    n = len(data)
    sample_mean = np.mean(data)
    posterior_precision = prior_precision + n / known_variance
    posterior_mean = (prior_precision * prior_mean + n * sample_mean / known_variance) / posterior_precision
    return posterior_mean, posterior_precision

def infer_normal_unknown_variance(data, prior_mean=0, prior_precision=1, prior_df=2, prior_scale=1):
    """
    Perform Bayesian inference for a normal likelihood with a normal-gamma prior.
    
    :param data: List of observed data.
    :param prior_mean: Mean of the Normal prior. Default is 0.
    :param prior_precision: Precision (1/variance) of the Normal prior. Default is 1.
    :param prior_df: Degrees of freedom of the Gamma prior. Default is 2.
    :param prior_scale: Scale parameter of the Gamma prior. Default is 1.
    :return: Posterior mean, precision, degrees of freedom, and scale.
    """
    n = len(data)
    sample_mean = np.mean(data)
    sample_variance = np.var(data, ddof=1)
    posterior_precision = prior_precision + n
    posterior_mean = (prior_precision * prior_mean + n * sample_mean) / posterior_precision
    posterior_df = prior_df + n
    posterior_scale = (prior_df * prior_scale + (n - 1) * sample_variance + 
                       (prior_precision * n * (sample_mean - prior_mean)**2) / posterior_precision) / posterior_df
    return posterior_mean, posterior_precision, posterior_df, posterior_scale
