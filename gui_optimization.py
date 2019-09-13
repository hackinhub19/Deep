from tkinter import *
import os
from pulp import * 
import pandas as pd
import numpy as np
import time

def get_input():
    brands=int(entry1.get())
    outlets=int(entry2.get())
    brand0budget=int(entry3.get())
    brand1budget=int(entry4.get())
    constraints = { 
        'Brand0Budget': brand0budget,
        'Brand1Budget': brand1budget}

    
    #os.chdir('C://Users//pi//Desktop')
    df = pd.read_csv('F:\machine learning\dataset\optimization_1000.csv')
    df = df.iloc[:,0:5]
    df.columns = ['ol', 'DEP-Brand0','DEP-Brand1', 'PromisedPayoutPerCase-Brand0','PromisedPayoutPerCase-Brand1'   ]
    """dep_brand0 = df['DEP-Brand0'].to_list()
    dep_brand1 = df['DEP-Brand1'].to_list()
    promised_payoutpc0 = df['PromisedPayoutPerCase-Brand0'].to_list()
    promised_payoutpc1 = df['PromisedPayoutPerCase-Brand1'].to_list()"""
    #for i in df.columns:
    #    i = list(df[i])
    
    dep_brand0 = list(df['DEP-Brand0'])
    dep_brand1 = list(df['DEP-Brand1'])
    promised_payoutpc0 = list(df['PromisedPayoutPerCase-Brand0'])
    promised_payoutpc1 = list(df['PromisedPayoutPerCase-Brand1'])
    
    #for i in df.columns:
    #    promised_payout
    promised_payout_0 = sum([dep_brand0[i]*promised_payoutpc0[i] for i in range(outlets)])
    promised_payout_1 = sum([dep_brand1[i]*promised_payoutpc1[i] for i in range(outlets)])
    #brands = ['brand_budget'+str(i) for i in range(1000)]
    #for i in brands:
    #    i = constraints[i]
    brand_budget_0 = constraints['Brand0Budget']
    brand_budget_1 = constraints['Brand1Budget']
    
    #for j in df.columns:
    #    outlet_wise_payout = list([j[i]*promised_payoutpc0[i] + \
    #                      j[i]*promised_payoutpc1[i] for i in range(outlets)])
    outlet_wise_payout = list([dep_brand0[i]*promised_payoutpc0[i] + \
                          dep_brand1[i]*promised_payoutpc1[i] for i in range(outlets)])
    x=[]
    for outlet in range(outlets):
        for brand in range(brands):
            x.append(LpVariable("payoutPerCase:Brand:{},Outlet:{}".format(brand, outlet), lowBound = 0, cat=LpContinuous))
    
    
    x = np.array(x).reshape(outlets,brands).tolist()
    
    #excess = (brand_budget_0 - sum([x[i][0]*dep_brand0[i] for i in range(outlets)])) +\
    #          brand_budget_1 - sum([x[i][1]*dep_brand1[i] for i in range(outlets)])
    excess1 = brand_budget_0 - sum([x[i][0]*dep_brand0[i] for i in range(outlets)]) 
    excess2 = brand_budget_1 - sum([x[i][1]*dep_brand1[i] for i in range(outlets)])
    excess = excess1 + excess2
    ol_payouts = [x[i][0]*dep_brand0[i]+x[i][1]*dep_brand1[i] for i in range(outlets)]
    outlet_payout_diff = [outlet_wise_payout[i] - ol_payouts[i] for i in range(outlets)]
    in_budget = (brand_budget_0 + brand_budget_1) > sum(outlet_wise_payout)
    
    if in_budget:
                   
       prob = LpProblem("OutletPayout",pulp.LpMaximize)
    
    if not in_budget:
        prob = LpProblem("OutletPayout",pulp.LpMinimize)
        
    prob += excess
    
    if in_budget:
        prob+= excess1>=0
        prob+= excess2>=0
        prob+= excess1==excess2
        
    if not in_budget:
        prob+= excess1 <=0
        prob+= excess2 <=0
        prob+= excess1 == excess2
    
    
    for i in range(outlets):
        prob+= outlet_payout_diff[i] == 0
    #prob+= excess1 >= 0
    #prob+= excess2 >= 0
    #prob+= sum([x[i][0]*dep_brand0[i] for i in range(outlets)]) <= brand_budget_0
    #prob+= sum([x[i][1]*dep_brand1[i] for i in range(outlets)]) <= brand_budget_1
    start = time.time()
    prob.solve()
    end = time.time()
    te_opt_1000 = end - start    
    print("The time elapsed for optimizing 10 outlet payouts is", te_opt_1000)
    
    #for v in prob.variables():
    #    print(v, v.varValue)
    
    for i in range(outlets):
        if x[i][0].varValue==None:
            x[i][0].varValue=0
            
    for i in range(outlets):
        if x[i][1].varValue==None:
            x[i][1].varValue=0        
            
    opt_1000_obj = value(prob.objective)
    print(opt_1000_obj)
    totalrevisedpayout_brand0 = sum(x[i][0].varValue*dep_brand0[i] for i in range(outlets))
    totalrevisedpayout_brand1 = sum(x[i][1].varValue*dep_brand1[i] for i in range(outlets))
    
    revised_table=pd.DataFrame({'Brand 1 Promised Payout':promised_payoutpc0,'Brand 2 Promised Payout':promised_payoutpc1,'Brand 1 Revised Payout':[x[i][0].varValue for i in range(outlets)],'Brand 2 Revised Payout':[x[i][1].varValue for i in range(outlets)]})
    revised_table.to_csv(r'Desktop\revised_payouts.csv')
    
    label5=Label(my_window,font='Verdana 10',width=50,borderwidth=1,relief='ridge',bg='yellow')
    label5['text']=('total revised payout of first brand :{}\ntotal revised payout of second brand :{}'.format(totalrevisedpayout_brand0,totalrevisedpayout_brand1))
    label5.grid(row=7,column=0)
     
    label6=Label(my_window,font='Verdana 10',width=50,borderwidth=1,relief='ridge',bg='pink')
    label6['text']=('Revised payouts in table format are saved on Destop')
    label6.grid(row=11,column=0)
    
my_window=Tk()
my_window.title('PAYOUT OPTIMIZATION')
my_window.configure(width=500,height=500,background='green')
my_window.geometry('600x500+400+100')
label1=Label(my_window,text='enter number of brands:',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry1=Entry(my_window)
label2=Label(my_window,text='enter number of outlets:',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry2=Entry(my_window)
button1=Button(my_window,text='click to get result',command=get_input,bg='blue',fg='white',font='Times',borderwidth=1,relief='solid')
label3=Label(my_window,text='enter budget for brand 1:',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry3=Entry(my_window)
label4=Label(my_window,text='enter budget for brand 2:',font='Verdana',width=30,borderwidth=1,relief='ridge')
entry4=Entry(my_window)

label1.grid(row=0,column=0)
entry1.grid(row=0,column=1)
label2.grid(row=1,column=0)
entry2.grid(row=1,column=1)
label3.grid(row=2,column=0)
entry3.grid(row=2,column=1)
label4.grid(row=3,column=0)
entry4.grid(row=3,column=1)
button1.grid(row=4,column=0)


my_window.mainloop()
