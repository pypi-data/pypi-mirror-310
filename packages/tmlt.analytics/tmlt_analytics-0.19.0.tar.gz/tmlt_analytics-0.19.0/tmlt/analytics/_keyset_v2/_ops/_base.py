"""Base class for KeySet operations."""

# SPDX-License-Identifier: Apache-2.0
# Copyright Tumult Labs 2024

from abc import ABC, abstractmethod

from pyspark.sql import DataFrame

from tmlt.analytics._schema import ColumnDescriptor


class KeySetOp(ABC):
    """Base class for operations used to define KeySets."""

    @abstractmethod
    def columns(self) -> list[str]:
        """Get a list of the columns included in the output of this operation."""

    @abstractmethod
    def schema(self) -> dict[str, ColumnDescriptor]:
        """Get the schema of the output of this operation.

        If this operation is a plan (i.e. ``self.is_plan()`` returns True), this
        method will raise ``AnalyticsInternalError``.
        """

    @abstractmethod
    def dataframe(self) -> DataFrame:
        """Generate the Spark dataframe corresponding to this operation.

        This operation may be computationally expensive, even though the full
        dataframe is not evaluated until it is used elsewhere.

        If this operation is a plan (i.e. ``self.is_plan()`` returns True), this
        method will raise ``AnalyticsInternalError``.
        """

    @abstractmethod
    def is_empty(self) -> bool:
        """Determine whether the dataframe corresponding to this operation is empty."""

    @abstractmethod
    def is_plan(self) -> bool:
        """Determine whether this plan has any parts requiring partition selection."""
