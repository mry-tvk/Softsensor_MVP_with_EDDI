import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.plotting.backend = 'plotly'


def MAPE(Y_actual,Y_Predicted):
    not_na = ~ np.isnan(Y_actual)
    y_act = [ (Y_actual[idx] - Y_Predicted[idx])/Y_actual[idx]  for idx in range(len(Y_actual)) if not_na[idx]]
    mape = np.mean(np.abs(y_act))*100
    return mape

def plot_signal(df_actual, df_pred, df_linear, plot_column):
    # gca stands for 'get current axis'
    ax = plt.gca()
    df_actual.plot(kind='line', y=plot_column,ax=ax, label="actual") #+ " [imputation: " + str(train_rows)+"-end]")
    df_linear.plot(kind='line', y=plot_column,ax=ax, color='green', label="linear") #+ " [imputation: " + str(train_rows)+"-end]")
    
    df_pred.plot(kind='line', y=plot_column, color='red', ax=ax, label="EDDI")

    mape_forecast_eddi = MAPE(df_actual[plot_column].values, df_pred[plot_column].values)
    mape_forecast_linear = MAPE(df_actual[plot_column].values, df_linear[plot_column].values)

    plt.title('Tag: ' + plot_column + '\n' + 'MAPE (EDDI): {:.2f}%'.format(mape_forecast_eddi) + '\n' + 'MAPE (Linear): {:.2f}%'.format(mape_forecast_linear))
    
    plt.show()
