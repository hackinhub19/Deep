from tkinter import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from xgboost import XGBRegressor

business=pd.read_csv(r'C:\Users\DEEP\machine learning\hackathon\FnB_hackathon_Pi\FnB_hackathon_Pi.csv')

white_business=business[business['Company']=='white walkers']
white_business.drop(columns=['Company'],inplace=True)


X=white_business[list(white_business.columns)[2:-3]]
X.drop(columns=['Area 3','Product Category 2','Outlet Name'],inplace=True)

l=[X[i].unique() for i in X.columns]

le = preprocessing.LabelEncoder()

for x in X.columns:
    X[x]=le.fit_transform(X[x])

m=[X[i].unique() for i in X.columns]

d=[dict(zip(l[i],m[i])) for i in range(len(X.columns))]

y=white_business['Units sold']

X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=0)

xgreg=XGBRegressor().fit(X_train,y_train)
xgreg_score=xgreg.score(X_test,y_test)

threshold=y_train.mean()


my_window=Tk()
my_window.title('FEASIBILITY ANALYSIS')
my_window.configure(width=500,height=500,background='yellow')
my_window.geometry('600x500+400+100')

def get_input():
    state=entry1.get()
    city=entry2.get()
    locality=entry3.get()
    outlet_type=entry4.get()
    product_category=entry5.get()
    product=entry6.get()
    
    r=pd.DataFrame({'Area 1':[d[0][state]],'Area 2':d[1][city],'Area 3 Classification':d[2][locality],'Outlet Type':d[3][outlet_type],'Product Category 1':d[4][product_category],'Product':d[5][product]},columns=['Area 1','Area 2','Area 3 Classification','Outlet Type','Product Category 1','Product'])
    predicted_revenue=xgreg.predict(r)
    
    label7=Label(my_window,font='Verdana 10',width=50,borderwidth=1,relief='ridge',bg='pink')
    
    if predicted_revenue>threshold:
        label7['text']=('feasible with revenue {}'.format(predicted_revenue))

    else:
        label7['text']=('not feasible with revenue {}'.format(predicted_revenue))

    label7.grid(row=7,column=0)
    
label1=Label(my_window,text='Enter State',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry1=Entry(my_window)
label2=Label(my_window,text='Enter City',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry2=Entry(my_window)
label3=Label(my_window,text='Enter Locality',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry3=Entry(my_window)
label4=Label(my_window,text='Outlet Type',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry4=Entry(my_window)
label5=Label(my_window,text='Product Category',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry5=Entry(my_window)
label6=Label(my_window,text='Product',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry6=Entry(my_window)

button1=Button(my_window,text='click to get result',command=get_input,bg='blue',fg='white',font='Times',borderwidth=1,relief='solid')

label1.grid(row=0,column=0)
entry1.grid(row=0,column=1)
label2.grid(row=1,column=0)
entry2.grid(row=1,column=1)
label3.grid(row=2,column=0)
entry3.grid(row=2,column=1)
label4.grid(row=3,column=0)
entry4.grid(row=3,column=1)
label5.grid(row=4,column=0)
entry5.grid(row=4,column=1)
label6.grid(row=5,column=0)
entry6.grid(row=5,column=1)

button1.grid(row=6,column=0)

my_window.mainloop()

#the north
#riverrun
#ser
#house frey
#korean
#white cabbage