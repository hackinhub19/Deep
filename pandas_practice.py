import numpy as np
import pandas as pd
s=pd.Series([1,3,5,np.nan,6,8])
dates=pd.date_range('20140101',periods=6)
df=pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))
df2=pd.DataFrame({'A':1.,
                  'B':pd.Timestamp('20130201'),
                  'C':pd.Series(1,index=list(range(4)),dtype='float32'),
                  'D':np.array([3]*4,dtype='int32'),
                  'E':pd.Categorical(['test','train','test','train']),
                  'F':'foo'})
s1=pd.Series([1,2,3,4,5,6],index=pd.date_range('20140101',periods=6))
s=pd.Series([1,3,5,np.nan,6,8],index=dates).shift(2)
s2=pd.Series(np.random.randint(0,7,size=10))
