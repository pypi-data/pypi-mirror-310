from __future__ import annotations

from typing import Any, Callable, Iterable, Optional, Tuple, Union

import pandas as pd

from edspdf import registry
from edspdf.data.base import BaseReader, BaseWriter
from edspdf.data.converters import (
    FILENAME,
    get_dict2doc_converter,
    get_doc2dict_converter,
)
from edspdf.lazy_collection import LazyCollection
from edspdf.utils.collections import dl_to_ld, flatten, ld_to_dl


class PandasReader(BaseReader):
    DATA_FIELDS = ("data",)

    def __init__(
        self,
        data: pd.DataFrame,
        **kwargs,
    ):
        assert isinstance(data, pd.DataFrame)
        self.data = data

        super().__init__(**kwargs)

    def read_main(self) -> Iterable[Tuple[Any, int]]:
        return ((item, 1) for item in dl_to_ld(dict(self.data)))

    def read_worker(self, fragments):
        return [task for task in fragments]


@registry.readers.register("pandas")
def from_pandas(
    data,
    converter: Union[str, Callable],
    **kwargs,
) -> LazyCollection:
    """
    The PandasReader (or `edspdf.data.from_pandas`) handles reading from a table and
    yields documents. At the moment, only entities and attributes are loaded. Relations
    and events are not supported.

    Example
    -------
    ```{ .python .no-check }

    import edspdf

    nlp = edspdf.blank("eds")
    nlp.add_pipe(...)
    doc_iterator = edspdf.data.from_pandas(df, nlp=nlp, converter="omop")
    annotated_docs = nlp.pipe(doc_iterator)
    ```

    !!! note "Generator vs list"

        `edspdf.data.from_pandas` returns a
        [LazyCollection][edspdf.core.lazy_collection.LazyCollection].
        To iterate over the documents multiple times efficiently or to access them by
        index, you must convert it to a list

        ```{ .python .no-check }
        docs = list(edspdf.data.from_pandas(df, converter="omop"))
        ```

    Parameters
    ----------
    data: pd.DataFrame
        Pandas object
    converter: Optional[Union[str, Callable]]
        Converter to use to convert the rows of the DataFrame to Doc objects
    kwargs:
        Additional keyword arguments passed to the converter. These are documented
        on the [Data schemas](/data/schemas) page.

    Returns
    -------
    LazyCollection
    """

    data = LazyCollection(reader=PandasReader(data))
    if converter:
        converter, kwargs = get_dict2doc_converter(converter, kwargs)
        data = data.map(converter, kwargs=kwargs)
    return data


class PandasWriter(BaseWriter):
    def __init__(self, dtypes: Optional[dict] = None):
        self.dtypes = dtypes

    def write_worker(self, records):
        # If write as jsonl, we will perform the actual writing in the `write` method
        for rec in records:
            if isinstance(rec, dict):
                rec.pop(FILENAME, None)
        return records, len(records)

    def write_main(self, fragments):
        import pandas as pd

        columns = ld_to_dl(flatten(fragments))
        res = pd.DataFrame(columns)
        return res.astype(self.dtypes) if self.dtypes else res


@registry.writers.register("pandas")
def to_pandas(
    data: Union[Any, LazyCollection],
    converter: Optional[Union[str, Callable]],
    dtypes: Optional[dict] = None,
    **kwargs,
) -> pd.DataFrame:
    """
    `edspdf.data.to_pandas` writes a list of documents as a pandas table.

    Example
    -------
    ```{ .python .no-check }

    import edspdf

    nlp = edspdf.blank("eds")
    nlp.add_pipe(...)

    doc = nlp("My document with entities")

    edspdf.data.to_pandas([doc], converter="omop")
    ```

    Parameters
    ----------
    data: Union[Any, LazyCollection],
        The data to write (either a list of documents or a LazyCollection).
    converter: Optional[Union[str, Callable]]
        Converter to use to convert the documents to dictionary objects before storing
        them in the dataframe.
    dtypes: Optional[dict]
        Dictionary of column names to dtypes. This is passed to `pd.DataFrame.astype`.
    kwargs:
        Additional keyword arguments passed to the converter. These are documented
        on the [Data schemas](/data/schemas) page.
    """
    data = LazyCollection.ensure_lazy(data)
    if converter:
        converter, kwargs = get_doc2dict_converter(converter, kwargs)
        data = data.map(converter, kwargs=kwargs)

    return data.write(PandasWriter(dtypes))
