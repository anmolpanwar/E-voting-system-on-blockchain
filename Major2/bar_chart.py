import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def show(performance):
    objects = ('BJP','Congress','NOTA')
    y_pos = np.arange(len(objects))

    plt.bar(y_pos, performance, align='center', alpha=1)
    plt.xticks(y_pos, objects)
    plt.ylabel('Votes')
    plt.title('Elections Result')

    plt.show()

if __name__=='__main__':
    show([40,58,7])
