import time

import structlog
from mtmaisdk import Context
from openai import OpenAI

from mtmai.workflows.wfapp import wfapp

openai = OpenAI()
LOG = structlog.get_logger()


@wfapp.workflow(on_events=["showtimer"])
class DemoTimerFlow:
    @wfapp.step()
    def start(self, context: Context):
        context.put_stream("hello from DemoTimerFlow start")

        for i in range(10):
            context.put_stream(f"DemoTimerFlow start {i}\n")
            time.sleep(0.01)
        return {
            "status": "reading hatchet docs",
        }

    @wfapp.step(parents=["start"])
    def load_docs(self, context: Context):
        context.put_stream("hello from DemoTimerFlow load_docs")
        for i in range(10):
            context.put_stream(f"load_docs {i}\n")
            time.sleep(0.01)
        return {
            "status": "making sense of the docs",
        }
