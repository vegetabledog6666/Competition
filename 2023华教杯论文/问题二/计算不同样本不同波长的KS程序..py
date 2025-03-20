import numpy as np
import pandas as pd

Ks=pd.read_excel("不同样本不同波长下R值.xlsx",index_col=[0])
Ks=(1-Ks**2)/(2*Ks)
Ks.to_excel("不同样本不同波长下KS值.xls")