import sys
from os.path import dirname
#sys.path.append(dirname(__file__))
#sys.path.append(dirname('../experiments.py'))
sys.path.append(dirname('../'))
import unittest
from unittest import TestCase
from flex.flex.config import Configuration
import pandas as pd
import yaml

class TestExperiment(TestCase):

    def test__init_no_old_exp_no_logged_exp(self):
        """
        Test init when no old or logged experiments given
        :return: Expected to have a warning, and the internal df is empty
        :rtype:
        """
        with self.assertWarns(UserWarning):
            experiment = Configuration()
            self.assertTrue(experiment.df.empty)

    def test__init_from_csv(self):
        """
        Test init with old experiments in a csv
        :return:
        :rtype: Expected to have the internal df having the same data in the csv
        """
        experiment = Configuration(csv_file='results_old.csv')

        old_df = pd.read_csv('results_old.csv')

        assert old_df.equals(experiment.df)

    def test__init_old_exp_orig_df_incomplete_exp(self):
        """
        Test init with old csv experiment + logged experiment with missing info
        :return: Expected to have user warning + internal df is empty
        :rtype:
        """

        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()


        experiment = Configuration(orig_df=old_df,
                                   meta_data=None,
                                   params=exp_config,
                                   performance=exp_results)
        self.assertFalse(experiment.df.empty)
        self.assertTrue(old_df.equals(experiment.df))

        experiment = Configuration(orig_df=old_df,
                                   meta_data=None,
                                   params=None,
                                   performance=exp_results)
        self.assertFalse(experiment.df.empty)
        self.assertTrue(old_df.equals(experiment.df))


        experiment = Configuration(orig_df=old_df,
                                   meta_data=exp_meta,
                                   params=None,
                                   performance=None)
        self.assertFalse(experiment.df.empty)
        self.assertTrue(old_df.equals(experiment.df))


    def test__init_old_exp_orig_df_complete_exp(self):
        """
        Test init with old csv experiment + logged experiment
        :return: Expected internal df = old csv + logged data
        :rtype:
        """

        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()


        experiment = Configuration(orig_df=old_df,
                                   meta_data=exp_meta,
                                   params=exp_config,
                                   performance=exp_results)
        self.assertFalse(experiment.df.empty)
        exp_df = pd.concat([pd.DataFrame([exp_meta]), pd.DataFrame([exp_config]), pd.DataFrame([exp_results])],
                           axis=1)
        df = pd.concat([old_df, exp_df], axis=0, ignore_index=True, sort=False)
        self.assertTrue(df.equals(experiment.df))

    def test__init_old_exp_orig_df(self):
        """
        Test init with old csv experiment + logged experiment
        :return: Expected internal df = old csv + logged data
        :rtype:
        """

        old_df = pd.read_csv('results_old.csv')


        experiment = Configuration(orig_df=old_df)
        self.assertFalse(experiment.df.empty)
        self.assertTrue(old_df.equals(experiment.df))

    def test__init_old_exp_new_yaml(self):
        """
        Test init with old csv experiment + logged experiment
        :return: Expected internal df = old csv + logged data
        :rtype:
        """
        experiment = Configuration(csv_file='results_old.csv', yaml_file='config.yml')
        self.assertFalse(experiment.df.empty)


        with open('config.yml', 'r') as f:
            exp_df = pd.DataFrame(yaml.load(f), index=[0])

        old_df = pd.read_csv('results_old.csv')
        df = pd.concat([old_df, exp_df], axis=0, ignore_index=True, sort=False)
        self.assertTrue(df.equals(experiment.df))

    def test__init_no_old_exp_new_yaml(self):
        """
        Test init with old csv experiment + logged experiment
        :return: Expected internal df = old csv + logged data
        :rtype:
        """
        with self.assertWarns(UserWarning):
            experiment = Configuration(yaml_file='config.yml')
            self.assertFalse(experiment.df.empty)

            with open('config.yml', 'r') as f:
                exp_df = pd.DataFrame(yaml.load(f), index=[0])

            self.assertTrue(exp_df.equals(experiment.df))


    def test__init_no_old_exp_incomplete_exp(self):
        """
        Test init with no old experiment + logged experiment with missing info
        :return: Expected to have user warning + internal df is empty
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()

        with self.assertWarns(UserWarning):
            experiment = Configuration(params=exp_config)
            self.assertTrue(experiment.df.empty)

        with self.assertWarns(UserWarning):
            experiment = Configuration(meta_data=exp_meta)
            self.assertTrue(experiment.df.empty)

        with self.assertWarns(UserWarning):
            experiment = Configuration(params=exp_results)
            self.assertTrue(experiment.df.empty)

    def test__init_no_old_exp_complete_exp(self):
        """
        Test init with no old experiments and logged experiment
        :return: Expected internal df = logged data
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()
        
        # Windows: Needs fix in unittest in File "/home/ahmad/anaconda3/lib/python3.6/unittest/case.py", line 230
        # Change sys.modules.values() into sys.modules.copy().values()
        with self.assertWarns(UserWarning):
            experiment = Configuration(meta_data=exp_meta, params=exp_config, performance=exp_results)
            self.assertFalse(experiment.df.empty)
            exp_df = pd.concat([pd.DataFrame([exp_meta]), pd.DataFrame([exp_config]), pd.DataFrame([exp_results])], axis=1)
            self.assertTrue(exp_df.equals(experiment.df))

    def test_from_csv(self):
        """
        Test init with csv data, but no logged data
        :return: Expected to have internal df with csv data
        :rtype:
        """
        experiment = Configuration()
        experiment.from_csv(csv_file='results_old.csv')
        old_df = pd.read_csv('results_old.csv')

        self.assertFalse(experiment.df.empty)
        assert old_df.equals(experiment.df)

    def test_from_df(self):
        """
        Test init from a df
        :return: Expected internal df to have same data as passed df
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        experiment = Configuration()
        experiment.from_df(old_df)

        assert old_df.equals(experiment.df)

    def test_log_experiment(self):
        """
        Test logging extra experiment(s) data
        :return: Expected to have internal df appending logged data every time
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()


        experiment = Configuration(csv_file='results_old.csv')
        experiment.log(meta_data=exp_meta, params=exp_config, performance=exp_results, yaml_file=None)
        self.assertFalse(experiment.df.empty)
        #exp_df = old_df.iloc[-1]#pd.concat([meta_df.iloc[-1], config_df.iloc[-1], exp_results], axis=1)
        exp_df = pd.concat([pd.DataFrame([exp_meta]), pd.DataFrame([exp_config]), pd.DataFrame([exp_results])], axis=1)
        df = pd.concat([old_df, exp_df], axis=0, ignore_index=True, sort=False)
        self.assertTrue(df.equals(experiment.df))

    def test_log_experiment_no_previous_exp(self):
        """
        Test logging extra experiment(s) data with no previous records
        :return: Expected to have internal df appending logged data every time
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()

        with self.assertWarns(UserWarning):
            experiment = Configuration()
            self.assertTrue(experiment.df.empty)
            experiment.log(meta_data=exp_meta, params=exp_config, performance=exp_results, yaml_file=None)
            self.assertFalse(experiment.df.empty)
            #exp_df = old_df.iloc[-1]#pd.concat([meta_df.iloc[-1], config_df.iloc[-1], exp_results], axis=1)
            exp_df = pd.concat([pd.DataFrame([exp_meta]), pd.DataFrame([exp_config]), pd.DataFrame([exp_results])], axis=1)

            self.assertTrue(exp_df.equals(experiment.df))

        # Log another one
        experiment.log(meta_data=exp_meta, params=exp_config, performance=exp_results, yaml_file=None)
        self.assertFalse(experiment.df.empty)
        #exp_df = old_df.iloc[-1]#pd.concat([meta_df.iloc[-1], config_df.iloc[-1], exp_results], axis=1)
        exp_df = pd.concat([exp_df, exp_df], axis=0, ignore_index=True, sort=False)

        self.assertTrue(exp_df.equals(experiment.df))

    def test_log_experiment_yaml(self):
        """
        Test logging extra experiment(s) data from yaml
        :return: Expected to have internal df appending logged data every time
        :rtype:
        """

        experiment = Configuration(csv_file='results_old.csv')
        self.assertFalse(experiment.df.empty)
        experiment.log(yaml_file='config.yml')

        with open('config.yml', 'r') as f:
            exp_df = pd.DataFrame(yaml.load(f), index=[0])

        old_df = pd.read_csv('results_old.csv')
        df = pd.concat([old_df, exp_df], axis=0, ignore_index=True, sort=False)
        self.assertTrue(df.equals(experiment.df))

    def test_no_prev_exp_log_experiment_yaml(self):
        """
        Test logging extra experiment(s) data from yaml
        :return: Expected to have internal df appending logged data every time
        :rtype:
        """

        experiment = Configuration()
        self.assertTrue(experiment.df.empty)
        experiment.log(yaml_file='config.yml')

        with open('config.yml', 'r') as f:
            exp_df = pd.DataFrame(yaml.load(f), index=[0])

        self.assertTrue(exp_df.equals(experiment.df))

    def test_log_experiment_incomplete_attribs(self):
        """
        Test logging incomplete experiment data
        :return: Expected assertion
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()

        with self.assertRaises(AssertionError):
            experiment = Configuration()
            experiment.log(exp_meta, None, None, None)

    def test_log_experiment_bad_data_type(self):
        """
        Test passing non-dict type
        :return: Expected assertion
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = []
        exp_config = []
        exp_results = results_df.iloc[-1].to_dict()

        with self.assertRaises(AssertionError):
            experiment = Configuration()
            experiment.log(exp_meta, exp_config, exp_results, None)


    def test_exp_to_df(self):
        """
        Test conversion from experiment attribs to one df
        :return: Expected merged df of meta, params and performance
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()

        with self.assertWarns(UserWarning):
            experiment = Configuration()
            df = experiment.to_df(meta_data=exp_meta, params=exp_config, performance=exp_results, yaml_file=None)
            self.assertFalse(df.empty)

            exp_df = pd.concat([pd.DataFrame([exp_meta]), pd.DataFrame([exp_config]), pd.DataFrame([exp_results])], axis=1)

            self.assertTrue(exp_df.equals(df))

    def test_to_csv(self):
        """
        Test writing the full experiment df (including old one)
        :return:
        :rtype:
        """
        experiment = Configuration(csv_file='results.csv')
        experiment.to_csv('results.csv')
        df = pd.read_csv('results.csv')
        self.assertTrue(df.equals(experiment.df))

    def test_new_logged_exp_to_csv(self):
        """
        Test writing the full experiment df (including old one)
        :return:
        :rtype:
        """
        experiment = Configuration(csv_file='results.csv')
        experiment.to_csv('results.csv')

        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()


        experiment = Configuration(csv_file='results_old.csv')
        experiment.log(meta_data=exp_meta, params=exp_config, performance=exp_results, yaml_file=None)
        self.assertFalse(experiment.df.empty)
        #exp_df = old_df.iloc[-1]#pd.concat([meta_df.iloc[-1], config_df.iloc[-1], exp_results], axis=1)
        exp_df = pd.concat([pd.DataFrame([exp_meta]), pd.DataFrame([exp_config]), pd.DataFrame([exp_results])], axis=1)
        df = pd.concat([old_df, exp_df], axis=0, ignore_index=True, sort=False)
        self.assertTrue(df.equals(experiment.df))

        experiment.to_csv('results.csv')
        df = pd.read_csv('results.csv')
        self.assertTrue(df.equals(experiment.df))

    def test_from_yaml(self):
        """
        Test Convert yaml file into df
        :return: Expected returned df to be the same as in yaml file
        :rtype: DataFrame
        """
        experiment = Configuration()
        exp_df = experiment.from_yaml('config.yml')
        with open('config.yml', 'r') as f:
            df = pd.DataFrame(yaml.load(f), index=[0])

        self.assertTrue(df.equals(exp_df))

    def test_to_yaml(self):
        """
        Test writing of yaml file from an experiment data frame
        :return: Expected to write yaml file with the same params in the experiment df's
        :rtype: yaml file written on desk
        """
        experiment = Configuration(csv_file='results.csv')
        self.assertFalse(experiment.df.empty)
        experiment.log(yaml_file='config.yml')

        with open('config.yml', 'r') as f:
            in_config = pd.DataFrame(yaml.load(f), index=[0])


        meta_df, config_df, results_df = self.df_to_exp_attribs(in_config)

        #experiment.to_yaml(meta_df.iloc[-1].to_dict(), config_df.iloc[-1].to_dict(), results_df.iloc[-1].to_dict(), 'out_config.yml')
        experiment.to_yaml(meta_df.iloc[-1].to_dict(), config_df.iloc[-1].to_dict(), results_df.iloc[-1].to_dict(),
                           'out_config.yml')

        with open('out_config.yml', 'r') as f:
            out_config = pd.DataFrame(yaml.load(f), index=[0])
            
        self.assertTrue(in_config.equals(out_config))



    # Utils
    def df_to_exp_attribs(self, df):
        """
        Segment the flat experiment df into: meta_data, params and performance
        :param df: flat experiment df
        :type df: DataFrame
        :return: split meta_df, config_df, results_df
        :rtype: DataFrame, DataFrame, DataFrame
        """
        meta_cols = ['Name', 'Purpose', 'Description', 'Run file', 'Commit']
        config_cols = ['Features', 'Train_test_split', 'Size', 'maxlen', 'batch_size', 'epochs', 'type',
                       'lr', 'lstm_output_size', 'dense', 'dropout', 'embedding_size',
                       'pool_size', 'filters', 'kernel_size']
        results_cols = ['AUC', 'Val acc', 'Model file', 'Comment']
        meta_df = df[meta_cols]
        config_df = df[config_cols]
        results_df = df[results_cols]

        return meta_df, config_df, results_df

if __name__ == '__main__':
    unittest.main()
