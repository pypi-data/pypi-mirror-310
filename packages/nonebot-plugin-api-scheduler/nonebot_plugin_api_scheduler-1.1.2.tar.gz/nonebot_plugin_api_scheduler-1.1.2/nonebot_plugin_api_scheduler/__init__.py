import nonebot
from nonebot.log import logger
from nonebot.drivers import ASGIMixin
from nonebot.plugin import PluginMetadata
from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI

# 插件元信息
__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-api-scheduler",
    description="像操作API一样设置定时任务&计划任务",
    usage="https://github.com/mmdexb/nonebot-plugin-api-scheduler/blob/master/README.md",
    type="application",
    homepage="https://github.com/mmdexb/nonebot-plugin-api-scheduler/",
    supported_adapters={"~onebot.v11"},
)

# 定义数据模型
class TimerModel(BaseModel):
    timestamp: str  # 格式: "2024-10-18 18:00:00"
    content: str
    img_url: str
    qqgroup_id: str
    is_at_all: bool


class SchedulerModel(BaseModel):
    day: int
    hour: int
    minute: int
    second: int
    content: str
    img_url: str
    qqgroup_id: str
    is_at_all: bool

scheduler = None
# 获取调度器
try:
    scheduler = nonebot.require("nonebot_plugin_apscheduler").scheduler
    print("已加载 nonebot_plugin_api_scheduler")
except Exception:
    scheduler = None
    logger.error("请先安装 nonebot_plugin_apscheduler 插件")

# 判断是否为 ASGI 驱动并包含 FastAPI
driver = nonebot.get_driver()
if isinstance(driver, ASGIMixin) and isinstance(nonebot.get_app(), FastAPI) and scheduler is not None:
    from fastapi.security import HTTPBasic, HTTPBasicCredentials
    from fastapi.responses import HTMLResponse
    from fastapi import FastAPI, Depends, HTTPException, status

    app: FastAPI = nonebot.get_app()
    security = HTTPBasic()

    # 定时任务接口
    @app.post("/scheduler/timer")
    async def scheduler_timer(timer: TimerModel):
        try:
            run_time = datetime.strptime(timer.timestamp, "%Y-%m-%d %H:%M:%S")
            scheduler.add_job(
                do_send, "date", run_date=run_time,
                args=[list(nonebot.get_bots().values())[0], timer.content,
                      timer.img_url, timer.qqgroup_id, timer.is_at_all]
            )
        except IndexError:
            return {"code": 500, "msg": "机器人未上线"}
        return {"code": 200, "msg": "任务已设定"}

    # 周期任务接口
    @app.post("/scheduler/plan")
    async def scheduler_plan(plan: SchedulerModel):
        try:
            scheduler.add_job(
                do_send, "cron", day=f'*/{plan.day}', hour=plan.hour,
                minute=plan.minute, second=plan.second,
                args=[list(nonebot.get_bots().values())[0], plan.content,
                      plan.img_url, plan.qqgroup_id, plan.is_at_all]
            )
        except IndexError:
            return {"code": 500, "msg": "机器人未上线"}
        return {"code": 200, "msg": "任务已设定"}

    # 取消任务接口
    @app.get("/scheduler/cancel")
    async def scheduler_cancel(job_id: str):
        scheduler.remove_job(job_id)
        return {"code": 200, "msg": "任务已取消"}

    # 任务列表接口
    @app.get("/scheduler/list")
    async def scheduler_list():
        jobs = scheduler.get_jobs()
        job_list = []
        for job in jobs:
            send_what = f"{job.args[1]}\n"
            if job.args[2]:
                send_what += f"{job.args[2]}\n"
            if job.args[4]:
                send_what += "@全体成员"
            job_list.append({
                "id": job.id,
                "name": job.name,
                "send_what": send_what,
                "send_to": job.args[3],
                "next_run_time": job.next_run_time.strftime("%Y-%m-%d %H:%M:%S") if job.next_run_time else None,
                "trigger": str(job.trigger)
            })
        return {"code": 200, "msg": "任务列表", "data": job_list}

    # 身份认证
    def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
        # 请在此修改面板账户密码
        correct_username = "admin"
        correct_password = "admin"
        if (credentials.username != correct_username or
                credentials.password != correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )

    # 管理面板接口
    @app.get("/dashboard", response_class=HTMLResponse, dependencies=[Depends(authenticate)])
    async def dashboard():
        with open("dashboard.html", "r", encoding="utf-8") as html_file:
            return html_file.read()
else:
    if not isinstance(driver, ASGIMixin):
        logger.warning("当前驱动不支持 ASGI。请切换到支持 ASGI 的驱动（如 fastapi）。")
    if scheduler is None:
        logger.warning("未找到 nonebot_plugin_apscheduler，请先安装该插件。")
