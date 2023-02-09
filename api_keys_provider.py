import os
from collections import deque


class OpenAIAPIKeysProvider(object):
    """
    Class that can provide openai API keys, rototaing the keys at each call
    Available keys must be set in traditional OPENAI_API_KEY env var, and
    then all the others in OPEN_API_KEY_2, OPEN_API_KEY_3 ...
    """

    api_keys_list = ['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']
    if 'OPENAI_API_KEY' in os.environ.keys():  # default api key
        api_keys_list.append(os.environ['OPENAI_API_KEY'])
    for i in range(2, 10):  # try to add additional api keys
        if f'OPENAI_API_KEY_{i}' in os.environ.keys():
            api_keys_list.append(os.environ[f'OPENAI_API_KEY_{i}'])
    print(f'api_keys_list: {api_keys_list}')
    api_keys = deque(api_keys_list)

    @classmethod
    def get(cls):
        api_key = cls.api_keys[0]
        cls.api_keys.rotate(-1)
        return api_key
