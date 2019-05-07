
import matplotlib.pyplot as plt


def plot_data2(sorted_df, title):
    plt.plot(sorted_df.Datatime, sorted_df.Mean, 'm')
    plt.plot(sorted_df.Datatime, sorted_df.NASA, 'g')
    plt.plot(sorted_df.Datatime, sorted_df.Bootstrap, 'b')
    plt.ylabel('ice conc')
    plt.xlabel('date')
    plt.xticks(rotation=20)
    plt.title(title)
    plt.legend(['Mean', 'NASA', 'Bootstrap'], loc='upper right')
    plt.savefig('../plots/' + title + '.png', dpi=100)
    plt.show()


def plot_histogram(sorted_df, title):
    plt.hist(sorted_df.Mean, density=1, facecolor='m', alpha=0.75)
    plt.title(title)
    plt.grid(True)
    plt.savefig('../plots/' + title + '.png', dpi=100)
    plt.show()


def plot_model(model, X_test, Y_test, Y_pred):
    # # The coefficients
    # print('Coefficients: \n', model.coef_)
    # # The mean squared error
    # print("Mean squared error: %.2"
    #       % mean_squared_error(Y_test, diabetes_y_pred))
    # # Explained variance score: 1 is perfect prediction
    # print('Variance score: %.2f' % r2_score(Y_test, diabetes_y_pred))

    # Plot outputs
    plt.scatter(X_test, Y_test, color='black')
    plt.plot(X_test, Y_pred, color='blue', linewidth=3)

    # plt.xticks(())
    # plt.yticks(())

    plt.show()





