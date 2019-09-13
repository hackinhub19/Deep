import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from xgboost import XGBRegressor

business=pd.read_csv(r'C:\Users\DEEP\machine learning\hackathon\FnB_hackathon_Pi\FnB_hackathon_Pi.csv')

white_business=business[business['Company']=='white walkers']
white_business.drop(columns=['Company'],inplace=True)


X=white_business[list(white_business.columns)[2:-3]]
X.drop(columns=['Area 3','Product Category 2','Outlet Name'],inplace=True)

le = preprocessing.LabelEncoder()

for x in X.columns:
    X[x]=le.fit_transform(X[x])

y=white_business['Units sold']

X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=0)

xgreg=XGBRegressor().fit(X_train,y_train)
xgreg_score=xgreg.score(X_test,y_test)

predicted_revenue=xgreg.predict(pd.DataFrame(X_test.iloc[0]).T)

threshold=y_train.mean()

if predicted_revenue>threshold:
    print('feasible with monthly revenue {}'.format(predicted_revenue))

else:
    print('not feasible with month revenue {}'.format(predicted_revenue))    