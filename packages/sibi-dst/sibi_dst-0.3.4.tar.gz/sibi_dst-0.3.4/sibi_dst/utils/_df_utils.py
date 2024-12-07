from ._log_utils import Logger

logger = Logger(log_dir='./logs/', logger_name=__name__, log_file=f'{__name__}.log')
class DfUtils:
    def __init__(self, provided_logger=None):
        self.logger = provided_logger or logger


    def load_grouped_activity(self, df, **kwargs):
        debug = kwargs.pop('debug', False)
        group_by_expr = kwargs.pop('group_by_expr', None)
        if group_by_expr is None:
            raise ValueError('group_by_expr must be specified')
        group_expr = kwargs.pop('group_expr', 'count')
        if group_by_expr is not None:
            if debug:
                self.logger.info("Grouping by: {}".format(group_by_expr))
            df = df.groupby(by=group_by_expr).size().reset_index(name=group_expr)
        return df

    def eval_duplicate_removal(self,df, **df_options):
        duplicate_expr = df_options.get('duplicate_expr', None)
        debug = df_options.get('debug', False)
        if duplicate_expr is None:
            return df
        if debug:
            df_duplicates = df[df.duplicated(duplicate_expr)]
            self.logger.info(f"Duplicate Rows based on columns are:, {df_duplicates}")
        sort_field = df_options.get('sort_field', None)
        keep_which = df_options.get('duplicate_keep', 'last')
        if sort_field is None:
            df = df.drop_duplicates(duplicate_expr, keep=keep_which)
        else:
            df = df.sort_values(sort_field).drop_duplicates(duplicate_expr, keep=keep_which)
        return df

    def load_latest(self, df, **kwargs):
        kwargs.update({'duplicate_keep': 'last'})
        return self.eval_duplicate_removal(df, **kwargs)


    def load_earliest(self,df, **kwargs):
        kwargs.update({'duplicate_keep': 'first'})
        return self.eval_duplicate_removal(df, **kwargs)

    @staticmethod
    def add_df_totals(df):
        df.loc['Total'] = df.sum(numeric_only=True, axis=0)
        df.loc[:, 'Total'] = df.sum(numeric_only=True, axis=1)
        return df

    @staticmethod
    def summarise_data(df, **opts):
        summary_columns = opts.get("summary_column", None)
        if summary_columns is None:
            raise ValueError('summary_column must be specified')
        value_columns = opts.get("values_column", None)
        if value_columns is None:
            raise ValueError('values_column must be specified')
        resample_rule = opts.get("rule", "D")
        agg_func = opts.get("agg_func", 'count')
        df = df.pivot_table(index=df.index, columns=summary_columns, values=value_columns,
                            aggfunc=agg_func).fillna(0)
        df = df.resample(resample_rule).sum()
        return df

    @staticmethod
    def summarize_and_resample_data(df, summary_columns, value_columns, **opts):
        if summary_columns is None:
            raise ValueError('summary_column must be specified')
        if value_columns is None:
            raise ValueError('values_column must be specified')

        resample_rule = opts.get("rule", "D")
        agg_func = opts.get("agg_func", 'count')

        return (df.pivot_table(index=df.index, columns=summary_columns, values=value_columns, aggfunc=agg_func)
                .fillna(0)
                .resample(resample_rule)
                .sum())
