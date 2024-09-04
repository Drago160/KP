from typing import Any
import configparser

from ml_models.co_gen.matcher import Matcher
from ml_models.gigachat_api_gate.utils import Logger


def parse_word(string, idx):
    end = idx
    while string[end] != ' ':
        end += 1
        if end >= len(string):
            break
    return string[idx:end]


class UserMessageCutHandler:
    def __init__(self, path_to_generate_cfg):
        Logger.print('Construct UserMessageCatHandler')

        self.matcher = Matcher()
        self.DEFAULT_MESSAGE = "Добрый день. Нужно реализовать проект."
        config = configparser.ConfigParser()
        config.read(path_to_generate_cfg)

        self.need_generate_bound = int(
            config['CUT_MESSAGE']['need_generate_bound'])
        self.max_matched_bound = int(
            config['CUT_MESSAGE']['max_matched_bound'])
        self.max_messages_size = int(
            config['CUT_MESSAGE']['max_messages_size'])
        self.min_messages_size = int(
            config['CUT_MESSAGE']['min_messages_size'])
        self.direction = config['CUT_MESSAGE']['direction']
        assert self.direction in ['END', 'BEGIN']

        Logger.print('Finish Construct UserMessageHandler')

        self.not_gen_flag = False

    def calc_new_len(self, length, matches):
        matches = min(matches, self.max_matched_bound)
        delta_matched = matches - self.need_generate_bound
        delta_sizes = self.max_messages_size - self.min_messages_size
        size_delta_to_match = delta_sizes / \
            (self.max_matched_bound - self.need_generate_bound)
        return int(min(length, self.min_messages_size + delta_matched*size_delta_to_match))

    def __call__(self, request):

        messages = request['messages']
        matches = 0
        concated_messages = ''.join(messages)
        for keyword in request['white_list']:
            if (self.matcher.count_matches(keyword, concated_messages) > 0):
                matches += 1
        if matches <= self.need_generate_bound:
            self.not_gen_flag = True
            request['messages'] = [self.DEFAULT_MESSAGE]
            return

        sum_len = min(len(concated_messages), self.max_messages_size)
        sum_len = self.calc_new_len(sum_len, matches)

        result_messages = []
        if self.direction == 'END':
            messages = list(reversed(messages))
        for message in messages:
            result_messages.append(message)
            if sum_len < len(message):
                result_messages[-1] = result_messages[-1][:sum_len]
                break
            sum_len -= len(message)
        if self.direction == 'END':
            result_messages = list(reversed(result_messages))
        request['messages'] = result_messages


class AddToLastMessageHandler:
    def __init__(self, path_to_generate_cfg):
        Logger.print("Construct AddToLastMessageHandler")

        self.matcher = Matcher()
        config = configparser.ConfigParser()
        config.read(path_to_generate_cfg)

        self.keyword_message_pad = config['EDIT_USER_MESSAGE']['add_to_end']

        Logger.print("Finish construct AddToLastMessageHandler")

    def __call__(self, request):
        Logger.print("Call AddToLastMessageHandler")
        tags = ', '.join(request['tags'])
        pad_to_end = self.keyword_message_pad.replace('[TAGS]', tags)
        request['messages'][-1] += pad_to_end


class UserMessageHeuristics:
    def __init__(self, path_to_generate_cfg):
        Logger.print("Construct UserMessageHeuristics")

        self.cut_heur = UserMessageCutHandler(path_to_generate_cfg)
        self.add_heur = AddToLastMessageHandler(path_to_generate_cfg)
        self.matcher = Matcher()
        self.buff = dict

        Logger.print("Finish Construct UserMessageHeuristics")

    def __call__(self, request):
        self.cut_heur(request)
        self.add_heur(request)
