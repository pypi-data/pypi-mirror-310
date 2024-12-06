
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from sklearn.model_selection import train_test_split

def correlation(df_temp):
    correlation_matirx = df_temp.corr()
    target_correlation = correlation_matirx['Price'].abs()
    selected_features = target_correlation[target_correlation > 0.1].index
    X = df_temp[selected_features]
    X.drop('Price', axis=1, inplace=True)
    X.fillna(0, inplace=True)
    y = df_temp['Price']

def linear_r(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    linear = LinearRegression()
    linear.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = linear.predict(X_test)

    print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
    print('Mean Absolute Error:', mean_absolute_error(y_test, y_pred))
    print('R^2:', r2_score(y_test, y_pred))

    # accuracy
    print(linear.score(X_test, y_test))

    logistic = LogisticRegression()
    logistic.fit(X_train, y_train)


    print(logistic.score(X_test,y_test))
    
def classificaiton():
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the classifiers
    rf_model = RandomForestClassifier(random_state=42)
    svm_model = SVC(random_state=42)
    dt_model = DecisionTreeClassifier(random_state=42)


    # Train each model
    rf_model.fit(X_train, y_train)
    svm_model.fit(X_train, y_train)
    dt_model.fit(X_train, y_train)

    # Make predictions
    rf_pred = rf_model.predict(X_test)
    svm_pred = svm_model.predict(X_test)
    dt_pred = dt_model.predict(X_test)

    # Evaluate each model
    rf_accuracy = accuracy_score(y_test, rf_pred)
    svm_accuracy = accuracy_score(y_test, svm_pred)
    dt_accuracy = accuracy_score(y_test, dt_pred)

    # Print results
    print("Random Forest Accuracy:", rf_accuracy)
    print("SVM Accuracy:", svm_accuracy)
    print("Decision Tree Accuracy:", dt_accuracy)

    print("\nRandom Forest Classification Report:\n", classification_report(y_test, rf_pred))
    print("SVM Classification Report:\n", classification_report(y_test, svm_pred))
    print("Decision Tree Classification Report:\n", classification_report(y_test, dt_pred))

    print("\nRandom Forest Confusion Matrix:\n", confusion_matrix(y_test, rf_pred))
    print("SVM Confusion Matrix:\n", confusion_matrix(y_test, svm_pred))
    print("Decision Tree Confusion Matrix:\n", confusion_matrix(y_test, dt_pred))