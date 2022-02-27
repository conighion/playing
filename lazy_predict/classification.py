from lazypredict.Supervised import LazyClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# load data and split sample
# if you want to view them as data.frame; load_breast_cancer(as_frame=True).frame
data = load_breast_cancer()
# array of 569 observations with 30 features each. Features are computed from a digitized image of a  fine needle
# aspirate (FNA) of a breast mass. They describe characteristics of the cell nuclei present in the image.
X = data.data
# Response is the diagnosis (malignant vs benign); 212 - Malignant (0), 357 - Benign (1)
y = data.target

# Split to the train and test sets. We choose to split 50% of the obs for training and 50 for testing.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=123)

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

# Get a feeling of which variables matter
clf_log_reg_coefficients = (np.std(X, 0) * clf_log_reg.coef_)[0]
df_log_reg_coefficients = pd.DataFrame([x.replace(" ", "_") for x in data.feature_names], columns=['feature'])
df_log_reg_coefficients['est'] = clf_log_reg.coef_[0]
df_log_reg_coefficients['estStd'] = (np.std(X, 0) * clf_log_reg.coef_)[0]
print(df_log_reg_coefficients.sort_values('estStd', ascending=False).to_string())



