# Copyright (c) 2023 ETH Zurich.
#                    All rights reserved.
#
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# main authors: Robert Gerstenberger, Nils Blach

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List


class Prompter(ABC):
    """
    Abstract base class that defines the interface for all prompters.
    Prompters are used to generate the prompts for the language models.
    """

    @abstractmethod
    def aggregate_prompt(self, state_dicts: Dict, **kwargs) -> str:
        """
        Generate a aggregation prompt for the language model.
        """
        pass

    @abstractmethod
    def improve_prompt(self, state_dicts: Dict, **kwargs) -> str:
        """
        Generate an improve prompt for the language model.
        The thought state is unpacked to allow for additional keyword arguments
        and concrete implementations to specify required arguments explicitly.
        """
        pass

    @abstractmethod
    def generate_prompt(self, state_dicts: Dict, **kwargs) -> str:
        """
        Generate a generate prompt for the language model.
        The thought state is unpacked to allow for additional keyword arguments
        and concrete implementations to specify required arguments explicitly.
        """
        pass

    @abstractmethod
    def split_prompt(self, state_dicts: Dict, **kwargs) -> str:
        """
        Generate a split prompt for the language model.
        The thought state is unpacked to allow for additional keyword arguments
        and concrete implementations to specify required arguments explicitly.
        """
        pass