# FIXME: use https://github.com/ahmadelsallab/ml_experiments either as submodule or pip install git+https://github.com/ahmadelsallab/ml_experiments

import pandas as pd
import warnings
import yaml
class Configuration:
    # TODO: add **kwargs to support any experiment parameters other than the given ones. It should be a dict.
    # TODO: csv_file and orig_df should be combined in 'prev_logs', and internal type checking to be done
    # TODO: yaml_file should be renamed into config_file and extension checked internally
    def __init__(self, meta_data=None, params=None, performance=None, csv_file=None, orig_df=None, yaml_file=None):
        """
        :param meta_data: the current experiment meta_data
        :type meta_data: dict
        :param params: the current experiment params/hyper parameters
        :type params: dict
        :param performance: the current experiment results
        :type performance: dict
        :param csv_file: full file path of the old runs params as csv. If given it overrides orig_df
        :type csv_file: string
        :param orig_df: the old runs params as DataFrame. This df will be merged to new experiment, new columns will be added with NaN in old records, but old wont be deleted.
        :type orig_df: DataFrame
        :param yaml_file: full file path of the current experiment yaml. Must have meta_data, params and results. If given, it overrides the other args.
        :type yaml_file: string

        """

        # Load old runs
        if csv_file:
            self.from_csv(csv_file)

        elif orig_df is not None:
            self.from_df(orig_df)

        else: # No records exist

            self.df = pd.DataFrame()
            warnings.warn(UserWarning("No old runs records given. It's OK if this is the first record or you will add later using from_csv or from_df. Otherwise, old records they will be overwritten"))

        # Log an experiment if yaml or exp attribs given is given
        if yaml_file or (meta_data and params and performance):
            self.log(meta_data, params, performance, yaml_file)

    def __str__(self):
        # FIXME
        return self.df

    def __repr__(self):
        # FIXME:
        return self.df

    def __iter__(self):
        return self.df.items()

    def __add__(self, other):
        # FIXME
        self.df = pd.concat([self.df, other.df], axis=0, ignore_index=True, sort=False)

    def from_csv(self, csv_file):
        self.df = pd.read_csv(csv_file)


    def from_df(self, old_df):
        self.df = old_df

    def log(self, meta_data=None, config=None, results=None, yaml_file=None):

        # Build the log experiment df
        exp_df = self.to_df(meta_data, config, results, yaml_file)

        # Append the current experiment to old records
        self.df = pd.concat([self.df, exp_df], axis=0, ignore_index=True, sort=False)

    def to_df(self, meta_data=None, config=None, results=None, yaml_file=None):
        if yaml_file:
            exp_df = self.from_yaml(yaml_file)

        else:
            # Load runs data:
            assert isinstance(meta_data, dict), "Meta data must a dictionary."
            assert isinstance(config, dict), "Config must a dictionary."
            assert isinstance(results, dict), "Results must a dictionary."

            # Concatenate all experiment parameters (meta, configs and results) along their columns. This will be one entry DataFrame.
            exp_df = pd.concat([pd.DataFrame([meta_data]), pd.DataFrame([config]), pd.DataFrame([results])], axis=1)

        return exp_df

    def to_csv(self, csv_file):
        """
        Writes the whole experiment data frame to csv_file
        Warning: if the csv_file has old runs they will be overwritten.
        To avoid that, first load the old runs records using from_csv method.

        :param csv_file: full file path
        :type csv_file: string
        :return:
        :rtype:
        """
        with open(csv_file, mode='w', newline='\n') as f:
            self.df.to_csv(f, index=False, sep=",", line_terminator='\n', encoding='utf-8')
        #self.df.to_csv(csv_file, index=False, line_terminator='\n')

    def from_yaml(self, yaml_file):
        """
        Convert yaml file into df
        :param yaml_file:
        :type yaml_file:
        :return: experiment data frame
        :rtype: DataFrame
        """
        with open(yaml_file, 'r') as f:
            exp_df = pd.DataFrame(yaml.load(f), index=[0])
        return exp_df
    def to_yaml(self, meta_data, config, results, yaml_file):
        """ Write yaml from experiment df

        :param meta_data: exp_df meta
        :type meta_data: DataFrame
        :param config: exp_df configs
        :type config: DataFrame
        :param results: exp_df results
        :type results: DataFrame
        :param yaml_file: the output file to save yaml (full path)
        :type yaml_file: string
        :return:
        :rtype:
        """


        exp_df = self.to_df(meta_data, config, results, yaml_file=None)
        with open(yaml_file, 'wt') as f:
            yaml.dump(exp_df.iloc[-1].to_dict(), f, default_flow_style=False)

        return exp_df

class DLConfiguration(Configuration):

    def _init_(self, yaml_file=None, meta_data=None, config=None, results=None):
        """

        :param yaml_file:
        :type yaml_file:
        :param meta_data:
        :type meta_data:
        :param config:
        :type config:
        :param results:
        :type results:
        :return:
        :rtype:
        """

        if yaml_file:
            self.parse_yaml(yaml_file)
        elif meta_data:
            '''meta_data is supposed to be dict: {'Name': , 'Description': , 'Run File':, 'Commit':}'''
            assert isinstance(meta_data, dict)
            self.meta_df = pd.DataFrame(meta_data)
        elif config:
            assert isinstance(config, dict)
        elif results:
            assert isinstance(results, dict)
        return

    def __str__(self):

        return 0

    def build_hier_df(self, level1_col_names, level2_dfs):
        """ Utility to restore a 2 level hierarichal indexed df, from many flat dfs

        :param level1_col_names: the higher level columns names
        :type level1_col_names: list of strings
        :param level2_dfs: the data frames to be used to build the 2 level column indexed df
        :type level2_dfs: list of DataFrames
        :return: merged hierarichal data frame
        :rtype: pd.DataFrame
        """
        level1_cols = []
        for level1_col_name, level2_df in zip(level1_col_names, level2_dfs):
            level1_cols.extend([level1_col_name for col in level2_df.columns])
        merged = pd.concat(level2_dfs, axis=1)
        merged.columns = [level1_cols, merged.columns]

        return merged

    def parse_yaml(self, yaml_file):
        # TODO: read yaml file and fill in the proper dfs
        return
    def from_csv(self):

        return 0

    def to_csv(self):

        return 0

    def save(self):

        return 0

    def load(self):

        return 0

    def from_yaml(self):

        return 0

    def to_yaml(self):

        return 0
