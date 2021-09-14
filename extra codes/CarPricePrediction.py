#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import numpy as np


# In[2]:


df=pd.read_csv('car data.csv')


# In[3]:


df.shape


# In[4]:


df.head()


# In[5]:


print(df['Seller_Type'].unique())
print(df['Fuel_Type'].unique())
print(df['Transmission'].unique())
print(df['Owner'].unique())


# In[6]:


##check missing values
df.isnull().sum()


# In[7]:


df.describe()


# In[8]:


final_dataset=df[['Year','Selling_Price','Present_Price','Kms_Driven','Fuel_Type','Seller_Type','Transmission','Owner']]


# In[9]:


final_dataset.head()


# In[10]:


final_dataset['Current Year']=2020


# In[11]:


final_dataset.head()


# In[12]:


final_dataset['no_year']=final_dataset['Current Year']- final_dataset['Year']


# In[13]:


final_dataset.head()


# In[14]:


final_dataset.drop(['Year'],axis=1,inplace=True)


# In[16]:


final_dataset=pd.get_dummies(final_dataset,drop_first=True)


# In[17]:


final_dataset.head()


# In[18]:


final_dataset=final_dataset.drop(['Current Year'],axis=1)


# In[19]:


final_dataset.head()


# In[20]:


final_dataset.corr()


# In[21]:


import seaborn as sns


# In[22]:


sns.pairplot(final_dataset)


# In[24]:



import seaborn as sns
import matplotlib.pyplot as plt
#get correlations of each features in dataset
corrmat = df.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
#plot heat map
g=sns.heatmap(df[top_corr_features].corr(),annot=True,cmap="RdYlGn")


# In[25]:


X=final_dataset.iloc[:,1:]
y=final_dataset.iloc[:,0]


# In[26]:


X['Owner'].unique()


# In[27]:


X.head()


# In[28]:


y.head()


# In[29]:


### Feature Importance

from sklearn.ensemble import ExtraTreesRegressor
import matplotlib.pyplot as plt
model = ExtraTreesRegressor()
model.fit(X,y)


# In[30]:


print(model.feature_importances_)


# In[31]:


#plot graph of feature importances for better visualization
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(5).plot(kind='barh')
plt.show()


# In[32]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)


# In[33]:


from sklearn.ensemble import RandomForestRegressor


# In[34]:


regressor=RandomForestRegressor()


# In[37]:


n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
print(n_estimators)


# In[38]:


from sklearn.model_selection import RandomizedSearchCV


# In[39]:


#Randomized Search CV

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]
# max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10, 15, 100]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 5, 10]


# In[40]:


# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}

print(random_grid)


# In[41]:


# Use the random grid to search for best hyperparameters
# First create the base model to tune
rf = RandomForestRegressor()


# In[42]:


# Random search of parameters, using 3 fold cross validation, 
# search across 100 different combinations
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid,scoring='neg_mean_squared_error', n_iter = 10, cv = 5, verbose=2, random_state=42, n_jobs = 1)


# In[43]:


rf_random.fit(X_train,y_train)


# In[44]:


rf_random.best_params_


# In[45]:


rf_random.best_score_


# In[46]:


predictions=rf_random.predict(X_test)


# In[47]:


sns.distplot(y_test-predictions)


# In[48]:


plt.scatter(y_test,predictions)


# In[49]:


from sklearn import metrics


# In[50]:


print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))


# In[51]:


import pickle
# open a file, where you ant to store the data
file = open('random_forest_regression_model.pkl', 'wb')

# dump information to that file
pickle.dump(rf_random, file)


# In[ ]:




