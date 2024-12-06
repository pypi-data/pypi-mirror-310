import time
from abc import ABC, abstractmethod
from collections import deque
from typing import Union, List, Optional, Type

from duowen_agent.error import ObserverException
from duowen_agent.llm.chat_model import OpenAIChat
from duowen_agent.llm.embedding_model import OpenAIEmbedding, EmbeddingCache
from duowen_agent.llm.entity import MessagesSet
from duowen_agent.llm.rerank_model import GeneralRerank
from duowen_agent.rag.retrieval.retrieval import Retrieval
from duowen_agent.tools.toolkit import Toolkit
from duowen_agent.utils.string_template import StringTemplate
from pydantic import BaseModel
from redis import StrictRedis
from sqlalchemy import Engine


class BaseAgent(ABC):

    def __init__(self, llm: OpenAIChat = None, retrieval_instance: Retrieval = None,
                 embedding_instance: Union[EmbeddingCache, OpenAIEmbedding] = None, redis_instance: StrictRedis = None,
                 sql_instance: dict[str:Engine] = None, rerank_model: GeneralRerank = None, callback: deque = None,
                 tools: Optional[List[Toolkit]] = None, agents: Optional[List['BaseAgent']] = None,
                 output_schema: Optional[Union[Type[BaseModel], StringTemplate, dict, str]] = None, **kwargs):

        self.llm = llm
        self.retrieval_instance = retrieval_instance
        self.embedding_instance = embedding_instance
        self.rerank_model = rerank_model
        self.redis_instance = redis_instance
        self.sql_instance = sql_instance
        self.callback = callback
        self.tools = tools
        self.agents = agents
        self.output_schema = output_schema
        self.kwargs = kwargs

    @staticmethod
    def retrying(_func, max_retries: int = 3, except_list: List[Exception] = None, **kwargs):

        if not except_list:
            _except_list = [ObserverException]
        else:
            _except_list = except_list

        _cnt = max_retries

        for attempt in range(max_retries):
            try:
                return _func(**kwargs)
            except _except_list as e:
                if _cnt == 1:
                    raise
                time.sleep(0.1)
            except Exception as e:
                raise

    def put_callback(self, item):
        if self.callback:
            self.callback.append(item)

    @abstractmethod
    def build_prompt(self):
        ...

    @abstractmethod
    def chat(self, user_input: Union[MessagesSet, str], **kwargs):
        ...
