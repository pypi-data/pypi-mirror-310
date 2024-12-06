# from mtmlib.mtutils import bash

from mtmai.workflows.workers import deploy_mtmai_workers


def register_worker_commands(cli):
    @cli.command()
    def worker():
        # print("starting workflow worker")
        # from mtmai.flows.deployments import start_prefect_deployment

        # start_prefect_deployment()

        deploy_mtmai_workers()

    # @cli.command()
    # def prefect():
    #     print("启动 prefect server")

    #     bash("sudo kill -9 $(lsof -t -i:4200) || true")
    #     bash(
    #         "prefect config set PREFECT_API_URL=https://colab-4200.yuepa8.com/api && prefect server start"
    #     )
