import pandas as pd
import warnings
import yaml
import os
from abc import abstractmethod


class DataMgr:
    '''
    Separate data should be kept for the config and logs for the following reasons:
    1. Merge might introduce NaN in case of deleted or added cols. So the output reports will have NaN
    2. Order of calling to save_log or save_config might make the config record not always the last in the merged DF
    '''
    def __init__(self, logs:pd.DataFrame=None, config:pd.DataFrame=None):
        self.config_df = pd.DataFrame()
        self.df = pd.DataFrame()

        if isinstance(config, pd.DataFrame):
            self.config = config
        if isinstance(logs, pd.DataFrame):
            self.logs = logs

    @property
    def config(self):
        return self.config_df

    @config.setter
    def config(self, config_df: pd.DataFrame):
        # Overwrite config_df
        self.config_df = config_df
        # Add to logs
        self.append(config_df)

    @property
    def logs(self)->pd.DataFrame:
        return self.df

    @logs.setter
    def logs(self, df:pd.DataFrame):
        # Overwrite logs
        self.df = df
        # Append config_df
        self.append(self.config)

    def append(self, df:pd.DataFrame):
        self.df.append(df, ignore_index=True)

    def edit_config(self, attribs:dict):

        attrib_df = pd.DataFrame(attribs, index=[0])

        # Merge in config. It will add new entry, keeping the old one.
        new_config_df = pd.concat([self.config_df, attrib_df], axis=1)

        # Update the config_df
        self.config_df = new_config_df

        # Update the last entry in the logs
        self.df.iloc[-1] = new_config_df.iloc[-1]# we want to have a Series, so we use iloc[-1] on the new_config_df

class PklConfig:
    @classmethod
    @abstractmethod
    def save(cls, df: pd.DataFrame, file: str):
        df.to_pickle(file)

    @classmethod
    @abstractmethod
    def load(cls, file: str) -> pd.DataFrame:
        return pd.read_pickle(file)


class CSVConfig:

    @classmethod
    @abstractmethod
    def save(cls, df: pd.DataFrame, file: str):
        df.to_csv(file)

    @classmethod
    @abstractmethod
    def load(cls, file: str)-> pd.DataFrame:
        return pd.read_csv(file)


class JSONConfig:

    @classmethod
    @abstractmethod
    def save(cls, df: pd.DataFrame, file: str):
        df.to_json(file)

    @classmethod
    @abstractmethod
    def load(cls, file: str) -> pd.DataFrame:
        return pd.read_json(file)


class HTMLConfig:

    @classmethod
    @abstractmethod
    def save(cls, df: pd.DataFrame, file: str):
        df.to_html(file)

    @classmethod
    @abstractmethod
    def load(cls, file: str)-> pd.DataFrame:
        #FIXME:
        return pd.read_html(file)


class YAMLConfig:

    @classmethod
    @abstractmethod
    def save(cls, df: pd.DataFrame, file: str):
        with open(file, 'w') as f:
            yaml.dump(dict(df), f, default_flow_style=False)

    @classmethod
    @abstractmethod
    def load(cls, file: str) -> pd.DataFrame:
        with open(file, 'r') as f:
            return pd.DataFrame(yaml.load(f), index=[0])


class ConfigTypeMgr:
    type_hndlr = {'csv'    :CSVConfig,
                  'json'   :JSONConfig,
                  'html'   :HTMLConfig,
                  'pkl'    :PklConfig,
                  'yml'    :YAMLConfig}
    def __init(self):
        pass

    @classmethod
    @abstractmethod
    def save(cls, df: pd.DataFrame, file:str):
        cls.type_hndlr[cls.check_file_type(file)].save(df, file)

    @classmethod
    @abstractmethod
    def load(cls, file:str)-> pd.DataFrame:
        return cls.type_hndlr[cls.check_file_type(file)].load(file)

    @classmethod
    @abstractmethod
    def check_file_type(cls, file:str) -> str:
        return str(os.path.splitext(file)[1].split('.')[-1])



class Configuration:

    def __init__(self, config=None, logs=None):

        # Load old runs
        logs_df = self.process_config(config)

        # Log config
        config_df = self.process_logs(logs)

        # Update the DB
        self.data_mgr = DataMgr(logs=logs_df, config=config_df)

    ####### Interfaces ############
    def __call__(self, *args, **kwargs):
        return self.config

    def save_config(self, file: str):
        ConfigTypeMgr.save(df=self.data_mgr.config, file=file)

    def load_config(self, file):
        self.data_mgr.config = self.process_config(file)

    def save_logs(self, file: str):
        ConfigTypeMgr.save(df=self.data_mgr.logs, file=file)

    def load_logs(self, file):
        self.data_mgr.logs = self.process_logs(file)

    def append_logs(self, logs):
        self.data_mgr.append(self.process_logs(logs))

    def add_config_attribs(self, attribs:dict):
        self.data_mgr.edit_config(attribs)

    @property
    def config(self)->pd.Series:
        return self.data_mgr.config.iloc[-1]

    @config.setter
    def config(self, config):
        """

        :param config:
        :type config: pd.DataFrame, dict or file
        :return:
        :rtype:
        """
        self.data_mgr.config = self.process_config(config)

    @property
    def logs(self)->pd.DataFrame:
        return self.data_mgr.logs

    @logs.setter
    def logs(self, logs):
        """

        :param logs:
        :type logs: pd.DataFrame, dict or file
        :return:
        :rtype:
        """
        self.data_mgr.logs = self.process_logs(logs)

    def process_config(self, config) -> pd.DataFrame:
        """

        :param config:
        :type config: pd.DataFrame, dict, file
        :return:
        :rtype:
        """
        if isinstance(config, pd.DataFrame):
            config_df = config
        elif isinstance(config, dict):
            config_df = pd.DataFrame(config, index=[0])
        elif isinstance(config, str):
            config_df = ConfigTypeMgr.load(file=config)
        else:
            config_df = pd.DataFrame()
            #assert "Unsupported format of config passed"

        return config_df

    def process_logs(self, logs) -> pd.DataFrame:
        """

        :param logs:
        :type logs: pd.DataFrame, dict, file
        :return:
        :rtype:
        """
        if isinstance(logs, pd.DataFrame):
            logs_df = logs
        elif isinstance(logs, str):
            logs_df = ConfigTypeMgr.load(file=logs)
        elif isinstance(logs, dict):
            logs_df = pd.DataFrame(logs)
        else: # No records exist
            logs_df = pd.DataFrame()
            warnings.warn(UserWarning("No old runs records given or unsupported type. It's OK if this is the first record or you will add later using from_csv or from_df. Otherwise, old records they will be overwritten"))

        return logs_df


    # Utils
    # TODO: Add meta_cols, params_cols and results_cols in init, save_config, load_config --> (return 3 dicts in config if all the 3 are not None)
    def df_to_exp_attribs(self, df):
        """
        Segment the flat experiment df into: meta_data, params and performance
        :param df: flat experiment df
        :type df: DataFrame
        :return: split meta_df, config_df, results_df
        :rtype: DataFrame, DataFrame, DataFrame
        """
        meta_cols = self.meta_data.keys()
        config_cols = self.params.keys()
        results_cols = self.performance.keys()
        meta_df = df[meta_cols]
        config_df = df[config_cols]
        results_df = df[results_cols]

        return meta_df, config_df, results_df