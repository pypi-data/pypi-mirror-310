import json
import os
import time
import threading
from typing import Union, Callable, Mapping

from cobweb import setting
from cobweb.base import (
    Seed,
    BaseItem,
    Request,
    Response,
    ConsoleItem,
    Decorators,
    TaskQueue,
)
from cobweb.constant import DealModel


class Crawler(threading.Thread):

    def __init__(self, stop, pause, custom_func: Union[Mapping[str, Callable]]):
        super().__init__()
        self.stop = stop
        self.pause = pause
        for func_name, _callable in custom_func.items():
            if isinstance(_callable, Callable):
                self.__setattr__(func_name, _callable)

        self.spider_max_retries = setting.SPIDER_MAX_RETRIES
        self.request_queue_size = setting.REQUEST_QUEUE_SIZE
        self.download_queue_size = setting.DOWNLOAD_QUEUE_SIZE
        self.upload_queue_size = setting.UPLOAD_QUEUE_SIZE

    @staticmethod
    def request(seed: Seed) -> Union[Request, BaseItem]:
        yield Request(seed.url, seed, timeout=5)

    @staticmethod
    def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
        response = item.download()
        yield Response(item.seed, response, **item.to_dict)

    @staticmethod
    def parse(item: Response) -> BaseItem:
        upload_item = item.to_dict
        upload_item["text"] = item.response.text
        yield ConsoleItem(item.seed, data=json.dumps(upload_item, ensure_ascii=False))

    # @decorators.add_thread()
    @Decorators.pause
    def build_request_item(self):
        thread_sleep = 0.1
        if TaskQueue.REQUEST.length >= self.request_queue_size:
            thread_sleep = 5
        elif seed := TaskQueue.TODO.pop():
            # member, priority = seed_info
            # seed = Seed(member, priority=priority)
            if seed.params.retry > self.spider_max_retries:
                TaskQueue.DOT.build(
                    topic=f"{os.getenv('PROJECT')}:{os.getenv('TASK')}",
                    process_task_type=seed.__class__.__name__,
                    seed_status=DealModel.fail,
                    retries=seed.params.retry,
                    **seed.to_dict
                )
            else:
                TaskQueue.process_task(seed, self.request)
            TaskQueue.DELETE.push(seed.seed)
        time.sleep(thread_sleep)

    @Decorators.pause
    def build_download_item(self):
        thread_sleep = 0.1
        if TaskQueue.RESPONSE.length >= self.download_queue_size:
            thread_sleep = 5
        elif request_item := TaskQueue.DOWNLOAD.pop():
            if request_item.params.retry > self.spider_max_retries:
                TaskQueue.DOT.build(
                    topic=f"{os.getenv('PROJECT')}:{os.getenv('TASK')}",
                    process_task_type=request_item.__class__.__name__,
                    retries=request_item.params.retry,
                    seed_status=DealModel.fail,
                    **request_item.to_dict
                )
                TaskQueue.DONE.push(request_item.seed)
            else:
                TaskQueue.process_task(request_item, self.download)
        time.sleep(thread_sleep)

    @Decorators.pause
    def build_parse_item(self):
        thread_sleep = 0.1
        if TaskQueue.UPLOAD.length >= self.upload_queue_size:
            thread_sleep = 5
        elif response_item := TaskQueue.RESPONSE.pop():
            if response_item.params.retry > self.spider_max_retries:
                TaskQueue.DOT.build(
                    topic=f"{os.getenv('PROJECT')}:{os.getenv('TASK')}",
                    process_task_type=response_item.__class__.__name__,
                    seed_status=DealModel.fail,
                    retries=response_item.params.retry,
                    **response_item.to_dict
                )
                TaskQueue.DONE.push(response_item.seed)
            else:
                TaskQueue.process_task(response_item, self.parse)
        time.sleep(thread_sleep)


