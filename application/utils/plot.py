import matplotlib.pyplot as plt

def ts_plot(x,y,figx=10, figy=10, s_scatter=5, alpha_scatter=0.8, alpha_plot=0.2, title=None):
    plt.figure(figsize=(figx,figy))
    if title:
        plt.title(title)
    plt.scatter(x,y,s=s_scatter,alpha=alpha_scatter)
    plt.plot(x,y,alpha=alpha_plot)