from ..data import BaseDataPreprocessor

from ..config import Configuration
from ..data import BaseDataLoader
from ..learners import BaseLearner
from ..models import BaseModel

import os
import subprocess
import warnings
class Application:
    def __init__(self,
                 loader: BaseDataLoader,
                 preprocessor: BaseDataPreprocessor,
                 model: BaseModel,
                 config: Configuration):
        self.loader = loader
        self.preprocessor = preprocessor
        self.model = model
        self.config = config

    def run(self):
        # Load data
        raw_data = self.loader.load_data()

        # Preprocess data
        data = self.preprocessor.preprocess_data(raw_data)

        # Load model
        self.model.load()

        # Predict
        result = self.model.predict(data)

        return result




class Runner:
    def __init__(self,
                 loader: BaseDataLoader,
                 preprocessor: BaseDataPreprocessor,
                 model: BaseModel,
                 learner: BaseLearner,
                 config: Configuration):
        self.loader = loader
        self.preprocessor = preprocessor
        self.model = model
        self.learner = learner
        self.config = config

    def run(self):
        # Load data
        raw_data = self.loader.load_data()

        # Preprocess data
        data = self.preprocessor.preprocess_data(raw_data)

        # TODO: Add to learner train, test split
        train_data = data
        test_data = data

        # Build model
        model = self.model.build()

        # Train
        self.learner.train(train_data=train_data, model=model)

        # Test
        self.learner.test(test_data=test_data, model=model)

        # Predict
        #self.model.predict()

        # Load performance
        self.config.to_csv(csv_file='../../runs/performance.csv')

    def save(self, branch, tag):
        """
        git checkout -b <branch>
        git add *
        git commit -m"tag"
        git tag <tag>
        git push -f origin <tag> <branch>:<branch>

        :param branch:
        :type branch:
        :param tag:
        :type tag:
        :return:
        :rtype:
        """
        # Change dir to base repo path
        # TODO: make repo path generic
        # TODO: add to Configuration self.config, meta and performance
        os.chdir(self.config()['repo_path'])

        # git checkout -b <branch>
        res = subprocess.call(['git', 'checkout', '-b', branch])
        assert res==0, 'Git command failed: ' + 'git checkout -b <branch>'

        # git add *
        res = subprocess.call(['git', 'add', '*'])
        assert res == 0, 'Git command failed: ' + 'git add *'

        # git commit -m"tag"
        res = subprocess.call(['git', 'commit', '-am', tag])
        if res != 0:
            '''
            !git config --global user.email "you@example.com"
            !git config --global user.name  "Your Name"
            '''
            res = subprocess.call(['git', 'config', '--global', 'user.email', self.config()['email']])
            assert res == 0, 'Git command failed: ' + 'git config --global user.email  "self.config()[email]"'
            res = subprocess.call(['git', 'config', '--global', 'user.name', self.config()['git_username']])
            assert res == 0, 'Git command failed: ' + 'git config --global user.name  "self.config()[git_username]"'
            res = subprocess.call(['git', 'commit', '-am', tag])
            assert res == 0, 'Git command failed: ' + 'git commit -mTag'

        #git push -f origin <tag> <branch>:<branch>

        res = subprocess.call(['git', 'push', '-f', 'origin', tag, branch+':'+branch])
        if res != 0:
            warnings.warn(
                UserWarning("Follow the steps to setup SSH keys here: "
                            "https://help.github.com/articles/generating-ssh-keys, "
                            "simply run (ssh-keygen -t rsa -b 4096 -C email@email.com), "
                            "then cat ~/.ssh/id_rsa.pub, copy that and add SSH to github or remote"))
            # Follow the steps to setup SSH keys here: https://help.github.com/articles/generating-ssh-keys
            #git remote add origin https://{username}:{password}@github.com/{username}/project.git
            res = subprocess.call(['git', 'remote', 'set-url', 'origin',
                                   'https://' + self.config()['git_username'] + ':' + self.config()['git_password'] +
                                   '@github.com/' + self.config()['git_username'] + '/' + self.config()['git_project'] +
                                   '.git'])

            assert res == 0, 'Git command failed: ' + \
                             'git remote add origin https://{username}:{password}@github.com/{username}/project.git'

    def load(self, branch, tag):
        '''
        git checkout -b <branch>
        git checkout  tags/<tag>
        '''


        res = subprocess.call(['git', 'checkout', '-b', branch])
        assert res==0, 'Git command failed: ' + 'git checkout -b <branch>'

        res = subprocess.call(['git', 'checkout', 'tags/'+tag])
        assert res==0, 'Git command failed: ' + 'git checkout tags/<tag>'


