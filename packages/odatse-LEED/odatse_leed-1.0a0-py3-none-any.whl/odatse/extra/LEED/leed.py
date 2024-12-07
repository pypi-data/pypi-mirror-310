# odatse-LEED -- Low Energy Electron Diffraction solver module for ODAT-SE
# Copyright (C) 2024- The University of Tokyo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.

from typing import Dict, List, Tuple
import itertools
import os
import os.path
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path
import subprocess

import numpy as np

import odatse
from odatse import exception
from .input import Input
from .parameter import SolverInfo

class Solver(odatse.solver.SolverBase):
    """
    Solver class for LEED (Low-Energy Electron Diffraction) analysis.
    Inherits from odatse.solver.SolverBase.
    """
    path_to_solver: Path
    dimension: int

    def __init__(self, info: odatse.Info):
        """
        Initializes the Solver instance.

        Parameters
        ----------
        info : odatse.Info
            Information object containing solver configuration.
        """
        super().__init__(info)

        self._name = "leed"
        self.param = SolverInfo(**info.solver)

        # Set environment
        p2solver = self.param.config.path_to_solver
        if os.path.dirname(p2solver) != "":
            # ignore ENV[PATH]
            self.path_to_solver = self.root_dir / Path(p2solver).expanduser()
        else:
            for P in itertools.chain([self.root_dir], os.environ["PATH"].split(":")):
                self.path_to_solver = Path(P) / p2solver
                if os.access(self.path_to_solver, mode=os.X_OK):
                    break
        if not os.access(self.path_to_solver, mode=os.X_OK):
            raise exception.InputError(f"ERROR: solver ({p2solver}) is not found")

        self.path_to_base_dir = self.param.reference.path_to_base_dir
        # check files
        files = ["exp.d", "rfac.d", "tleed4.i", "tleed5.i", "tleed.o", "short.t"]
        for file in files:
            if not os.path.exists(os.path.join(self.path_to_base_dir, file)):
                raise exception.InputError(
                    f"ERROR: input file ({file}) is not found in ({self.path_to_base_dir})"
                )
        self.input = Input(info)

    def evaluate(self, x: np.ndarray, args = (), nprocs: int = 1, nthreads: int = 1) -> float:
        """
        Evaluates the solver with the given parameters.

        Parameters
        ----------
        x : np.ndarray
            Input array.
        args : tuple, optional
            Additional arguments.
        nprocs : int, optional
            Number of processes. Defaults to 1.
        nthreads : int, optional
            Number of threads. Defaults to 1.

        Returns
        -------
        float
            The result of the evaluation.
        """
        self.prepare(x, args)
        cwd = os.getcwd()
        os.chdir(self.work_dir)
        self.run(nprocs, nthreads)
        os.chdir(cwd)
        result = self.get_results()
        return result

    def prepare(self, x: np.ndarray, args) -> None:
        """
        Prepares the solver for evaluation.

        Parameters
        ----------
        x : np.ndarray
            Input array.
        args : tuple
            Additional arguments.
        """
        self.work_dir = self.proc_dir
        for dir in [self.path_to_base_dir]:
            copy_tree(os.path.join(self.root_dir, dir), os.path.join(self.work_dir))
        self.input.prepare(x, args)

    def run(self, nprocs: int = 1, nthreads: int = 1) -> None:
        """
        Runs the solver.

        Parameters
        ----------
        nprocs : int, optional
            Number of processes. Defaults to 1.
        nthreads : int, optional
            Number of threads. Defaults to 1.
        """
        self._run_by_subprocess([str(self.path_to_solver)])

    def _run_by_subprocess(self, command: List[str]) -> None:
        """
        Runs a command using subprocess.

        Parameters
        ----------
        command : List[str]
            Command to run.
        """
        with open("stdout", "w") as fi:
            subprocess.run(
                command,
                stdout=fi,
                stderr=subprocess.STDOUT,
                check=True,
            )

    def get_results(self) -> float:
        """
        Retrieves the results from the solver.

        Returns
        -------
        float
            The R-factor result.

        Raises
        ------
        RuntimeError
            If the R-factor cannot be found.
        """
        rfactor = -1.0
        filename = os.path.join(self.work_dir, "search.s")
        with open(filename, "r") as fr:
            lines = fr.readlines()
            for line in lines:
                if "R-FACTOR" in line:
                    rfactor = float(line.split("=")[1])
                    break
        if rfactor == -1.0:
            msg = f"R-FACTOR cannot be found in {filename}"
            raise RuntimeError(msg)
        return rfactor

