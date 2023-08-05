from krakentren import *


pair = Coin("XXBTZEUR")

data = pair.get_ohlc_data("15")


add_ta(data,
       sma1={'indicator': 'sma', 'period': 3},
       sma2={'indicator': 'sma', 'period': 9},
       mfi={'indicator': 'mfi', 'period': 14},
       psl={'indicator': 'psl', 'period': 9},
       chop={'indicator': 'chop', 'period': 15},
       roc={'indicator': 'roc', 'period': 17},
       adl={'indicator': 'adl'},
       psar={'indicator': 'psar', 'af': 0.040, 'max_af': 0.40})

print(data)
