from sklearn.svm import SVR
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


# Make predictions using the testing set
def predict_using_model(model, X_test):
    return model.predict(X_test)


def linear_regression_model(X_train, Y_train):
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(X_train, Y_train)

    return regr


def svr_model(X_train, Y_train):
    svr_rbf = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
    svr_rbf.fit(X_train, Y_train)
    return svr_rbf


def svr_lin_model(X_train, Y_train):
    svr_lin = SVR(kernel='linear', C=100, gamma='auto')
    svr_lin.fit(X_train, Y_train)
    return svr_lin


def svr_poly_model(X_train, Y_train):
    svr_poly = SVR(kernel='poly', C=100, gamma='auto', degree=3, epsilon=.1, coef0=1)
    svr_poly.fit(X_train, Y_train)
    return svr_poly


def create_model(X, y):
    model = SVR(kernel='poly')
    model.fit(X, y)
    return model