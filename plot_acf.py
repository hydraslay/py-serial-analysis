import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt

dta = sm.datasets.sunspots.load_pandas().data
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('1700', '2008'))
del dta["YEAR"]
squeezed = dta.values.squeeze()
sm.graphics.tsa.plot_acf(squeezed, lags=40)
plt.show()
