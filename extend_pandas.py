import pandas as pd
import numpy as np
from typing import Union, Optional, List, Callable


# create fake data
def create_fake_data() -> pd.DataFrame:
    dates = pd.date_range("2021.02.01", periods=3)
    df = pd.DataFrame({'date': dates})
    clients = ['Bridgewater Associates', 'Renaissance Technologies', 'Man Group', 'Millennium Mgmt.']
    df['clientName'] = [clients for _ in df.index]
    df = df.explode('clientName').reset_index(drop=True)
    mnemonics = [['bridgeuk', 'usbridge1'], ['renAIsig'], ['manthevol'], ['mlnmprtnrs', 'mlnmmgmt']]
    df['counterparty'] = mnemonics * 3
    df = df.explode('counterparty').reset_index(drop=True)
    ccy_pairs = ['EURUSD', 'USDJPY', 'AUDUSD']
    df['sym'] = [ccy_pairs for i in df.index]
    df = df.explode('sym').reset_index(drop=True)
    df['channel'] = [['NEO', 'FXI', 'DIGIVEGA'] for _ in df.index]
    df = df.explode('channel').reset_index(drop=True)
    np.random.seed(0)
    df['nOfFirmQuotes'] = np.random.randint(100, size=len(df))
    df['nOfTrades'] = np.random.randint(10, size=len(df))
    df['nOfTrades'] = df[['nOfFirmQuotes', 'nOfTrades']].min(1)
    return df


# Create the summarize
df_data = create_fake_data()


# make this a function and discard unit columns
# df = df_data.copy()
# df = df_data.query('sym == "EURUSD"').copy()
# df = df_data.query('clientName == "Bridgewater Associates"').copy()
# df = df_data.query('sym == "EURUSD"').query('clientName == "Bridgewater Associates"').query('channel == "FXI"')
# grouper: Optional['str'] = np.average
# by: Optional[Union[str, List[str]]] = None
# vars_agg: Optional[Union[str, List[str]]] = None
# value_name: Optional[str] = None
# omit_unique: Optional[bool] = True
def add_agg_by_groups(df, grouper: Optional[Callable] = sum, by: Optional[Union[str, List[str]]] = None,
                      vars_agg: Optional[Union[str, List[str]]] = None,
                      value_name: Optional[str] = None,
                      omit_unique: Optional[bool] = True) -> pd.DataFrame:

    if by is None:
        by = list(df.select_dtypes(include='object').columns)
    group_vars = by.copy()

    if vars_agg is None:
        vars_agg = list(df.select_dtypes(include='number').columns)

    if value_name is None:
        value_name = "z_" + grouper.__name__

    # create the frame of totals by aggregating on the first group
    df = df.groupby(by=by)[vars_agg].agg(grouper).reset_index()
    df_out = df.copy()

    # Add aggregates by groups
    remaining_vars = []
    while len(group_vars) > 1:
        remaining_vars.insert(0, group_vars.pop())
        df_loop = df.groupby(by=group_vars)[vars_agg].agg(grouper).reset_index()
        if omit_unique:
            if len(group_vars) > 1:
                unique_groups = df.groupby(group_vars[:-1])[group_vars[-1]].nunique().reset_index().rename(columns={group_vars[-1]: 'nUnique'})
                df_loop = df_loop.merge(unique_groups)
                df_loop = df_loop[df_loop.nUnique > 1].drop('nUnique', axis=1)
            else:
                if len(df_loop) <= 1:
                    continue
        if len(df_loop) > 0:
            df_out = df_out.append(df_loop).reset_index(drop=True)
            df_out[remaining_vars] = df_out[remaining_vars].fillna(value_name)

    # Add aggregates across all levels
    df_out = df_out.append(df[vars_agg].agg(grouper), ignore_index=True).reset_index(drop=True)
    df_out[by] = df_out[by].fillna(value_name)

    # Add index and sort
    df_out = df_out.set_index(by).sort_index()

    return df_out


# this should work
print(add_agg_by_groups(df_data).to_string())

# with only one group?
print(add_agg_by_groups(df_data.query('sym == "EURUSD"').query('clientName == "Bridgewater Associates"'),  grouper=np.average))
print(add_agg_by_groups(df_data.query('clientName == "Bridgewater Associates"'), grouper=np.average).to_string())


@pd.api.extensions.register_dataframe_accessor("fxo")
class FxoAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        validation = True
        if not validation:
            raise AttributeError("I will never raise anything.")

    def agg(self, grouper: Optional[Callable] = sum, by: Optional[Union[str, List[str]]] = None,
            vars_agg: Optional[Union[str, List[str]]] = None,
            value_name: Optional[str] = None,
            omit_unique: Optional[bool] = True) -> pd.DataFrame:
        if by is None:
            by = list(self._obj.select_dtypes(include='object').columns)
        group_vars = by.copy()

        if vars_agg is None:
            vars_agg = list(self._obj.select_dtypes(include='number').columns)

        if value_name is None:
            value_name = "z_" + grouper.__name__

        # create the frame of totals by aggregating on the first group
        df = self._obj.groupby(by=by)[vars_agg].agg(grouper).reset_index()
        df_out = df.copy()

        # Add aggregates by groups
        remaining_vars = []
        while len(group_vars) > 1:
            remaining_vars.insert(0, group_vars.pop())
            df_loop = self._obj.groupby(by=group_vars)[vars_agg].agg(grouper).reset_index()
            if omit_unique:
                if len(group_vars) > 1:
                    unique_groups = self._obj.groupby(group_vars[:-1])[group_vars[-1]].nunique().reset_index().rename(
                        columns={group_vars[-1]: 'nUnique'})
                    df_loop = df_loop.merge(unique_groups)
                    df_loop = df_loop[df_loop.nUnique > 1].drop('nUnique', axis=1)
                else:
                    if len(df_loop) <= 1:
                        continue
            if len(df_loop) > 0:
                df_out = df_out.append(df_loop).reset_index(drop=True)
                df_out[remaining_vars] = df_out[remaining_vars].fillna(value_name)

        # Add aggregates across all levels
        df_out = df_out.append(self._obj[vars_agg].agg(grouper), ignore_index=True).reset_index(drop=True)
        df_out[by] = df_out[by].fillna(value_name)

        # Add index and sort
        df_out = df_out.set_index(by).sort_index()

        return df_out


print(df_data.fxo.agg().to_string())


