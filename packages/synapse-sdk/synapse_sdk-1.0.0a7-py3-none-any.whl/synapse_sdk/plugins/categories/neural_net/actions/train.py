from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod
from synapse_sdk.plugins.models import Run


class TrainRun(Run):
    def log_metric(self, x, i, **kwargs):
        self.log(x, {x: i, **kwargs})

    def log_model(self, files, status=None):
        pass


@register_action
class TrainAction(Action):
    name = 'train'
    category = PluginCategory.NEURAL_NET
    method = RunMethod.JOB
    run_class = TrainRun

    def get_dataset(self):
        return {}

    def start(self):
        hyperparameter = self.params['hyperparameter']

        # download dataset
        self.run.log_event('Preparing dataset for training.')
        input_dataset = self.get_dataset()

        # train dataset
        self.run.log_event('Starting model training.')

        model_files = self.entrypoint(self.run, input_dataset, hyperparameter)

        # upload model_data
        self.run.log_event('Registering model data.')

        self.run.end_log()
        return model_files
