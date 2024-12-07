import matplotlib.pyplot as plt

def plot2(
  x1, x2, y,
  markers = ['s','o'],
  fills = ['#ddf', '#fdd'],
  strokes = ['b', 'r'],
  labels = [0, 1],
):
    plt.figure(figsize=(4, 4))
    for i in range(len(y)):
        m = markers[labels.index(y[i])]
        mec = strokes[labels.index(y[i])]
        mfc = fills[labels.index(y[i])]
        plt.plot(x1[i], x2[i], marker=m, mec=mec, mfc=mfc)
    
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.grid();
