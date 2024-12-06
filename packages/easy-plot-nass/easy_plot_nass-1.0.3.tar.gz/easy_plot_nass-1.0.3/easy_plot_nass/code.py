import matplotlib.pyplot as plt

class EasyPlot:
    def __init__(self, style="ggplot"):
        """
        Initialise le module avec un style par défaut.
        :param style: Style des graphiques (par exemple, 'ggplot', 'seaborn', 'classic').
        """
        plt.style.use(style)

    def line_plot(self, x, y, title="Line Plot", xlabel="X-Axis", ylabel="Y-Axis", legend=None, save_path=None):
        """
        Crée un graphique en ligne.
        """
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, marker="o")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if legend:
            plt.legend(legend)
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def scatter_plot(self, x, y, title="Scatter Plot", xlabel="X-Axis", ylabel="Y-Axis", color="blue", save_path=None):
        """
        Crée un nuage de points.
        """
        plt.figure(figsize=(8, 6))
        plt.scatter(x, y, c=color)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def histogram(self, data, bins=10, title="Histogram", xlabel="Values", ylabel="Frequency", save_path=None):
        """
        Crée un histogramme.
        """
        plt.figure(figsize=(8, 6))
        plt.hist(data, bins=bins, edgecolor="black")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def box_plot(self, data, title="Box Plot", labels=None, save_path=None):
        """
        Crée un graphique à boîte à moustaches.
        """
        plt.figure(figsize=(8, 6))
        plt.boxplot(data, labels=labels)
        plt.title(title)
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def pie_chart(self, labels, sizes, title="Pie Chart", save_path=None):
        """
        Crée un graphique circulaire.
        """
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title(title)
        plt.axis("equal")  # Pour un cercle parfait
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def combined_plot(self, x, y1, y2, title="Combined Plot", xlabel="X-Axis", ylabel="Y-Axis", legend=None, save_path=None):
        """
        Crée un graphique combiné (courbe + histogramme).
        """
        plt.figure(figsize=(8, 6))
        plt.plot(x, y1, label="Line")
        plt.bar(x, y2, alpha=0.5, label="Bar")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if legend:
            plt.legend(legend)
        if save_path:
            plt.savefig(save_path)
        plt.show()
