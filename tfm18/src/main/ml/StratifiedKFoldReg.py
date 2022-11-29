import numpy
from sklearn.model_selection import StratifiedKFold


# Define the cross-validator object for regression, which inherits from
# StratifiedKFold, overwritting the split method


# noinspection PyAbstractClass
class StratifiedKFoldReg(StratifiedKFold):

    """

    This class generate cross-validation partitions
    for regression setups, such that these partitions
    resemble the original sample distribution of the
    target variable.
    Credits: jrasero, https://github.com/jrasero

    """

    def split(self, X, y, groups=None):

        n_samples = len(y)

        # Number of labels to discretize our target variable,
        # into bins of quasi equal size
        n_labels = int(numpy.round(n_samples / self.n_splits))

        # Assign a label to each bin of n_splits points
        y_labels_sorted = numpy.concatenate([numpy.repeat(ii, self.n_splits) for ii in range(n_labels)])

        # Get number of points that would fall
        # out of the equally-sized bins
        mod = numpy.mod(n_samples, self.n_splits)

        # Find unique idxs of first unique label's ocurrence
        _, labels_idx = numpy.unique(y_labels_sorted, return_index=True)

        # sample randomly the label idxs to which assign the
        # the mod points
        rand_label_ix = numpy.random.choice(labels_idx, mod, replace=False)

        # insert these at the beginning of the corresponding bin
        y_labels_sorted = numpy.insert(y_labels_sorted, rand_label_ix, y_labels_sorted[rand_label_ix])

        # find each element of y to which label corresponds in the sorted
        # array of labels
        map_labels_y = dict()
        for ix, label in zip(numpy.argsort(y), y_labels_sorted):
            map_labels_y[ix] = label

        # put labels according to the given y order then
        y_labels = numpy.array([map_labels_y[ii] for ii in range(n_samples)])

        return super().split(X, y_labels, groups)
