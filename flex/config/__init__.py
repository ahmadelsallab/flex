import pandas as pd
import warnings
import yaml
import json
class Configuration:
    def __init__(self, meta_data=None, params=None, performance=None, yaml_file=None, json_file=None, csv_file=None, orig_df=None):
        """
        :param meta_data: the current experiment meta_data
        :type meta_data: dict
        :param params: the current experiment params/hyper parameters
        :type params: dict
        :param performance: the current experiment performance
        :type performance: dict
        :param csv_file: full file path of the old runs params as csv. If given it overrides orig_df
        :type csv_file: string
        :param orig_df: the old runs params as DataFrame. This df will be merged to new experiment, new columns will be added with NaN in old records, but old wont be deleted.
        :type orig_df: DataFrame
        :param yaml_file: full file path of the current experiment yaml. Must have meta_data, params and performance. If given, it overrides the other args.
        :type yaml_file: string

        """
        self.df = pd.DataFrame()
        self.exp_df = pd.DataFrame()


        # Load old runs
        if csv_file or orig_df:
            self.add_logs(csv_file=csv_file, df=orig_df)
        else: # No records exist
            warnings.warn(UserWarning("No old runs records given. It's OK if this is the first record or you will add later using from_csv or from_df. Otherwise, old records they will be overwritten"))

        # Log an experiment if yaml or exp attribs given is given
        if yaml_file or json_file or (meta_data and params and performance):
            self.log(meta_data, params, performance, yaml_file, json_file)

    ####### Interfaces ############
    def __call__(self):
        """
        calling the class returns only the last experiment config
        :return:
        :rtype:
        """
        return self.experiment_info

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
        self.logs = pd.concat([self.df, other.df], axis=0, ignore_index=True, sort=False)


    @property
    def experiment_info(self):
        return self.exp_df.iloc[-1]

    @experiment_info.setter
    def experiment_info(self, exp_df):
        self.exp_df = exp_df
        self.update_df()


    @property
    def logs(self):
        return self.df

    @logs.setter
    def logs(self, df):
        self.df = df
        self.update_df()


    def add_logs(self, csv_file=None, df=None):
        """
        Add old experiments logs
        :param csv_file:
        :type csv_file:
        :param df:
        :type df:
        :return:
        :rtype:
        """
        if csv_file:
            self.from_csv(csv_file=csv_file)
        elif df:
            self.from_df(old_df=df)



    def log(self, meta_data=None, params=None, performance=None, yaml_file=None, json_file=None):
        """
        Adds new config

        :param meta_data:
        :type meta_data:
        :param params:
        :type params:
        :param performance:
        :type performance:
        :param yaml_file:
        :type yaml_file:
        :return:
        :rtype:
        """
        if yaml_file:
            self.experiment_info = self.from_yaml(yaml_file)
        elif json_file:
            self.experiment_info = self.exp_from_json(json_file)
        else:
            # Load runs data:
            assert isinstance(meta_data, dict), "Meta data must a dictionary."
            assert isinstance(params, dict), "Config must a dictionary."
            assert isinstance(performance, dict), "Results must a dictionary."

            self.meta_data = meta_data
            self.params = params
            self.performance = performance

            # Concatenate all experiment parameters (meta, configs and performance) along their columns. This will be one entry DataFrame.
            self.experiment_info = pd.concat([pd.DataFrame([meta_data]), pd.DataFrame([params]), pd.DataFrame([performance])], axis=1)

    def save(self, json_file=None, yaml_file=None):
        """
        Saves current config
        :return:
        :rtype:
        """
        pass

    def save_logs(self, csv_file):
        """
        Writes all logs to csv file
        :return:
        :rtype:
        """
        self.to_csv(csv_file=csv_file)

    ####### Private Methods ############
    def update_df(self):
        self.df = pd.concat([self.df, self.exp_df], axis=0, ignore_index=True, sort=False)

    ######## Current Config Management ########
    def exp_to_json(self, json_file):
        """
        Writes current config to json
        :return:
        :rtype:
        """
        self.exp_df.to_json(json_file)

    def exp_from_json(self, json_file):
        """
        Loads experiment from JSON
        :return:
        :rtype:
        """
        self.experiment_info = pd.read_json(json_file)

    def to_yaml(self, yaml_file):
        """ Write yaml from experiment df

        :param meta_data: exp_df meta
        :type meta_data: DataFrame
        :param params: exp_df configs
        :type params: DataFrame
        :param performance: exp_df performance
        :type performance: DataFrame
        :param yaml_file: the output file to save yaml (full path)
        :type yaml_file: string
        :return:
        :rtype:
        """

        with open(yaml_file, 'w') as f:
            yaml.dump(dict(self.experiment_info), f, default_flow_style=False)

    def from_yaml(self, yaml_file):
        """
        Convert yaml file into df
        :param yaml_file:
        :type yaml_file:
        :return: experiment data frame
        :rtype: DataFrame
        """
        with open(yaml_file, 'r') as f:
            self.experiment_info = pd.DataFrame(yaml.load(f), index=[0])

    ######## All Logs Management ########
    def from_df(self, old_df):
        """
        Loads old logs from DataFrame
        :param old_df:
        :type old_df:
        :return:
        :rtype:
        """
        self.logs = old_df

    def from_csv(self, csv_file):
        """
        Load config from csv
        """
        self.logs = pd.read_csv(csv_file)

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
        self.df.to_csv(csv_file)


    def to_json(self, json_file):
        """
        Log all logs in JSON
        :param json_file:
        :type json_file:
        :return:
        :rtype:
        """

        #self.df.to_json(json_file, orient='index')
        self.df.to_json(json_file)

    def from_json(self, json_file):
        """
        Log all logs in JSON with index orientation
        :param json_file:
        :type json_file:
        :return:
        :rtype:
        """
        '''
        with open(json_file, 'r') as f:
            self.df = pd.DataFrame(json.load(json_file))
        '''
        #self.df = pd.read_json('json_file', orient='index')
        self.logs = pd.read_json(json_file)


    # Utils
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