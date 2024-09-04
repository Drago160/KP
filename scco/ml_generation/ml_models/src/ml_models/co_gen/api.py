import configparser
from importlib.resources import files

from ml_models.gigachat_api_gate.api import GenerateGateWrapper
from ml_models.gigachat_api_gate.utils import UserMessageWrapper
from ml_models.co_gen.user_message_heuristic import UserMessageHeuristics

from ml_models.gigachat_api_gate.utils import Logger

from overrides import override

pos_to_insert_in_system = {
    'company_name': '[COMPANY]',
    'channel_name': '[CHANNEL]',
    'services': '[SERVICES]',
    'specific': '[SPECIFIC]',
    'tags': '[TAGS]'
}


def parse_custormer_services(request: dict):
    res_list = []
    for service in request['customer_services']:
        name, desc = service['service_name'], service['service_desc']
        res_list.append(name + f'({desc})')
    return ', '.join(res_list)


def make_system_prompt(request, path_to_conf):
    config = configparser.ConfigParser()
    config.read(path_to_conf)

    basic = config['PROMPTS']['main_system']

    basic = basic.replace(
        pos_to_insert_in_system['company_name'], request['company_name'])
    basic = basic.replace(
        pos_to_insert_in_system['channel_name'], request['channel_ids'][0])
    basic = basic.replace(
        pos_to_insert_in_system['services'], parse_custormer_services(request))
    basic = basic.replace(pos_to_insert_in_system['specific'], ', '.join(
        request['specific_features']))
    basic = basic.replace(pos_to_insert_in_system['tags'], ', '.join(
        request['tags']
    ))
    return basic


class COGenerator(GenerateGateWrapper):
    def __init__(self):
        Logger.print("Start constucting COGenerator", flush=True)
        cfg_path = 'co_gen/configs'
        params_config_path = str(
            files("ml_models").joinpath(
                cfg_path + "/params.ini"
            )
        )
        system_prompt_config_path = str(
            files("ml_models").joinpath(
                cfg_path+'/prompts.ini'
            )
        )
        Logger.print("Init basic model wrapper", flush=True)
        super().__init__(params_config_path, system_prompt_config_path)

        path_to_generate_cfg = str(
            files('ml_models').joinpath(
                cfg_path + '/prepare_params.ini'
            )
        )
        self.user_message_handler_heur = UserMessageHeuristics(
            path_to_generate_cfg)
        Logger.print("Finish constucting COGenerator", flush=True)

    def get_prepared_messages(self, request):
        Logger.print("Start preparing messges", flush=True)

        self._set_system_params(request, make_system_prompt)
        self.user_message_handler_heur(request)
        messages = self.system_prompts + \
            UserMessageWrapper.handle_messages(request['messages'])

        Logger.print("Finish preparing messages")
        return messages

    @override
    def generate(self, request) -> dict:
        Logger.print("Start Generate CO", flush=True)

        messages = self.get_prepared_messages(request)
        Logger.print("Get response from Gate", flush=True)
        response = self.gate.generate_request(messages)
        if (response.status_code != 200):
            raise Exception(
                f"GigaChat Gate returns response with status code: {response.status_code}")
        text_response = response.json()['choices'][0]['message']['content']
        result = {
            "main_text": text_response,  # api
        }

        Logger.print("Finish Generate CO")
        return result
