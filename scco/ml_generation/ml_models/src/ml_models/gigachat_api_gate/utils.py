from typing import List


class UserMessageWrapper:
    @staticmethod
    def handle_message(message: str):
        return {
            "role": "user",
            "content": message
        }

    @staticmethod
    def handle_messages(messages: List[str]):
        Logger.print("Start pack messages", flush=True)
        res = [UserMessageWrapper.handle_message(
            message) for message in messages]
        Logger.print("End pack messages", flush=True)
        return res


class Logger:
    @staticmethod
    def print(message: str, flush=None):
        if (flush is None):
            flush = True
        print(message, flush=flush)
        # print()
        # print('-'*100)
        # print(flush=flush)
