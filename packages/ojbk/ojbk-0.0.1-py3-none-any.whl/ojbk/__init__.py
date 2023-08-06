#!/usr/bin/env python
import codefast as cf
from typing import List, Dict, Tuple, Set, Optional
import datetime
from authc import get_redis
import json


class Base(object):
    pass


class Messager(object):
    def post(self, msg: Dict):
        pass


class MessageQueue(Messager):
    def __init__(self) -> None:
        super().__init__()
        self.queue = get_redis()
        self.name = '__MessageQUEUE__'

    def post(self, msg: Dict):
        self.queue.rpush(self.name, json.dumps(msg))

    def popall(self) -> List[Dict]:
        """ Get all messages from queue. 
        """
        results = []
        while True:
            msg = self.queue.lpop(self.name)
            if msg:
                results.append(json.loads(msg))
            if self.queue.llen(self.name) == 0:
                break
        return results


class EventReporter(object):
    def __init__(self, messager: Messager) -> None:
        self.messager = messager

    def report(self, msg: Dict) -> bool:
        self.messager.post(msg)


class TaskReporter(EventReporter):
    def __init__(self, task_name: str,
                 messager: Messager = MessageQueue()) -> None:
        super().__init__(messager)
        self.task_name = task_name

    def collect_info(self) -> str:
        hostname = cf.shell('hostname')
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {
            'task_name': self.task_name,
            'hostname': hostname,
            'date': date
        }

    def report_self(self) -> bool:
        self.report(self.collect_info())


if __name__ == '__main__':
    tr = TaskReporter('reporter')
    # for _ in range(10):
    # tr.report_self()
    msgs = tr.messager.popall()
    print(msgs)
