import re
import time
from typing import Any, overload
import requests
import logging

class GroqAgent():
    '''
    Create a GroqAgent object to interact with the Groq API.
    Automatically handles chat for the agent.
    '''
    def __init__(self,
        *,
        api_key: str,
        model: str | None = None,
        frequency_penalty: float | None = None,
        function_call: str | dict | None = None,
        functions: list | None = None,
        logit_bias: dict | None = None,
        logprobs: bool | None = None,
        max_tokens: int | None = None,
        n: int | None = None,
        parallel_tool_calls: bool | None = None,
        presence_penalty: float | None = None,
        response_format: dict | None = None,
        seed: int | None = None,
        stop: str | list | None = None,
        stream: bool | None = None,
        stream_options: dict | None = None,
        temperature: float | None = None,
        tool_choice: str | dict | None = None,
        tools: list | None = None,
        top_logprobs: int | None = None,
        top_p: float | None = None,
        user: str | None = None,
        # Custom parameters
        max_attempts: int | None = None,
        # Development parameters
        DEBUG: bool = False,
    ):
        '''
        Initialize the GroqAgent object with the settings.
        
        Args:
            Groq: API Parameters detailed in the OpenAI API documentation. https://console.groq.com/docs/api-reference#chat
            max_attempts (int): The maximum number of attempts to make the request.-1 for infinite attempts. 
        '''
        self.Set_Agent_Settings(api_key=api_key, model=model, frequency_penalty=frequency_penalty, function_call=function_call,
            functions=functions, logit_bias=logit_bias, logprobs=logprobs, max_tokens=max_tokens, n=n,
            parallel_tool_calls=parallel_tool_calls, presence_penalty=presence_penalty, response_format=response_format,
            seed=seed, stop=stop, stream=stream, stream_options=stream_options, temperature=temperature,
            tool_choice=tool_choice, tools=tools, top_logprobs=top_logprobs, top_p=top_p, user=user,
            
            # Custom parameters
            max_attempts=3,)
        self.chat_history: list = []
        self.DEBUG = DEBUG

    def Set_Agent_Settings(self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        frequency_penalty: float | None = None,
        function_call: str | dict | None = None,
        functions: list | None = None,
        logit_bias: dict | None = None,
        logprobs: bool | None = None,
        max_tokens: int | None = None,
        n: int | None = None,
        parallel_tool_calls: bool | None = None,
        presence_penalty: float | None = None,
        response_format: dict | None = None,
        seed: int | None = None,
        stop: str | list | None = None,
        stream: bool | None = None,
        stream_options: dict | None = None,
        temperature: float | None = None,
        tool_choice: str | dict | None = None,
        tools: list | None = None,
        top_logprobs: int | None = None,
        top_p: float | None = None,
        user: str | None = None,
        # Custom parameters
        max_attempts: int | None = None,
    ):
        '''
        Set the agent settings for the Groq API.
        
        Args:
            Groq: API Parameters detailed in the OpenAI API documentation. https://console.groq.com/docs/api-reference#chat
            max_attempts (int): The maximum number of attempts to make the request. -1 for infinite attempts. 
        '''
        self.api_key = api_key or getattr(self, 'api_key', None)
        self.model = model or getattr(self, 'model', None)
        self.frequency_penalty = frequency_penalty or getattr(self, 'frequency_penalty', None)
        self.function_call = function_call or getattr(self, 'function_call', None)
        self.functions = functions or getattr(self, 'functions', None)
        self.logit_bias = logit_bias or getattr(self, 'logit_bias', None)
        self.logprobs = logprobs or getattr(self, 'logprobs', None)
        self.max_tokens = max_tokens or getattr(self, 'max_tokens', None)
        self.n = n or getattr(self, 'n', None)
        self.parallel_tool_calls = parallel_tool_calls or getattr(self, 'parallel_tool_calls', None)
        self.presence_penalty = presence_penalty or getattr(self, 'presence_penalty', None)
        self.response_format = response_format or getattr(self, 'response_format', None)
        self.seed = seed or getattr(self, 'seed', None)
        self.stop = stop or getattr(self, 'stop', None)
        self.stream = stream or getattr(self, 'stream', None)
        self.stream_options = stream_options or getattr(self, 'stream_options', None)
        self.temperature = temperature or getattr(self, 'temperature', None)
        self.tool_choice = tool_choice or getattr(self, 'tool_choice', None)
        self.tools = tools or getattr(self, 'tools', None)
        self.top_logprobs = top_logprobs or getattr(self, 'top_logprobs', None)
        self.top_p = top_p or getattr(self, 'top_p', None)
        self.user = user or getattr(self, 'user', None)

        # Custom parameters
        self.max_attempts = max_attempts or getattr(self, 'max_attempts', None)

    # TODO: Remove this method in the next release.
    def ChatSettings(self,
        *,
        model: str | None = 'llama3-70b-8192',
        frequency_penalty: float | None = None,
        function_call: str | dict | None = None,
        functions: list | None = None,
        logit_bias: dict | None = None,
        logprobs: bool | None = None,
        max_tokens: int | None = None,
        n: int | None = None,
        parallel_tool_calls: bool | None = None,
        presence_penalty: float | None = None,
        response_format: dict | None = None,
        seed: int | None = None,
        stop: str | list | None = None,
        stream: bool | None = None,
        temperature: float | None = None,
        tool_choice: str | dict | None = None,
        tools: list | None = None,
        top_logprobs: int | None = None,
        top_p: float | None = None,
        user: str | None = None,
        extra_headers: Any | None = None,
        extra_query: Any | None = None,
        extra_body: Any | None = None,
        timeout: Any | None = None,
    ):
        '''
        DEPRECATED: Use Set_Agent_Settings instead.

        extra_headers, extra_query, extra_body, timeout are not used in this method.
        '''
        self.Set_Agent_Settings(model=model, frequency_penalty=frequency_penalty, function_call=function_call,
            functions=functions, logit_bias=logit_bias, logprobs=logprobs, max_tokens=max_tokens, n=n,
            parallel_tool_calls=parallel_tool_calls, presence_penalty=presence_penalty, response_format=response_format,
            seed=seed, stop=stop, stream=stream, temperature=temperature, tool_choice=tool_choice, tools=tools,
            top_logprobs=top_logprobs, top_p=top_p, user=user)

    def SystemPrompt(self, prompt: str):
        '''
        Use this method to add a system prompt to the chat history altering how the agent responds.
        example: 'Respond as a personal assistant.' or 'Respond as a customer service agent.'
        '''
        self.chat_history.append({
            "role": "system",
            "content": prompt
        })

    def Chat(self, message: str, *, remember: bool = True, verbose: bool = False) -> str | dict:
        '''
        Chat with the agent. The agent will respond to the message.

        Args:
            message (str): The message to send to the agent.
            remember (bool): Whether to remember the chat history. Default is True.
            verbose (bool): Whether to return the full response. Default is False.

        Returns:
            str | dict: The response message from the agent.
                str: If verbose is False, only the response message is returned.
                dict: If verbose is True, the full response is returned.
        '''
        response = self._post(messages=[*self.chat_history, {"role": "user", "content": message}])
        response_message = response['choices'][0]['message']
        if remember:
            self.chat_history.append({"role": "user", "content": message})
            self.chat_history.append(response_message)
        
        if verbose:
            return response
        return response_message['content']

    def _post(self, *, messages: list = None) -> dict:
        '''
        POST request to the Groq API.
        '''
        URL = 'https://api.groq.com/openai/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

        if self.function_call:
            logging.warning('\'function_call\' is Deprecated')
        if self.functions:
            logging.warning('\'functions\' is Deprecated')
        if self.logit_bias:
            logging.warning('\'logit_bias\' is not yet supported')
        if self.logprobs:
            logging.warning('\'logprobs\' is not yet supported')
        if self.n:
            logging.warning('\'n\' only supports n=1')
        if self.tool_choice:
            logging.warning('\'tool_choice\' disabled')
        if self.tools:
            logging.warning('\'tools\' disabled')
        if self.top_logprobs:
            logging.warning('\'top_logprobs\' is not yet supported')

        body = {
            'messages': messages,
            'model': self.model,
            'frequency_penalty': self.frequency_penalty,
            # 'function_call': self.function_call, # Deprecated on API
            # 'functions': self.functions, # Deprecated on API
            # 'logit_bias': self.logit_bias, # not yet supported on API
            # 'logprobs': self.logprobs, # not yet supported on API
            'max_tokens': self.max_tokens,
            # 'n': self.n, # only support n=1 on API
            'parallel_tool_calls': self.parallel_tool_calls,
            'presence_penalty': self.presence_penalty,
            'response_format': self.response_format,
            'seed': self.seed,
            'stop': self.stop,
            'stream': self.stream,
            'stream_options': self.stream_options,
            'temperature': self.temperature,
            # 'tool_choice': self.tool_choice, # not working
            # 'tools': self.tools, # not working
            # 'top_logprobs': self.top_logprobs,# not yet supported on API
            'top_p': self.top_p,
            'user': self.user,
        }

        # NOTE: This 'while' loop should not be broken using 'break' keyword.
        # NOTE: Must 'return' or 'raise' to exit the loop and a 'continue' keyword must be used for looping.
        attempt = 0
        # NOTE: If max_attempts is -1, it will loop infinitely.
        while attempt != self.max_attempts:
            attempt += 1

            response = requests.post(URL, headers=headers, json=body)

            # Handle HTTP errors separately
            try:
                response.raise_for_status()
            # HTTP error handling
            except requests.exceptions.HTTPError as e:
                content: dict

                content = response.json()
                content_error = content.get('error', None)
                messages = content_error.get('message', None)
                error_type = content_error.get('type', None)
                error_code = content_error.get('code', None)

                t_regex = r'Limit (?P<limit>\d*).*?Used (?P<used>\d*).*?Requested (?P<requested>\d*).*?Please try again in ((?P<m>\d)m)?((?P<s>\d*\.?\d*?)s)?((?P<ms>\d*\.?\d*?)ms)?'
                # Rate limit exceeded for tokens and requests error handling
                if error_code == 'rate_limit_exceeded':
                    match = re.search(t_regex, messages)
                    if not match:
                        raise e
                    limit = match.group('limit')
                    # used = match.group('used')
                    requested = match.group('requested')
                    limit_wait_m = match.group('m') or 0 # minutes
                    limit_wait_m_in_s = int(limit_wait_m) * 60 # minutes in seconds
                    limit_wait_s = float(match.group('s') or 0) # seconds
                    limit_wait_ms = match.group('ms') or 0 # milliseconds
                    limit_wait_ms_in_s = float(limit_wait_ms) / 1000 # milliseconds in seconds
                    waiting_time_seconds = limit_wait_m_in_s + limit_wait_s + limit_wait_ms_in_s

                    # If requested tokens exceed the maximum limit, raise an exception
                    #NOTE: This only happens on excessive token requests
                    if requested > limit:
                        raise Exception(f'Request of \'{requested}\' exceeds the maximum limit of \'{limit}\'')

                    logging.warning(f'Attempt {attempt} - {messages}')
                    print(self.DEBUG)
                    if self.DEBUG:
                        while waiting_time_seconds > 0:
                            print(f' Waiting for {waiting_time_seconds} seconds...   ', end='\r')
                            time.sleep(min(1, waiting_time_seconds))
                            waiting_time_seconds -= 1
                        continue
                    else:
                        time.sleep(waiting_time_seconds); continue
                
                # Unknown error handling
                logging.error(content)
                raise e
                
            # Other exceptions
            except Exception as e:
                logging.error(str(e), exc_info=True)
                raise e
            
            # Rate limit info
            rate_limit_info = {
                'max_requests': response.headers.get('x-ratelimit-limit-requests'),
                'max_tokens': response.headers.get('x-ratelimit-limit-tokens'),
                'remaining_requests': response.headers.get('x-ratelimit-remaining-requests'),
                'remaining_tokens': response.headers.get('x-ratelimit-remaining-tokens'),
                'reset_requests': response.headers.get('x-ratelimit-reset-requests'),
                'reset_tokens': response.headers.get('x-ratelimit-reset-tokens'),
            }

            return_response = response.json()
            return_response['rate_limit'] = rate_limit_info
            return return_response
        
            # NOTE: NEVER REMOVE THIS ERROR CHECK EVEN IF THE CODE IS UNREACHABLE
            raise Exception('Loop auto looped. \'continue\' must be used to loop.')
        
        if attempt == self.max_attempts: # If the loop reaches the max attempts
            raise Exception('Max attempts reached. Unable to get valid response from API.')
        raise Exception('Loop exited. \'return\' or \'raise\' must be used to exit the loop.')
