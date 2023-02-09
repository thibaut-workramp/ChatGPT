import logging
import time

import openai

from utils import concat_strs
from api_keys_provider import OpenAIAPIKeysProvider


class BaseTaskSolverBot(object):
    """
    Base bot which is an openai models api call wrapper.
    Template class for all subclass designed to solve a specific task, given the task description and
    input with expected output examples
    """

    examples = tuple()     # tuple of dict examples ({input, output}, ...)

    # default params for the openai API. We can override them in a subclass, or at runtime at each call to the bot (__call__)
    default_model = 'code-davinci-002'
    default_temperature = 0.
    default_max_tokens = 256
    default_top_p = 1.0
    default_frequency_penalty = 0.0
    default_presence_penalty = 0.0
    stop = '#'   # the char used to stop the completion

    @classmethod
    def examples_separator(cls) -> str:
        return f'{cls.stop}\n'

    @staticmethod
    def encode_input(example_input):
        return f"""\
Q: "{example_input}"
A: \
"""

    @staticmethod
    def encode_example_output(example_output):
        return example_output

    @staticmethod
    def decode_output(example_output):
        return example_output

    # Description of the problem
    def build_task_description(self):
        return ''

    @classmethod
    def encode_example(cls, example: dict) -> str:
        _input = cls.encode_input(example['input'])
        _output = cls.encode_example_output(example['output'])
        encoded_example = f"{_input}{_output}"
        return encoded_example

    @classmethod
    def encode_examples(cls) -> str:
        encoded_examples = concat_strs([f'{cls.encode_example(example)}{cls.examples_separator()}' for example in cls.examples])
        return encoded_examples

    def build_prompt_prefix(self, **kwargs):
        encoded_examples = self.encode_examples()
        prompt_prefix = f"""\
{self.build_task_description(**kwargs)}

Examples:

{encoded_examples}"""
        logging.debug(f"prompt prefix sent everytime to the openai api, concatenate before the nl_query:\n{'-' * 80}\n{prompt_prefix}{'-' * 80}")
        return prompt_prefix

    @classmethod
    def encode_one_history_elem(cls, hist_elem: dict) -> str:
        encoded_history_elem = f'{cls.encode_input(hist_elem["nl_query"])}{hist_elem["response"]}'
        return encoded_history_elem

    def encode_history(self):
        encoded_history = concat_strs([f'{self.encode_one_history_elem(hist_elem)}{self.examples_separator()}' for hist_elem in self.history])
        return encoded_history

    def build_prompt(self, nl_query, with_history=False, **kwargs):
        prompt = f"""\
{self.build_prompt_prefix(**kwargs)}\
{self.encode_history() if with_history else ''}\
{self.encode_input(nl_query)}\
"""
        logging.debug(f"prompt:\n{'-' * 80}\n{prompt}{'-' * 80}")
        return prompt

    def __init__(self):
        self.history = []   # keep conversation history, to send it or not at the next request (or not)

    def __call__(
        self,
        nl_query: str,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        top_p: float = None,
        frequency_penalty: float = None,
        presence_penalty: float = None,
        stop=None,
        send_history=False,   # if True, the past of the discussion is sent to the openai model
        nsec_before_retry: float = 2,
        decode_output=False,
        **kwargs,
    ):
        logging.info(f'nl_query: {nl_query}')

        prompt = self.build_prompt(nl_query, with_history=send_history, **kwargs)

        nb_retry = 0
        start = time.time()
        while True:
            try:
                api_key = OpenAIAPIKeysProvider.get()
                openai.api_key = api_key
                response = openai.Completion.create(
                    model=model if model is not None else self.default_model,
                    prompt=prompt,
                    temperature=temperature if temperature is not None else self.default_temperature,
                    max_tokens=max_tokens if max_tokens is not None else self.default_max_tokens,
                    top_p=top_p if top_p is not None else self.default_top_p,
                    frequency_penalty=frequency_penalty if frequency_penalty is not None else self.default_frequency_penalty,
                    presence_penalty=presence_penalty if presence_penalty is not None else self.default_presence_penalty,
                    stop=self.stop,
                )
                break
            except openai.error.RateLimitError as e:
                if nsec_before_retry is None:
                    raise e
                else:
                    nb_retry += 1
                    if nb_retry % len(OpenAIAPIKeysProvider.api_keys_list) == 0:
                        logging.error(f"Sorry I'm too busy... . Ok I will retry in {nsec_before_retry} seconds...")
                        time.sleep(nsec_before_retry)
        duration = time.time() - start

        logging.debug(f'full response:\n{response}')
        response = response["choices"][0]["text"]

        self.history.append({'nl_query': nl_query, 'response': response})

        if decode_output:
            response = self.decode_output(response)

        nb_retry_msg = f"    (nb retry: {nb_retry})" if nb_retry > 0 else ""
        logging.info(f"response  (time: {round(duration, 3)}s){nb_retry_msg}: {response}")

        return response

    def from_standard_input(self):
        nl_query = input("Hi ! Try to suggest a dataset filter query in natural langage:\n")
        while True:
            if nl_query == "exit":
                break
            else:
                self(nl_query)
            nl_query = input("\n")
