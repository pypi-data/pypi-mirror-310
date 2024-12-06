import matplotlib.pyplot as plt
from datetime import datetime
import pickle 
import pandas as pd 
import os, sys
script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, '..', 'toolbox'))
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../src/econ_tools")
from data_moments import data_moments
from data_class import Data

# Options
savefig = False
showfig = True
data_raw_in = os.path.join(script_dir, '..', 'data', 'data_raw.test')

# Load data (pickle)
f = open(data_raw_in, 'rb')
dataraw = pickle.load(f)
f.close()

## Transform dat
# Sample
D1 = '01-Jan-1989'
D2 = '31-Dec-2019'
# Quarterly GDP
GDP_q = Data(dataraw, 'GDP').agg('quarterly', 'lastvalue')
# data 
data = pd.DataFrame({
    # Quarterly GDP growth rate
    "GDP-logdiff": GDP_q.trans('logdiff', 1).trunc(D1, D2).tt(),
    # Quarterly cyclical GDP
    "GDP-hfilter": GDP_q.trans('100log').filter(D1, D2, 'hamilton', LagLength=4, LeadLength=8).tt()
})

## Summarize data
print('Summary Statistics')
vars = ['GDP-logdiff', 'GDP-hfilter']
# Select stats
moms = ['mean', 'SD', 'Skew', 'Kurt']
# Calculate statistics and display
data_moments(data, vars, moms)

## Plot data
# Figure width, height (inches)
fig_opt = {
    'figpos': [1, 1, 6.5, 4],
    'fontsize': 10,
    # Subplot padding (proportion of axis box)
    'pad': {
        'topmarg': 0.03,
        'leftmarg': 0.08,
        'vspace': 0.05,
        'hspace': 0.08,
        'rightmarg': 0.02,
        'botmarg': 0.09
    }
}

# Plot 
if not showfig and not savefig:
    exit(0)
vars = data.columns
nvars = len(vars)
fig, axes = plt.subplots(nvars, 1, figsize=(10, 8))
fig.subplots_adjust(
    top=1-fig_opt['pad']['topmarg'],
    bottom=fig_opt['pad']['botmarg'],
    left=fig_opt['pad']['leftmarg'],
    right=1-fig_opt['pad']['rightmarg'],
    hspace=fig_opt['pad']['hspace'],
    wspace=fig_opt['pad']['vspace']
)
ylims = []
recessions = [(datetime(1980, 1, 1), datetime(1991, 7, 1)), (datetime(1990, 7, 1), datetime(1991, 3, 1)), (datetime(2001, 3, 1), datetime(2001, 11, 1)), (datetime(2007, 12, 1), datetime(2009, 6, 1)), (datetime(2020, 2, 1), datetime(2020, 4, 1))]
for ivar in range(nvars):
    plt.subplot(nvars, 1, ivar + 1)
    ax = axes[ivar]
    ax.plot(data.index, data[vars[ivar]])
    ax.set_ylabel(vars[ivar])
    ax.grid(True)
    
    if ivar == nvars - 1:
        ax.set_xlabel('Quarters')
    
    ylims.append(ax.get_ylim())
    axes[ivar].set_ylim(ylims[ivar])
    # shade the recession periods if within time period
    for i in range(len(recessions)):
        if recessions[i][0] >= data.index[0] and recessions[i][1] <= data.index[-1]:
            plt.axvspan(recessions[i][0], recessions[i][1], color='gray', alpha=0.5)

if savefig:
    plt.savefig(f'out/data_test.pdf')

if showfig:
    plt.show()