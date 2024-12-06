import logging
import random
import string
import time
from functools import wraps
from importlib import import_module
from typing import Callable, Dict, List, Optional, Type

import json5
import pyparsing as pp
from pydantic import ValidationError, BaseModel

from duowen_agent.error import ObserverException

logger = logging.getLogger(__name__)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.

    Args:
        dotted_path: eg promptulate.schema.MessageSet

    Returns:
        Class corresponding to dotted path.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (module_path, class_name)) from err


def listdict_to_string(data: List[Dict], prefix: Optional[str] = "", suffix: Optional[str] = "\n",
                       item_prefix: Optional[str] = "", item_suffix: Optional[str] = ";\n\n",
                       is_wrap: bool = True, ) -> str:
    """Convert List[Dict] type data to string type"""
    wrap_ch = "\n" if is_wrap else ""
    result = f"{prefix}"
    for item in data:
        temp_list = ["{}:{} {}".format(k, v, wrap_ch) for k, v in item.items()]
        result += f"{item_prefix}".join(temp_list) + f"{item_suffix}"
    result += suffix
    return result[:-2]


def generate_unique_id() -> str:
    timestamp = int(time.time() * 1000)
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=6))

    unique_id = f"dw-{timestamp}-{random_string}"
    return unique_id


def convert_backslashes(path: str):
    """Convert all \\ to / of file path."""
    return path.replace("\\", "/")


def hint(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ret = fn(*args, **kwargs)
        logger.debug(f"function {fn.__name__} is running now")
        return ret

    return wrapper


def record_time():
    def decorator(fn: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            start_time = time.time()
            ret = fn(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"[duowen-agent timer] <{fn.__name__}> run {duration}s")
            return ret

        return wrapper

    return decorator


def retrying(_func, _max_retries=3, **kwargs):
    for attempt in range(_max_retries):
        try:
            return _func(**kwargs)
        except ObserverException:
            if attempt == _max_retries - 1:
                raise
            else:
                time.sleep(0.1)
                continue
        except Exception as e:
            raise


def extract(llm_response: str, extract_type='json') -> str:
    _block = pp.Suppress(pp.Literal('```')) + pp.Suppress(
        pp.Optional(pp.Keyword(extract_type, caseless=True))) + pp.SkipTo(pp.Literal('```')) + pp.Suppress(
        pp.Literal('```'))

    _text = _block.search_string(llm_response)
    if _text:
        return _text[0][0]
    else:
        return llm_response


def json_observation(content: str, pydantic_obj: Type[BaseModel]):
    _data = extract(content, 'json')

    if not _data.strip():
        _data = content

    try:
        _data1 = json5.loads(_data)
    except ValueError as e:
        raise ObserverException(predict_value=content, expect_value="json格式数据",
                                err_msg=f"observation error jsonload, msg: {str(e)}")
    try:
        return pydantic_obj(**_data1)
    except ValidationError as e:
        raise ObserverException(predict_value=content, expect_value=str(self.pydantic_obj.model_json_schema()),
                                err_msg=f"observation error ValidationError, msg: {str(e)}")
