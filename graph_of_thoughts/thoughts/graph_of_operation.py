# Copyright (c) 2023 ETH Zurich.
#                    All rights reserved.
#
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# main author: Nils Blach

from __future__ import annotations
from typing import List
from graphviz import Digraph
import string
import os

from graph_of_thoughts.thoughts.operations import Operation


class GraphOfOperations:
    """
    Represents the Graph of Operations, which prescribes the execution plan of thought operations.
    """

    def __init__(self, is_visualize:bool = True) -> None:
        """
        Initializes a new Graph of Operations instance with empty operations, roots, and leaves.
        The roots are the entry points in the graph with no predecessors.
        The leaves are the exit points in the graph with no successors.
        """
        self.operations: List[Operation] = []
        self.roots: List[Operation] = []
        self.leaves: List[Operation] = []
        self.is_visualize = is_visualize
        if self.is_visualize == True:
            self.dot = Digraph(comment='A Round Graph')
            self.label = list(string.ascii_letters) + list(string.ascii_lowercase)


    def append_operation(self, operation: Operation) -> None:
        """
        Appends an operation to all leaves in the graph and updates the relationships.

        :param operation: The operation to append.
        :type operation: Operation
        """
        self.operations.append(operation)
        if self.is_visualize == True:
            self.dot.node(self.label[operation.id], operation.operation_name)

        if len(self.roots) == 0:
            self.roots = [operation]
        else:
            for leave in self.leaves:
                leave.add_successor(operation)
                if self.is_visualize == True:
                    self.dot.edge(self.label[leave.id], self.label[operation.id])

        self.leaves = [operation]


    def add_operation(self, operation: Operation) -> None:
        """
        Add an operation to the graph considering its predecessors and successors.
        Adjust roots and leaves based on the added operation's position within the graph.

        :param operation: The operation to add.
        :type operation: Operation
        """
        self.operations.append(operation)
        if self.is_visualize == True:
            self.dot.node(self.label[operation.id], operation.operation_name)
        if len(self.roots) == 0:
            self.roots = [operation]
            self.leaves = [operation]
            assert (
                len(operation.predecessors) == 0
            ), "First operation should have no predecessors"
        else:
            if len(operation.predecessors) == 0:
                self.roots.append(operation)
            for predecessor in operation.predecessors:
                if self.is_visualize == True:
                    self.dot.edge(self.label[predecessor.id], self.label[operation.id])
                if predecessor in self.leaves:
                    self.leaves.remove(predecessor)
            if len(operation.successors) == 0:
                self.leaves.append(operation)

    def visualize(self): 
        if not self.is_visualize:
            raise TypeError("`is_visualize` is set into False, so this feature is not supported")
            return
        self.dot.format = 'png'
        self.dot.render('visualization/Graph', view = True)