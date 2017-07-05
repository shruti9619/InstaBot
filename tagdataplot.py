import csv
import numpy as np
import matplotlib.pyplot as plt


def plotter():
    tag_objects = []
    stats = []
    f = open("collection.csv", "rb")
    reader = csv.reader(f)
    for row in reader:
        tag_objects.append(row[0])
        stats.append(row[1])
        print row[0]

    f.close()
    y_pos = np.arange(len(tag_objects))
    plt.bar(y_pos, stats, align='center', alpha=1)
    plt.xticks(y_pos, tag_objects)
    plt.ylabel('Usage')
    plt.title('Tag Trend Data')

    plt.show()

def categoryplotter():
    print