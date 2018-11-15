# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import logging
import traceback


class concat_tuples_to_list():
    def __init__(self):
        pass

    # tuples = {tuple1, tuple2}
    # headers = {header1, header2}
    def concat_datasrcset(self,tuples, headers, condkey):
        result = {}
        try:
            if not tuples and not headers:
                result = {'errorcode':-1, 'errortext':'tuples or headers is not invalid'}
                return result
            header1 = headers['header1']
            header2 = headers['header2']

            if (condkey not in header1) and (condkey not in header2):
                result['errorcode'] = -1
                result['errortext'] = '%s is not in %s' % (condkey, headers)
                return result
            list1 = list(tuples['tuple1'])
            list2 = list(tuples['tuple2'])
            list1[:] = [list(t) for t in list1]
            list2[:] = [list(t) for t in list2]


            df1 = pd.DataFrame(list1, columns=header1)
            df2 = pd.DataFrame(list2, columns=header2)
            df3 = pd.merge(df1, df2, how='left', on=condkey)
            df3 = df3.where(df3.notnull(), None)
            train_data = np.array(df3)
            result['datasrcset'] = train_data.tolist()
            result['errorcode'] = 0
            return result
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            logging.error(result)
            return result