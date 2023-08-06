'''
Module for statistical bootstrapping.

Requirements: numpy 1.15.4
              scipy 1.1.0
              
Adapted from the bootstrap_interval module by Alexander Neshitov (https://github.com/neshitov/bootstrap\_interval)

'''
import numpy as np
import scipy
from scipy.stats import norm

class Bootstrap:
    '''
    The Boostrap class contains the resampling distribution for paired samples 
     (thus, on the difference between two performance measures computed on the same sample)
    Instance parameters:
    x1: predicted scores from the first system to compare, one-dimensional numpy array
    x2: predicted scores from the second system to compare, one-dimensional numpy array
    y:  true scores, one-dimensional numpy array
    stat: the statistics to estimate. Must be a
          callable function that compute the performance measure such as accuracy, F1-score or Pearson r.
    n_iter: number of iterations for resampling distribution. By default 10000
    sample_size: size of resampling sample. If None, equals to the size of the
                 data sample of the whole data sample (recommended)
    distribution: resampling distribution of the given statistics, array of
                  shape (n_iter,) consisting of values of statistics on the
                  bootstrap samples
    computed: a flag that shows if bootstrap distribution is stored in memory
    '''
    
    #Modified for paired
    def __init__(self, x1, x2, y, stat='mean', n_iter=10000, sample_size=None):
        ''' creates the class instance. does not compute the distribution'''
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.stat = stat
        self.n_iter = n_iter
        self.sample_size = sample_size
        self.computed = False
        self.distribution = None
        assert callable(self.stat), 'stat must be callable'
        if self.sample_size is None:
            self.sample_size = y.shape[0]
        self.theta = self.stat(self.x1,self.y) - self.stat(self.x2,self.y)
        
    def get_distribution(self):
        ''' returns the resampling distribution'''
        if not self.computed:
            distribution1 = np.zeros(self.n_iter)
            distribution2 = np.zeros(self.n_iter)
            self.distribution = np.zeros(self.n_iter)
            idx = np.random.randint(self.sample_size, size=(self.n_iter,self.sample_size))
            #self.distribution = np.apply_along_axis(self.stat, 1, bootstrap_samples)
            self.distribution1 = np.array([self.stat(np.take(self.x1,idx[i]),np.take(self.y,idx[i])) for i in range(self.n_iter) ])
            self.distribution2 = np.array([self.stat(np.take(self.x2,idx[i]),np.take(self.y,idx[i])) for i in range(self.n_iter) ])
            self.distribution = self.distribution1 - self.distribution2
            self.computed = True
        return self.distribution

    def get_confidence_interval(self, alpha, method='percentile'):
        ''' method computes the non-parametric confidence interval for paired samples (thus, on the difference)
        with significance level alpha
        Args:
            alpha: significance level
            method: one of ['percentile','sampling','bias_corrected']
                    if method='sampling' the interval is constructed from bootstrap
                    distribution quantiles
                    if method='percentile' the intrval is constructed using
                    percentile method (Ch. 23.1 van der Vaart, 'Asymptotic
                    statistics')
                    if method='bias_corrected' the interval is constructed using
                    the accelerated bias correction method (formula (2.3) of
                    T.DiCiccio, B.Efron, 'Bootstrap confidence intervals') (recommended)
        Returns:
            [left,right]: endpoints of confidence interval
        '''
        self.distribution = self.get_distribution()
        assert method in ['percentile', 'sampling', 'bias_corrected'], 'method \
                should be one of ["percentile", "sampling", "bias_corrected"]'
        if method == 'percentile':
            #theta = self.stat(self.sample)
            theta = self.theta
            xi_left, xi_right = np.quantile((self.distribution - theta),
                                            [alpha/2, 1-alpha/2])
            return np.array([theta - xi_right, theta - xi_left])

        elif method == 'bias_corrected':
            #theta_hat = self.stat(self.sample)
            theta_hat = self.theta
            fraction = np.sum(self.distribution < theta_hat) / len(self.distribution)
            z_0 = norm.ppf(fraction)
            n = len(self.y)
            U = np.zeros(n)
            for i in range(n):
                #U[i] = (n-1)*(theta_hat - self.stat(np.delete(self.sample, i)))
                U[i] = (n-1)*(theta_hat - (self.stat(np.delete(self.x1,i),np.delete(self.y,i)) - self.stat(np.delete(self.x2,i),np.delete(self.y,i))))
            # formula (6.6)  of DiCiccio, Efron
            a_hat = 1/6 * np.sum(np.power(U, 3)) / (np.sum(np.power(U, 2))**(1.5))
            def BC(level, z0, a):
                ''' right-hand side of formula (2.3)'''
                z_alpha = norm.ppf(level)
                return norm.cdf(z0 + (z0 + z_alpha) / (1 - a*(z0 + z_alpha)))
            return np.quantile(self.distribution, [BC(alpha/2, z_0, a_hat),
                                                   BC(1 - alpha/2, z_0, a_hat)])
        return np.quantile(self.distribution, [alpha/2, 1-alpha/2])
