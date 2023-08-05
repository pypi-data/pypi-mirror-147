import pytest
from common.plugin.data_bus import DataBus
from loguru import logger


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    每个测试用例执行后，制作测试报告
    :param item: 测试用例对象
    :param call: 测试用例的测试步骤
            先执行when=’setup’ 返回setup 的执行结果
            然后执行when=’call’ 返回call 的执行结果
            最后执行when=’teardown’返回teardown 的执行结果
    :return:
    """
    out = yield
    report = out.get_result()
    if report.when == "call":
        testname=item.__dict__['keywords'].__dict__['_markers']['__allure_display_name__']
        logger.info(testname)


@pytest.fixture(scope="session", autouse=True)
def fix_session():
    """
    1. 数据初始化，在所有用例文件/用例执行之前，统一从qamp拿到配置好的测试数据，共享给所有用例使用

    2. scope = session 代表一次执行，若包含多个用例文件，则可跨用例文件调用，该装饰器下的函数，会在所有用例文件
                    执行之前执行

            -function：每一个函数或方法都会调用

            -class：每一个类调用一次，一个类中可以有多个方法

            -module：每一个.py文件调用一次，该文件内又有多个function和class
    :return:
    """
    logger.info("数据初始化")
    DataBus.save_init_data()
    yield
    logger.info("数据清理")
