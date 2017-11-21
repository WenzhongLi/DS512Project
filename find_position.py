# coding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV

def rearrange_column(df):
	"""rearrrange column so that testing data is listed in the same order with training data"""
	col = ['Aggression', 'Crossing', 'Curve', 'Dribbling', 'Finishing',
								 'Free kick accuracy', 'Heading accuracy', 'Long shots', 'Penalties', 'Shot power',
								 'Volleys',
								 'Short passing', 'Long passing',
								 'Interceptions', 'Marking', 'Sliding tackle', 'Standing tackle',
								 'Strength', 'Vision', 'Acceleration', 'Agility',
								 'Reactions', 'Stamina', 'Balance', 'Ball control', 'Composure', 'Jumping',
								 'Sprint speed', 'Positioning']
	df = df[col]
	return df

# get_ipython().magic('matplotlib inline')
df = pd.read_csv('CompleteDataset.csv')
df.head()
df.columns

# Gather only columns that we need for this analysis purpose:
# attack attribute first, then defence, then mixed
columns_needed_rearranged = ['Aggression','Crossing', 'Curve', 'Dribbling', 'Finishing',
       'Free kick accuracy', 'Heading accuracy', 'Long shots','Penalties', 'Shot power', 'Volleys', 
       'Short passing', 'Long passing',
       'Interceptions', 'Marking', 'Sliding tackle', 'Standing tackle',
       'Strength', 'Vision', 'Acceleration', 'Agility', 
       'Reactions', 'Stamina', 'Balance', 'Ball control','Composure','Jumping', 
       'Sprint speed', 'Positioning','Preferred Positions']

df = df[columns_needed_rearranged]
df.head()

# We don't want to classify GK because it will be too obvious:
df['Preferred Positions'] = df['Preferred Positions'].str.strip()
df = df[df['Preferred Positions'] != 'GK']
df.head()

# Check any missing data:
df.isnull().values.any()

# All possible outcome for preferred position:
p = df['Preferred Positions'].str.split().apply(lambda x: x[0]).unique()
p

# Handle players with multiple preferred positions: duplicate a set of data for each

# copy a structure
df_new = df.copy()
df_new.drop(df_new.index, inplace=True)

for i in p:
    df_temp = df[df['Preferred Positions'].str.contains(i)]
    df_temp['Preferred Positions'] = i
    df_new = df_new.append(df_temp, ignore_index=True)
    
df_new.iloc[::500, :]
            

# Some of the attributes have '+/-' sign, let's perform the calculation rather than keeping them as string:
cols = [col for col in df_new.columns if col not in ['Preferred Positions']]

for i in cols:
    df_new[i] = df_new[i].apply(lambda x: eval(x) if isinstance(x,str) else x)

df_new.iloc[::500, :]
df_new_normalized_all = df_new.copy()
mapping_all = {'ST': 0, 'RW': 1, 'LW': 2, 'RM': 3, 'CM': 4, 'LM': 5, 'CAM': 6, 'CF': 7, 'CDM': 8, 'CB': 9, 'LB': 10, 'RB': 11, 'RWB': 12, 'LWB': 13}

# mapping positions from string to int
df_new_normalized_all = df_new_normalized_all.replace({'Preferred Positions': mapping_all})
df_new_normalized_all.iloc[::1000,]


# Fit the model:
X_train_all, X_test_all, y_train_all, y_test_all = train_test_split(df_new_normalized_all.iloc[:,:-1], df_new_normalized_all.iloc[:,-1],test_size=0.05, random_state=0)

print('X train shape: {}'.format(X_train_all.shape))
print('X test shape: {}'.format(X_test_all.shape))
print('y train shape: {}'.format(y_train_all.shape))
print('y test shape: {}'.format(y_test_all.shape))


clf_knn = KNeighborsClassifier(n_neighbors=150)
clf_knn.fit(X_train_all, y_train_all)
print(clf_knn.score(X_test_all, y_test_all))

# 这是C罗的数据
test_case = pd.DataFrame({'Aggression':[63],'Crossing':[85], 'Curve':[81], 'Dribbling':[91], \
							 'Finishing':[94],'Free kick accuracy':[76], 'Heading accuracy':[88], \
							 'Long shots':[92],'Penalties':[85], 'Shot power':[94], 'Volleys':[88], \
							 'Short passing':[83], 'Long passing':[77],'Interceptions':[29], \
							 'Marking':[22], 'Sliding tackle':[23], 'Standing tackle':[31], \
							 'Strength':[80], 'Vision':[85], 'Acceleration':[89], 'Agility':[89], \
							 'Reactions':[96], 'Stamina':[92], 'Balance':[63], 'Ball control':[93], \
							 'Composure':[95],'Jumping':[95],'Sprint speed':[91], 'Positioning':[95]},dtype=int)

# 这理论上是一个CB，因为铲球很高，身体很壮
# test_case = pd.DataFrame({'Aggression':[20],'Crossing':[20], 'Curve':[20], 'Dribbling':[20], \
# 							 'Finishing':[20],'Free kick accuracy':[20], 'Heading accuracy':[88], \
# 							 'Long shots':[20],'Penalties':[20], 'Shot power':[70], 'Volleys':[88], \
# 							 'Short passing':[20], 'Long passing':[20],'Interceptions':[29], \
# 							 'Marking':[99], 'Sliding tackle':[99], 'Standing tackle':[99], \
# 							 'Strength':[95], 'Vision':[85], 'Acceleration':[80], 'Agility':[75], \
# 							 'Reactions':[80], 'Stamina':[85], 'Balance':[90], 'Ball control':[70], \
# 							 'Composure':[70],'Jumping':[95],'Sprint speed':[91], 'Positioning':[95]},dtype=int)

test_case = rearrange_column(test_case)

# 输出依次是ST、RW、LW、RM、CM、LM、CAM、CF、CDM、CB、LB、RB、RWB、LWB
# 其中，RWLW是边锋，ST/CF是前锋，M是中场，B是后卫，LR是左右边路
clf_knn.predict(test_case)
print(clf_knn.predict_proba(test_case))