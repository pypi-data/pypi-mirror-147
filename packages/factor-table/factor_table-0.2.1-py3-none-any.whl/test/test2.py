# coding=utf-8
import sys

import pandas as pd

sys.path.append('C:\\Users\\user\\Documents\\GitHub\\factor_table')

from factor_table.core import FactorTable

path = './stk_daily.h5'

# cik_ids= ['100025.OF','000645.OF']
with pd.HDFStore(path, mode='r') as f:
    print(f.keys())


def temp_load_data(path, key, stk='stklist', dt='trade_dt'):
    cp = pd.read_hdf(path, key)
    stklist = pd.read_hdf(path, stk)
    trade_dt = pd.read_hdf(path, dt)

    cp.index = pd.to_datetime(trade_dt.astype(str).values.ravel())
    cp.index.name = dt
    cp.columns = stklist.values.ravel()
    cp.columns.name = stk
    cp = cp.stack().reset_index()
    cp.columns = [dt, stk, key]
    return cp


if __name__ == '__main__':
    cp2 = temp_load_data(path, 'cp')
    mv_float = temp_load_data(path, 'mv_float')
    # cp2.info()

    ft = FactorTable()
    ft.add_factor('cp', cp2, cik_dt='trade_dt', cik_id='stklist', factor_names=['cp'], db_type='DF')
    ft.add_factor('mv_float', mv_float, cik_dt='trade_dt', cik_id='stklist', factor_names=['mv_float'], db_type='DF')
    print(dir(ft))



    fetched = ft.fetch(cik_dts=None, cik_ids=['688321.SH'], skip_cache=False, delay=False)
    # print(1)
    # ft.save('./cp.h5')
    # ft2 = FactorTable()
    #
    # ft2.load('./cp.h5', cik_cols=['trade_dt', 'stklist'])
    print(1)

    pass
