from mtmaisdk.clients.rest.models.workflow_list import WorkflowList

from mtmai.workflows.basicrag import BasicRagWorkflow
from mtmai.workflows.showtimer import DemoTimerFlow
from mtmai.workflows.wfapp import wfapp

# from mtmaisdk.hatchet import Hatchet


async def deploy_mtmai_workers():
    # 获取配置文件
    # response = httpx.get("http://localhost:8383/api/v1/worker/config")
    # hatchet = Hatchet(debug=True)

    list: WorkflowList = await wfapp.rest.aio.default_api.worker_config()
    worker = wfapp.worker("basic-rag-worker2")
    worker.register_workflow(BasicRagWorkflow())
    worker.register_workflow(DemoTimerFlow())

    worker.start()
