brands = 2
#brands = 9
outlets = 1000

#change the names as brand_budget0,....
constraints = { 
        'Brand0Budget': 2800000,
        'Brand1Budget': 2700000}


import os
from pulp import * 
import pandas as pd
import numpy as np
import time

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
