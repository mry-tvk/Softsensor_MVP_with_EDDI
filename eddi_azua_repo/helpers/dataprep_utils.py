
import numpy as np
import pandas as pd
import requests
import os
import json


def long_to_wide(df, tag_colname='tag', time_colname='time', val_colname='value', resample_time=False, resample_granularity='Min'):
    # only our cols
    df_wide=df[[tag_colname, time_colname, val_colname]].copy()

    # sort by time
    df_wide = df_wide.sort_values(by=time_colname)

    # create pivot-table
    df_wide = df_wide.pivot_table(index=time_colname,columns=tag_colname, aggfunc='mean')

    # average out over min granularity
    if resample_time:
        df_wide = df_wide.resample(resample_granularity, level=time_colname).mean()

    # remove multi-index
    df_wide.columns = [x[1] for x in df_wide.columns]

    # df = df.reindex(idx)
    return df_wide

# # wide back to long
def wide_to_long(df, index_colname='time', tag_name='tag', value_name='value'):
    # assumption time is index
    df_long=df.copy()
    df_long[index_colname]=df_long.index
    df_long.reset_index(drop=True, inplace=True)
    df_long.sort_values(by=index_colname)
    df_long.reset_index(drop=True, inplace=True)
    df_long = pd.melt(df_long,id_vars=[index_colname], var_name=tag_name, value_name=value_name)
    return df_long


def extend_features_with_temporal_window(df_orig, to_extend_columns, temp_start=1, temp_step_size=1, temp_num_steps=1):
    """
    temporal_start: what is the temporal distance of first temporal feature (prev & next). Default: 1
    (e.g., temporal_start=1 adds X_{t-1} & X_{t+1} or temporal_start=2 adds X_{t-2} & X_{t+2} to the featuresets)
    temp_step_size: the distance of two temporal features on each side of the feature; if the temp_num_steps=0, then this value does not matter. Default: 1
    temp_num_steps: the number of temporal features on each side. Default: 1
    
    If you want to include temporal features in multiple distances, you can change the temp_step_size & temp_num_steps to control the step size and the number of steps. For example if temp_start=1, temp_step_size=2, temp_num_steps=3, it will add X_{t-1} & X_{t+1} features to the features and then since temp_step_size equals to 2, it adds X_{t-3} & X_{t+3} to the featureset. As the temp_num_steps=3, it also adds X_{t-5} & X_{t+5}, which adds up to three temporal features on each side.
    """
    
    df_ext = df_orig.copy()
    colnames = list(df_ext.columns)
    
    for step in range(temp_num_steps):
        #shift values down by 1 => all cols but time
        df_tprev = df_ext[to_extend_columns].shift(temp_start + step*temp_step_size) #shift down
        df_tnext = df_ext[to_extend_columns].shift(-(temp_start + step*temp_step_size)) #shift up

        # rename columns
        df_tprev.columns = ['prev' +str(temp_start + (step)*temp_step_size)+'_' + tagname for tagname in df_tprev.columns]
        df_tnext.columns = ['next' +str(temp_start + (step)*temp_step_size)+'_' + tagname for tagname in df_tnext.columns]

        # column-names correction
        colnames = colnames + list(df_tprev.columns)
        colnames = colnames + list(df_tnext.columns)

        # combine starting from original => then prev => then next
        df_ext = pd.concat([df_ext, df_tprev, df_tnext], axis=1)
    return df_ext, colnames

def compute_missing_ratio(df):
    df_missing = (df.isnull().sum() / len(df)) * 100
    df_missing = df_missing.drop(df_missing[df_missing == 0].index).sort_values(ascending = False)
    display(pd.DataFrame({'Missing Ratio' :df_missing}))


def get_variables_metadata(df, columns, config_file, epsilon = 0.01):
    # df = df.replace('', np.nan)
    variables_metadata = []
    # we need to create a list of dict for columns' meta-data
    for col in columns:
        col_info = {
                "query": True,
                "type": "continuous",
                "name": col,
                "lower": df[col].min() - epsilon *  df[col].min(),
                "upper": df[col].max() + epsilon * df[col].max()
        }
        variables_metadata.append(col_info)
        json.dump(variables_metadata, open(config_file, 'w'))
    return variables_metadata

import matplotlib.pyplot as plt
def plot_error(pred_df, actual_df, col):
    """
    Plot the error.
    """
    actual=[x for x in actual_df.loc[:,col].values]
    pred=[x for x in pred_df.loc[:,col].values]

    plt.figure(figsize=(10,5))
    plt.plot(actual, label='actual', color='green')
    plt.plot(pred, label='pred', color='red')
    plt.legend()
    plt.show()