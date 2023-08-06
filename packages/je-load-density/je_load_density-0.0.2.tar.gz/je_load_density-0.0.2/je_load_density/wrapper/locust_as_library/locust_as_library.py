import gevent
import locust
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging

setup_logging("INFO", None)


def create_env(user_class: [locust.User]):
    env = Environment(user_classes=[user_class])
    env.create_local_runner()
    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)
    return env


def start_test(user_class: [locust.User], user_count: int = 50, spawn_rate: int = 10, test_time: int = 60,
               web_ui_dict: dict = None,
               **kwargs):
    env = create_env(user_class)
    env.runner.start(user_count, spawn_rate=spawn_rate)
    if web_ui_dict is not None:
        env.create_web_ui(web_ui_dict.get("host", "127.0.0.1"), web_ui_dict.get("port", "8089"))
    if test_time is not None:
        gevent.spawn_later(test_time, lambda: env.runner.quit())
    env.runner.greenlet.join()

