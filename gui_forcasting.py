from tkinter import *
import pandas as pd
from fbprophet import Prophet

hack=pd.read_csv(r'F:\machine learning\dataset\business.csv')

white_company=hack[hack['Company']=='white walkers']
men_company=hack[hack['Company']=='men']

white_group=white_company.groupby(['Outlet Name','Product'])
men_group=men_company.groupby(['Outlet Name','Product'])

d=[]
v=[]

def func(g):
    v.append((g['Outlet Name'].unique()[0],g['Product'].unique()[0]))
    df1=pd.DataFrame(g.groupby(['MONTH'])['Units sold'].agg('sum'))
    df2=pd.DataFrame([0]*12,index=['2019-01-01','2019-01-02','2019-01-03','2019-01-04',
                     '2019-01-05','2019-01-06','2019-01-07','2019-01-08','2019-01-09'
                     ,'2019-01-10','2019-01-11','2019-01-12'],columns=['Units sold'])
    for i in df2.index:
        for j in df1.index:
            if i==j:
                df2['Units sold']=df1['Units sold']
    df2['date'] = pd.to_datetime(df2.index)
    df2.rename(columns={'date':'ds','Units sold':'y'},inplace=True)
    d.append(df2)
    
white_group.apply(func)
outlet_product_units=list(zip(v[1:],d[1:]))

final=[]

def remove_nan(f):
    if f[1]['y'].count()==12:
        final.append(f)

a=list(map(remove_nan,outlet_product_units))
#m.fit(outlet_product_units[0][1])
use=final[:10]
name=[x[0] for x in final[:10]]
#forecast = m.predict(future)
result=[]
models=[]
#m.plot(forecast)

def auto_calc(f):
    m = Prophet(weekly_seasonality=False,yearly_seasonality=False,daily_seasonality=False)
    m.add_seasonality('self_define_cycle',period=30.5,fourier_order=8,prior_scale=0.02)
    m.fit(f)
    future = m.make_future_dataframe(periods=1)
    forcast=m.predict(future)
    result.append(forcast[['ds','yhat','yhat_lower','yhat_upper']])
    models.append(m)


my_window=Tk()
my_window.title('SALES FORCASTING')
my_window.configure(width=500,height=500,background='yellow')
my_window.geometry('600x500+400+100')

label1=Label(my_window,text='enter the outlet name',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry1=Entry(my_window)
label2=Label(my_window,text='enter the product name',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry2=Entry(my_window)

def get_input():
    outlet_name=entry1.get()
    product_name=entry2.get()
    
    
button1=Button(my_window,text='click to get result',command=get_input,bg='blue',fg='white',font='Times',borderwidth=1,relief='solid')
    
label1.grid(row=0,column=0)
entry1.grid(row=0,column=1)
label2.grid(row=1,column=0)
entry2.grid(row=1,column=1)
button1.grid(row=2,column=0)

my_window.mainloop()