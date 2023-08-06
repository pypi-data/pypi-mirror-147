from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

from osaft.core.variable import ActiveVariable, PassiveVariable
from osaft.plotting.arf.arf_plotter import ARFPlotter
from osaft.plotting.datacontainers.arf_datacontainer import ARFData
from osaft.solutions.base_arf import BaseARF


class ARFPlot:
    """Plotting different ARF solutions inside same axis over attribute

    :param attr_name: name of attribute for x-axis
    :param x_values: x values for axis
    """

    def __init__(
        self, attr_name: Optional[str] = None,
        x_values: Optional[np.ndarray] = None,
    ):
        """Constructor method"""
        self.plotter = ARFPlotter()
        self._solutions = {}

        self._attr_name = PassiveVariable(attr_name, 'Name of attribute')
        self._x_values = PassiveVariable(x_values, 'Name of attribute')
        # the callable is not important; we want to use the dependency logic of
        # the ActiveVariable and we are not actually interested in the value
        self._needs_computation = ActiveVariable(
            lambda: None,
            'ARF needs to be recomputed',
        )

        self._needs_computation.is_computed_by(self._attr_name, self._x_values)

    @property
    def attr_name(self) -> str:
        """Attribute that is used as x-axis

        :getter: returns the attribute name for the x-axis
        :setter: sets attribute name
        """
        return self._attr_name.value

    @attr_name.setter
    def attr_name(self, value: str) -> None:
        self._attr_name.value = value

    @property
    def x_values(self) -> np.ndarray:
        """Values of x-axis

        :getter: returns x-axis values
        :setter: sets x-axis values
        """
        return self._x_values.value

    @x_values.setter
    def x_values(self, values: np.ndarray) -> None:
        self._x_values.value = values

    def set_abscissa(self, x_values: np.ndarray, attr_name: str) -> None:
        """Setting the abscissa variable and values for the ARF plot

        :param x_values: data points to be plotted over
        :param attr_name: name of the dependent variable to be plotted over
        """
        self.x_values = x_values
        self.attr_name = attr_name

    def add_solutions(self, *solutions: BaseARF) -> None:
        """Add solution to list of solutions for plotting

        :param solutions: one or multiple solutions,
        e.g. :class:`osaft.king1934.ARF()`
        """
        if len(solutions) == 0:
            out = 'is_computed_by() takes at least one positional argument '
            out += '(0 were given)'
            raise TypeError(out)
        for solution in solutions:
            if solution.name in self._solutions:
                raise ValueError(
                    f'Solution with the same name ({solution.name}) is '
                    'already in the list of solution and has been '
                    'overwritten. Consider renaming the '
                    f'attribute `name` of this solution({solution}).',
                )
            self._solutions[solution.name] = ARFData(solution)

    def remove_solution(self, solution: BaseARF) -> None:
        """Remove solution of list of solutions for plotting

        :param solution: specific ARF solution, e.g.
        :class:`osaft.king1932.ARF()`
        """
        self._solutions.pop(solution.name, None)

    def _compute_arf(self) -> None:
        if not self._needs_computation.needs_update:
            return None

        # value of the ActiveVariable needs to be accessed
        # such that the needs_update property changes to False
        _ = self._needs_computation.value
        for _, items in self._solutions.items():
            items.compute_arf(self.attr_name, self.x_values)

    def _find_max(self):
        """Finds the max ARF value in all solutions."""
        all_max = 0
        for _, item in self._solutions.items():
            current_max = np.max(abs(item._arf))
            if current_max > all_max:
                all_max = current_max
        return all_max

    def _normalize_arf(self, normalization_name: str) -> None:
        if normalization_name is None:
            return None
        elif normalization_name == 'max':
            norm = self._find_max()
        elif normalization_name in self._solutions.keys():
            norm = self._solutions[normalization_name].arf
        else:  # pragma: no cover
            raise ValueError(
                'normalization name needs to be either the name '
                'of a solution or \'max\'',
            )
        for _, items in self._solutions.items():
            items.normalize_arf(norm)

    def plot_solutions(
            self,
            ax: Optional[plt.Axes] = None,
            normalization_name: Optional[str] = None,
            plot_method=plt.plot,
            **kwargs,
    ) -> (plt.Figure, plt.Axes):
        """Plot all solutions in stack over attribute set via
        :meth:`set_abscissa()`. If :attr:`normalization_name` is passed,
        the solution is normalized. If :attr:`normalization_name` is the name
        of an added solution then the plot is normalized w.r.t. this solution.
        If :attr:`normalization_name`` = 'max'`, then the plot is normalized
        w.r.t. to the max value.

        :param ax: axes object where plot will be generated
        :param normalization_name: name of the solutions used for normalizing
        :param plot_method: matplotlib native plotting method (e.g.plt.loglog)
        :param kwargs: keyword arguments that get piped to :attr:`plot_method`
        """

        self._compute_arf()
        self._normalize_arf(normalization_name)

        for _, data in self._solutions.items():
            fig, ax = self.plotter.plot_solution(
                self.x_values, data, ax, plot_method, **kwargs,
            )

        self.plotter.set_labels(ax, self.attr_name, normalization_name)
        self.plotter.add_legend(ax)

        return fig, ax


if __name__ == '__main__':
    pass
