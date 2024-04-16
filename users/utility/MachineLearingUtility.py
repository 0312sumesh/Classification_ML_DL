from django.conf import settings
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

path = os.path.join(settings.MEDIA_ROOT, "Dentals.csv")
df = pd.read_csv(path)
df = df[['tooth', 'gene_ace', 'gene_smoc1', 'gene_pou3f3', 'gene_wnt2']]
df['tooth'] = df['tooth'].map(
    {'lower': 1, 'upper': 0})
#print(df.head())
X = df.iloc[:, 1:].values
#print('*'*100, X)
y = df.iloc[:, :1].values
#print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)


def process_svm():
    from sklearn.svm import SVC
    svm_model = SVC()
    svm_model.fit(X_train,y_train)
    y_pred = svm_model.predict(X_test)
    svm_accuracy = accuracy_score(y_test, y_pred)
    print("svm accuracy :", svm_accuracy)
    from sklearn.neighbors import KNeighborsClassifier
    knn_model = KNeighborsClassifier()
    knn_model.fit(X_train,y_train)
    y_pred = knn_model.predict(X_test)
    knn_accuracy = accuracy_score(y_test, y_pred)
    print("Knn accuracy :", knn_accuracy)

    from keras.models import Sequential
    from keras.layers import Dense
    classifier = Sequential()
    classifier.add(Dense(output_dim=3, init='uniform', activation='relu', input_dim=4))
    classifier.add(Dense(output_dim=3, init='uniform', activation='relu'))
    classifier.add(Dense(output_dim=1, init='uniform', activation='sigmoid'))
    classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    print(classifier.summary())
    classifier.fit(X_train, y_train, batch_size=10, nb_epoch=100)

    y_pred = classifier.predict(X_test)
    y_pred = (y_pred > 0.5)
    ann_accuracy = accuracy_score(y_test, y_pred)
    print("Ann accuracy :",ann_accuracy)

    return svm_accuracy, knn_accuracy, ann_accuracy


