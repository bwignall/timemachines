from timemachines.skatertools.visualization.priorplot import prior_plot_exogenous
from statsmodels.tsa.arima.model import ARIMA
from timemachines.skatertools.utilities.conventions import Y_TYPE, A_TYPE, R_TYPE, E_TYPE, T_TYPE, wrap
from typing import Any
from timemachines.skaters.tsa.tsaparams import TSA_META

TSA_P_DEFAULT = 3
TSA_D_DEFAULT = 0
TSA_Q_DEFAULT = 3


def tsa_constant_skater_factory(y: Y_TYPE, s: dict, k: int, a: A_TYPE = None,
                             t: T_TYPE = None, e: E_TYPE = None,
                             p:int=TSA_P_DEFAULT, d:int=TSA_D_DEFAULT, q:int=TSA_D_DEFAULT) -> ([float], Any, Any):
    """ Extremely simple univariate, fixed p,d,q ARIMA model that is re-fit each time """

    y = wrap(y)
    a = wrap(a)

    if not s.get('y'):
        s = {'y': list(),
             'a': list(),
             'k': k}
    else:
        # Assert immutability of k, dimensions
        if s['y']:
            assert len(y) == len(s['y'][0])
            assert k == s['k']
        if s['a']:
            assert len(a) == len(s['a'][0])

    if y is None:
        return None, s, None
    else:
        s['y'].append(y)
        if a is not None:
            s['a'].append(a)
        if len(s['y']) > max(2 * k + 5, TSA_META['n_warm']):
            y0s = [ y_[0] for y_ in s['y']]
            model = ARIMA(y0s, order=(p,d,q))
            x = list( model.fit().forecast(steps=k) )
            x_std = [1.0]*k
        else:
            x = [y[0]] * k
            x_std = [1.0] * k
        return x, x_std, s


def tsa_constant_skater_p3_d0_q3(y: Y_TYPE, s: dict, k: int, a: A_TYPE = None,
                             t: T_TYPE = None, e: E_TYPE = None) -> ([float], Any, Any):
    return tsa_constant_skater_factory(y=y,s=s,k=k,a=a,t=t,e=e)


def tsa_constant_skater_p3_d1_q3(y: Y_TYPE, s: dict, k: int, a: A_TYPE = None,
                             t: T_TYPE = None, e: E_TYPE = None) -> ([float], Any, Any):
    return tsa_constant_skater_factory(y=y,s=s,k=k,a=a,t=t,e=e)


TSA_SKATERS_CONSTANT = [ tsa_constant_skater_p3_d0_q3, tsa_constant_skater_p3_d1_q3 ]


if __name__=='__main__':
    prior_plot_exogenous(f=tsa_constant_skater_factory,k=5,n=TSA_META['n_warm']+25,n_plot=50)