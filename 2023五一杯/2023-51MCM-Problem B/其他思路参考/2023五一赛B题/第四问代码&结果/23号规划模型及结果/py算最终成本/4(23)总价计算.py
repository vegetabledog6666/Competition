#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[4]:


for i in range(1,82):
    pd.DataFrame([]).to_excel(r"C:\Users\MATH_MGD\Desktop\23\{}.xlsx".format(i))


# In[9]:


data = pd.read_excel(r"C:\Users\MATH_MGD\Desktop\23\{}.xlsx".format(1),index_col=0).values.copy()
for i in range(2,82):
    data+=pd.read_excel(r"C:\Users\MATH_MGD\Desktop\23\{}.xlsx".format(i),index_col=0).values.copy()


# In[11]:


pd.DataFrame(data).to_excel(r"C:\Users\MATH_MGD\Desktop\23\{}.xlsx".format("总"))


# In[17]:


R = pd.read_excel(r"C:\Users\MATH_MGD\Desktop\23\额定装货量R.xlsx",index_col=0).values
F = pd.read_excel(r"C:\Users\MATH_MGD\Desktop\23\固定成本F.xlsx",index_col=0).values


# In[19]:


np.sum((1+(data/R)**3)*F)


# In[ ]:




