from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod


@register_action
class AutoLabelAction(Action):
    name = 'label'
    category = PluginCategory.SMART_TOOL
    method = RunMethod.TASK

    def get_auto_label(self):
        return self.entrypoint(**self.params)

    def run_model(self, input_data):
        return {}

    def start(self):
        auto_label = self.get_auto_label()
        input_data = auto_label.handle_input(self.params['input_data'])
        output_data = self.run_model(input_data)
        return auto_label.handle_output(output_data)
