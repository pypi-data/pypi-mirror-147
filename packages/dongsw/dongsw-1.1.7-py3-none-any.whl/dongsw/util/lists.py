from ..extension import pandas as pd

def find_before(data, list1, num = 1):
    if isinstance(data, pd.Series):
        return data.apply(lambda x: find_before(x, list1, num))
    else:
        list1 = list(list1)
        index = list1.index(data)
        if index == 0:
            return None
        return list1[index - num]