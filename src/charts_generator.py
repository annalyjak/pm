
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








