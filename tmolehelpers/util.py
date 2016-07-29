import pandas as pd
import operator as op


def to_dataframe(collection, *fields):
    field_extractor = op.attrgetter(*fields)
    data = [field_extractor(result) for result in collection]
    if len(fields) is 1:
        data = [(_,) for _ in data]
    index = [result.directory for result in collection]
    return pd.DataFrame.from_records(data, index=index, columns=fields)
