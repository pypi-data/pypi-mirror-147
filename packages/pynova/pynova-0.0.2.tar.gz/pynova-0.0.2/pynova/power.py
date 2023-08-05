import scipy.stats
import numpy as np

def power_anova_test(groups=None, n=None, between_var=None, within_var=None, sig_level=0.05, power=None):
    if power == None:
        ncp = (groups - 1) * n * (between_var/within_var)
        q = scipy.stats.f.ppf(1-sig_level, groups-1, dfd=(n-1) * groups)

        return 1 - scipy.stats.ncf.cdf(q, groups-1, (n-1) * groups, ncp)