import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class SmartTable:
    def __init__(self, shape=(3, 3), fill_value=0):
        """
        Initialise un tableau dynamique.
        :param shape: Tuple représentant les dimensions du tableau (par défaut (3, 3)).
        :param fill_value: Valeur initiale pour remplir le tableau (par défaut 0).
        """
        self.data = np.full(shape, fill_value)

    def __repr__(self):
        """
        Représentation textuelle du tableau.
        """
        return f"SmartTable(shape={self.data.shape}, data=\n{self.data})"

    def __getitem__(self, index):
        """
        Accès aux éléments du tableau.
        ex index = i / (i,j) / (i,j,k) ...
        """
        return self.data[index]

    def __setitem__(self, index, value):
        """
        Modification des éléments du tableau.
        ex index = i / (i,j) / (i,j,k) ...
        """
        self.data[index] = value

    def add_row(self, row):
        """
        Ajoute une ligne au tableau.
        :param row: Liste ou tableau à ajouter en tant que nouvelle ligne.
        """
        if len(row) != self.data.shape[1]:
            raise ValueError("La longueur de la ligne doit correspondre au nombre de colonnes.")
        self.data = np.vstack([self.data, row])

    def add_column(self, column):
        """
        Ajoute une colonne au tableau.
        :param column: Liste ou tableau à ajouter en tant que nouvelle colonne.
        """
        if len(column) != self.data.shape[0]:
            raise ValueError("La longueur de la colonne doit correspondre au nombre de lignes.")
        self.data = np.hstack([self.data, np.array(column).reshape(-1, 1)])

    def remove_row(self, index):
        """
        Supprime une ligne par index.
        """
        self.data = np.delete(self.data, index, axis=0)

    def remove_column(self, index):
        """
        Supprime une colonne par index.
        """
        self.data = np.delete(self.data, index, axis=1)

    def summarize(self):
        """Affiche un résumé statistique du tableau."""
        return {
            "shape": self.data.shape,
            "mean": np.mean(self.data),
            "std": np.std(self.data),
            "min": np.min(self.data),
            "max": np.max(self.data),
        }

    def sum(self, axis=None):
        """
        Calcule la somme des éléments.
        :param axis: Axe le long duquel effectuer la somme (None pour somme totale).
        """
        return self.data.sum(axis=axis)

    def mean(self, axis=None):
        """
        Calcule la moyenne des éléments.
        :param axis: Axe le long duquel effectuer la moyenne (None pour moyenne totale).
        """
        return self.data.mean(axis=axis)

    def transpose(self):
        """
        Transpose le tableau (lignes <-> colonnes).
        """
        return SmartTable(self.data.T.shape, fill_value=0).from_numpy(self.data.T)

    def to_numpy(self):
        """
        Convertit le tableau en un tableau NumPy.
        """
        return self.data

    def to_dataframe(self, columns=None):
        """
        Convertit le tableau en DataFrame Pandas.
        :param columns: Liste de noms pour les colonnes.
        """
        return pd.DataFrame(self.data, columns=columns)

    def plot(self, kind="heatmap"):
        """
        Génère un graphique à partir du tableau.
        :param kind: Type de graphique ('heatmap', 'bar', etc.).
        """
        if kind == "heatmap":
            plt.imshow(self.data, cmap="viridis", aspect="auto")
            plt.colorbar()
            plt.title("Heatmap")
            plt.show()
        elif kind == "bar":
            for i, row in enumerate(self.data):
                plt.bar(range(len(row)), row, alpha=0.7, label=f"Row {i}")
            plt.legend()
            plt.title("Bar Chart")
            plt.show()
        else:
            raise ValueError(f"Type de graphique '{kind}' non pris en charge.")

    @staticmethod
    def random(shape, min_val=0, max_val=10):
        """
        Génère un tableau rempli de valeurs aléatoires.
        :param shape: Dimensions du tableau.
        :param min_val: Valeur minimale pour les valeurs aléatoires.
        :param max_val: Valeur maximale pour les valeurs aléatoires.
        """
        return SmartTable(shape).from_numpy(np.random.randint(min_val, max_val, shape))

    def from_numpy(self, numpy_array):
        """
        Remplace les données actuelles par celles d'un tableau NumPy.
        """
        self.data = numpy_array
        return self
