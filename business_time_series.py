import pandas as pd

hack=pd.read_csv(r'C:\Users\DEEP\machine learning\hackathon\FnB_hackathon_Pi\FnB_hackathon_Pi.csv')
white_company=hack[hack['Company']=='white walkers']
men_company=hack[hack['Company']=='men']

hack_time=hack.copy()

to_replace=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
replace_with=['2019-01-01','2019-02-01','2019-03-01','2019-04-01','2019-05-01','2019-06-01'
              ,'2019-07-01','2019-08-01','2019-09-01','2019-10-01','2019-11-01','2019-12-01']

hack_time['MONTH'].replace(to_replace=to_replace,value=replace_with,inplace=True)

hack_time['MONTH']= pd.to_datetime(hack_time['MONTH'],format="%Y%m%d")
