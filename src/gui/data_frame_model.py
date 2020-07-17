"""A GUI view of the guides DB table."""

import pandas as pd
from PySide2 import QtCore
from PySide2.QtCore import Qt


class DataFrameModel(QtCore.QAbstractTableModel):
    """use a dataframe as a model."""

    def __init__(self, df=pd.DataFrame()):
        super().__init__()
        self._df = df

    @property
    def dataframe(self):
        """Dataframe getter."""
        return self._df

    @dataframe.setter
    def dataframe(self, dataframe):
        """Reset the dataframe."""
        self.beginResetModel()
        self._df = dataframe.copy()
        self.endResetModel()

    def data(self, index, role=Qt.DisplayRole):
        """Get the data."""
        if (role != Qt.DisplayRole or not index.isValid()
                or not 0 <= index.row() < self.rowCount()
                or not 0 <= index.column() < self.columnCount()):
            return None
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        val = self._df.iloc[row][col]
        # TODO: Handle different data types
        return str(val)

    def rowCount(self, parent=None, *args, **kwargs):
        """Row count."""
        return self._df.shape[0]

    def columnCount(self, parent=None, *args, **kwargs):
        """Column count."""
        return self._df.shape[1]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Get the row or column headers."""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[section]
            else:
                return str(self._df.index[section])
        return None

    def sort(self, column, order=None):
        """Sort the dataframe by column."""
        col_name = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(
            col_name, ascending=(order == Qt.AscendingOrder), inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
