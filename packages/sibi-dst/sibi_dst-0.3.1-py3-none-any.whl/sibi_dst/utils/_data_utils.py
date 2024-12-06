import numpy as np
import pandas as pd

class DataUtils:
    @staticmethod
    def transform_numeric_columns(df, fill_value=0, transform_func=None, meta_type='int64'):
        """
        Transform integer columns in a Dask DataFrame, handling missing values and applying optional transformations.

        Parameters:
        - df (dask.dataframe.DataFrame): The Dask DataFrame.
        - fill_value (int): The value to replace NA values with.
        - transform_func (callable, optional): The transformation function to apply.
          If None, no additional transformation is applied.
        - meta_type (str): The target data type for the transformed column (default 'int64').

        Returns:
        - dask.dataframe.DataFrame: Updated DataFrame with transformed integer columns.
        """

        def is_integer_dtype(col):
            """
            Check if a column has an integer or nullable integer type.
            """
            return pd.api.types.is_integer_dtype(col.dtype)

        def is_float_dtype(col):
            """
            Check if a column has a float type.
            """
            return pd.api.types.is_float_dtype(col.dtype)

        # Detect integer columns
        integer_columns = [col for col in df.columns if is_integer_dtype(df[col])]
        # Detect float columns
        float_columns = [col for col in df.columns if is_float_dtype(df[col])]

        # Default transformation function (identity) if none is provided
        if transform_func is None:
            transform_func_int = lambda x: x
            transform_func_float = lambda x: x

        # Apply transformations
        if integer_columns:
            meta_type = 'int64'
            for col in integer_columns:
                df[col] = df[col].fillna(fill_value).astype(meta_type).apply(
                    transform_func_int, meta=(col, meta_type)
                )

        if float_columns:
            meta_type = 'float64'
            for col in float_columns:
                df[col] = df[col].fillna(fill_value).astype(meta_type).apply(
                    transform_func_int, meta=(col, meta_type)
                )
        return df

    @staticmethod
    def transform_boolean_columns(df, threshold=1):
        """
        Transform boolean-like columns (e.g., 0/1 or similar) in a Dask DataFrame to actual booleans.

        Parameters:
        - df (dask.dataframe.DataFrame): The Dask DataFrame.
        - threshold (int or float): The value to evaluate as `True`.

        Returns:
        - dask.dataframe.DataFrame: Updated DataFrame with transformed boolean columns.
        """

        def is_boolean_like(col):
            """
            Check if a column is boolean-like (contains 0/1 or similar data).
            """
            sample = col.head(10, compute=True)
            return sample.isin([0, 1]).all()  # Check if all values are 0 or 1 in a sample

        # Detect boolean-like columns
        boolean_columns = [col for col in df.columns if is_boolean_like(df[col])]

        # Transformation function
        def to_boolean(value):
            return value == threshold

        # Apply transformation to each detected column
        for col in boolean_columns:
            df[col] = df[col].apply(to_boolean, meta=(col, 'bool'))

        return df



    @staticmethod
    def merge_lookup_data(classname, df, **kwargs):
        """
        kwargs={
            'source_col':'marital_status_id',
            'lookup_description_col':'description',
            'lookup_col':'id',
            'source_description_alias':'marital_status_description',
            'fillna_source_description_alias': True
        }
        :param classname:
        :param df:
        :param kwargs:
        :return:
        """
        if df.empty:
            return df
        source_col = kwargs.pop('source_col', None)
        lookup_col = kwargs.pop('lookup_col', None)
        lookup_description_col = kwargs.pop('lookup_description_col', None)
        source_description_alias = kwargs.pop('source_description_alias', None)
        fillna_source_description_alias = kwargs.pop('fillna_source_description_alias', False)
        fieldnames = kwargs.get('fieldnames', None)
        column_names = kwargs.get('column_names', None)

        if source_col is None or lookup_description_col is None or source_description_alias is None or lookup_col is None:
            raise ValueError(
                'source_col, lookup_col, lookup_description_col and source_description_alias must be specified')
        if source_col not in df.columns:
            # raise ValueError(f'{source_col} not in dataframe columns')
            return df
        ids = list(df[source_col].dropna().unique())
        if not ids:
            return df
        if fieldnames is None:
            kwargs['fieldnames'] = (lookup_col, lookup_description_col)
        if column_names is None:
            kwargs['column_names'] = ['temp_join_col', source_description_alias]
        kwargs[f'{lookup_col}__in'] = ids
        result = classname(live=True).load(**kwargs)
        if 'temp_join_col' in kwargs.get("column_names"):
            temp_join_col = 'temp_join_col'
        else:
            temp_join_col = lookup_col

        df = df.merge(result, how='left', left_on=source_col, right_on=temp_join_col)
        if fillna_source_description_alias:
            if source_description_alias in df.columns:
                df.fillna({source_description_alias: ''}, inplace=True)
        if 'temp_join_col' in df.columns:
            df.drop(columns='temp_join_col', inplace=True)
        return df