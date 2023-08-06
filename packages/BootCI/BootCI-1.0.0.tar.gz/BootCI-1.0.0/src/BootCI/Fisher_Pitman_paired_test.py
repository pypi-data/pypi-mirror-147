
import numpy as np

"""
  Function implementing the Fisher-Pitman test for paired samples
    x1: predicted scores from the first system to compare, one-dimensional numpy array
    x2: predicted scores from the second system to compare, one-dimensional numpy array
    y:  true scores, one-dimensional numpy array
    stat: the statistics to estimate. Must be a
          callable function that compute the performance measure such as accuracy, F1-score or Pearson r.
    n_iter: number of iterations for resampling. By default 10000
    Note: (n_iter-1) iterations are done because the p-value for this test cannot be smaller than one (the original sample) divided by the number of resamplings done.
"""
def fpreptest(x1, x2, y, stat, n_iter=10000):
    n = len(y)
    r = 0
    n_iter -= 1 # to get (n_iter-1) iterations
    obs_diff = abs(stat(x1,y)-stat(x2,y))
    x = np.squeeze(np.dstack((x1, x2)),axis=0)
    row = np.arange(n)
    for z in range(0, n_iter):
        p = np.random.randint(2, size=n)
        f1 = x[row,p]
        f2 = x[row,1-p]
        if (abs(stat(f1,y)-stat(f2,y)) >= obs_diff):
            r += 1
    return float(r+1.0)/(n_iter+1.0)
