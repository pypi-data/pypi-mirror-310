import pytest
import logging

#Interesting note to API3
#The main benefit of using the listener API is that modifications can be done dynamically based on execution results or otherwise. 
#This allows, for example, interesting possibilities for model based testing.

# for pytest import as plugin 
# It use hooks for pytest https://docs.pytest.org/en/8.0.x/reference/reference.html#id56
# https://docs.pytest.org/en/8.0.x/reference/reference.html#test-running-runtest-hooks
# intro to pytetst hooks https://pytest-with-eric.com/hooks/pytest-hooks/

#for importing to Roboto FGRamework use 
#https://robot-framework.readthedocs.io/en/master/autodoc/robot.result.html#robot.result.resultbuilder.ExecutionResult
# or listener

#use external listener - http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#taking-listeners-into-use

# RF - adding keywords

class Log_Writer_Via_RFListener:
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    # when is loaded this library test is probably already started 
    #maybe this whole section shoudl be callecd from decorator?
    #def start_test(data, result):
    #    data.body.create_keyword(name='Log', args=['Keyword added by listener!'])
       
    def _start_keyword(self, data, result):
        a = data.body.create_keyword(name='Pytest Setup (_start_keyword)', args=['Keyword added by listener!'])
        b = data.body.create_keyword(name='Pytest Test (_start_keyword)', args=['Keyword added by listener!'])
        c = data.body.create_keyword(name='Pytest Teardown (_start_keyword)', args=['Keyword added by listener!'])
        logging.info('Created keyword object has these methods and atributes: ' + str(dir(a))) 

    def _end_keyword(self, data, result):
        # write all data from keyword to the logs
        #running model in data https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.Keyword
        #result model in result https://robot-framework.readthedocs.io/en/master/autodoc/robot.result.html#robot.result.model.Keyword.body
        a = data.body.create_keyword(name='Pytest Setup (_end_keyword)', args=['Keyword added by listener!'])
        b = data.body.create_keyword(name='Pytest Test (_end_keyword)', args=['Keyword added by listener!'])
        c = data.body.create_keyword(name='Pytest Teardown (_end_keyword)', args=['Keyword added by listener!'])
        logging.info('Created keyword object has these methods and atributes: ' + str(dir(a)))

class Log_Collector_From_Pytest:
    logs = []
    def __init__(self):
        self.log.append({'level':'info', 'message':'start collecting logs from pytest','timestamp':''})

    def collect_log(self,level,message):
        print('DEBUG ' + level + ' ' + message) # DEBUG LINE
        self.log.append({'level': level, 'message':message,'timestamp':''})

    def log_all_to_rf(self):
        for log in self.logs:
            if log['level'] == 'info':
                logging.info(log['message'])
            else:
                logging.info(log['message'])

@pytest.hookimpl()
def pytest_runtest_logfinish(nodeid, location, caplog):
    RFLogger = Log_Collector_From_Pytest
    RFLogger.collect_log('info', 'start pytets hook pytest_runtest_logfinish')
    for record in caplog.records:
        #log record docu https://docs.python.org/3/library/logging.html#logging.LogRecord
        RFLogger.collect_log('info', 'time: ' + record.asctime + '; ' record.levelname + ' ' + record.message)
    RFLogger.log_all_to_rf()
    #caplog.clear()

"""
pytest_runtest_protocol
#phases
pytest_runtest_setup
pytest_runtest_call
pytest_runtest_teardown
"""

#Pytest hooks for loging
""" 
pytest_runtest_protocol(item, nextitem)[source]
    Perform the runtest protocol for a single test item.

    The default runtest protocol is this (see individual hooks for full details):

    pytest_runtest_logstart(nodeid, location)

    Setup phase:
            call = pytest_runtest_setup(item) (wrapped in CallInfo(when="setup"))

            report = pytest_runtest_makereport(item, call)

            pytest_runtest_logreport(report)

            pytest_exception_interact(call, report) if an interactive exception occurred

    Call phase, if the the setup passed and the setuponly pytest option is not set:
            call = pytest_runtest_call(item) (wrapped in CallInfo(when="call"))

            report = pytest_runtest_makereport(item, call)

            pytest_runtest_logreport(report)

            pytest_exception_interact(call, report) if an interactive exception occurred

    Teardown phase:
            call = pytest_runtest_teardown(item, nextitem) (wrapped in CallInfo(when="teardown"))

            report = pytest_runtest_makereport(item, call)

            pytest_runtest_logreport(report)

            pytest_exception_interact(call, report) if an interactive exception occurred

            pytest_runtest_logfinish(nodeid, location)

    Parameters:
    item (Item) – Test item for which the runtest protocol is performed.

    nextitem (Optional[Item]) – The scheduled-to-be-next test item (or None if this is the end my friend).

    Stops at first non-None result, see firstresult: stop at first non-None result. The return value is not used, but only stops further processing.

"""




""" EXAMPLE how to initilize from library 
class LibraryItselfAsListener:
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    # Use the '_' prefix to avoid listener method becoming a keyword.
    def _end_suite(self, name, attrs):
        print(f"Suite '{name}' ending with status {attrs['id']}.")

    def example_keyword(self):
         ...
"""

# http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-examples
"""EXAMPLE - how to manipulate with results
from robot import result, running


class ResultModifier:

    def __init__(self, max_seconds: float = 10.0):
        self.max_seconds = max_seconds

    def start_suite(self, data: running.TestSuite, result: result.TestSuite):
        result.doc = 'Documentation set by listener.'
        # Information about tests only available via data at this point.
        smoke_tests = [test for test in data.tests if 'smoke' in test.tags]
        result.metadata['Smoke tests'] = len(smoke_tests)

    def end_test(self, data: running.TestCase, result: result.TestCase):
        elapsed_seconds = result.elapsed_time.total_seconds()
        if result.status == 'PASS' and  elapsed_seconds > self.max_milliseconds:
            result.status = 'FAIL'
            result.message = 'Test execution took too long.'

    def log_message(self, msg: result.Message):
        if msg.level == 'WARN' and not msg.html:
            msg.message = f'<b style="font-size: 1.5em">{msg.message}</b>'
            msg.html = True
"""

""" EXAMPLE - how to add test/keyword
def start_suite(data, result):
    data.tests.create(name='New test')

def start_test(data, result):
    data.body.create_keyword(name='Log', args=['Keyword added by listener!'])
"""
