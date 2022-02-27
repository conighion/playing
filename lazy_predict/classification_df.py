import pandas as pd
import numpy as np
from lazypredict.Supervised import LazyClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# load data and split sample
# if you want to view them as data.frame; load_breast_cancer(as_frame=True).frame
data = load_breast_cancer(as_frame=True)
df_data = data.frame
df_data.columns = [x.replace(" ", "_") for x in df_data.columns]  # fix column names

# Split to the train and test sets. We choose to split 50% of the obs for training and 50 for testing.
data_train, data_test = train_test_split(df_data, test_size=0.5, random_state=123)
X, y = data.frame.loc[:, df_data.columns != 'target'], df_data.loc[:, data.frame.columns == 'target']
X_train, y_train = data_train.loc[:, data_train.columns != 'target'], data_train.loc[:, data_train.columns == 'target']
X_test, y_test = data_test.loc[:, data_train.columns != 'target'], data_test.loc[:, data_train.columns == 'target']


# Specify the classifier (clf)
clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
models, predictions = clf.fit(X_train, X_test, y_train, y_test)

# I know from the horse racing that Logistic Regression performs well.
clf_log_reg = LogisticRegression(random_state=123)
fit_train_set = True
clf_log_reg.fit(X_train, y_train) if fit_train_set else clf_log_reg.fit(X, y)
clf_log_reg.score(X_test, y_test) if fit_train_set else clf_log_reg.score(X, y)

# Another evaluation tool is the confusion matrix
confusion_matrix(y_test, clf_log_reg.predict(X_test))
print(classification_report(y_test, clf_log_reg.predict(X_test)))

# Get a feeling of which variables matter
df_vars = pd.DataFrame(df_data.columns, columns=['feature']).query('feature != "target"')
df_vars['est'] = clf_log_reg.coef_[0]
df_vars['estStd'] = (np.std(X, 0)[0] * clf_log_reg.coef_)[0]
df_vars['estStdAbs'] = np.abs((np.std(X, 0)[0] * clf_log_reg.coef_)[0])
features_important = df_vars.sort_values('estStdAbs', ascending=False).iloc[:10].feature.to_list()

# Repeat training
features_important = df_vars.sort_values('estStdAbs', ascending=False).iloc[:2].feature.to_list()
df_data = data.frame
df_data.columns = [x.replace(" ", "_") for x in df_data.columns]  # fix column names
df_data = df_data[features_important + ['target']]
data_train, data_test = train_test_split(df_data, test_size=0.5, random_state=123)
X, y = df_data.loc[:, df_data.columns != 'target'], df_data.loc[:, df_data.columns == 'target']
X_train, y_train = data_train.loc[:, data_train.columns != 'target'], data_train.loc[:, data_train.columns == 'target']
X_test, y_test = data_test.loc[:, data_train.columns != 'target'], data_test.loc[:, data_train.columns == 'target']

clf_log_reg_small = LogisticRegression(random_state=123)
fit_train_set = True
clf_log_reg_small.fit(X_train, y_train) if fit_train_set else clf_log_reg.fit(X, y)
clf_log_reg_small.score(X_test, y_test) if fit_train_set else clf_log_reg.score(X, y)

df_vars_small = pd.DataFrame(df_data.columns, columns=['feature']).query('feature != "target"')
df_vars_small['est'] = clf_log_reg_small.coef_[0]
df_vars_small['estStd'] = (np.std(X, 0)[0] * clf_log_reg_small.coef_)[0]
df_vars_small['estStdAbs'] = np.abs((np.std(X, 0)[0] * clf_log_reg_small.coef_)[0])
features_important = df_vars_small.sort_values('estStdAbs', ascending=False).iloc[:10].feature.to_list()


# Pot for the single variable model -> offering prediction equal to 89%
# Retrieve the model parameters.
b = clf_log_reg_small.intercept_[0]
w1, w2 = clf_log_reg_small.coef_.T
# Calculate the intercept and gradient of the decision boundary.
c = -b/w2
m = -w1/w2

# Plot the data and the classification with the decision boundary.
x_min, x_max = df_data.mean_radius.min(), df_data.mean_radius.max()
y_min, y_max = df_data.worst_radius.min(), df_data.worst_radius.max()
xd = np.array([x_min, x_max])
yd = m*xd + c
plt.plot(xd, yd, 'k', lw=1, ls='--')
plt.fill_between(xd, yd, y_min, color='tab:blue', alpha=0.2)
plt.fill_between(xd, yd, y_max, color='tab:orange', alpha=0.2)


plt.scatter(df_data.query('target == 0').mean_radius.to_list(), df_data.query('target == 0').worst_radius.to_list(),
            s=8, alpha=0.5)
plt.scatter(df_data.query('target == 1').mean_radius.to_list(), df_data.query('target == 1').worst_radius.to_list(),
            s=8, alpha=0.5)
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.ylabel('Worst Radius ' + r'$(x_2)$')
plt.xlabel('Mean Radius ' + r'$(x_1)$')

plt.show()

# Let's if there are differences in models for the small one
features_important = df_vars.sort_values('estStdAbs', ascending=False).iloc[:2].feature.to_list()
df_data = data.frame
df_data.columns = [x.replace(" ", "_") for x in df_data.columns]  # fix column names
df_data = df_data[features_important + ['target']]
data_train, data_test = train_test_split(df_data, test_size=0.5, random_state=123)
X, y = df_data.loc[:, df_data.columns != 'target'], df_data.loc[:, df_data.columns == 'target']
X_train, y_train = data_train.loc[:, data_train.columns != 'target'], data_train.loc[:, data_train.columns == 'target']
X_test, y_test = data_test.loc[:, data_train.columns != 'target'], data_test.loc[:, data_train.columns == 'target']
clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
models, predictions = clf.fit(X_train, X_test, y_train, y_test)
print(models.to_string())


