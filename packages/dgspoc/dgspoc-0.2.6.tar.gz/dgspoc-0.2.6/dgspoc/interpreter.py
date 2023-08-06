"""Module containing the logic for describe-get-system to interpret
user describing problem"""


import re
import operator
import yaml
import time

from textwrap import indent
from textwrap import dedent
from textwrap import wrap

from dgspoc.utils import DotObject
from dgspoc.utils import Misc
# from dgspoc.utils import File
from dgspoc.utils import Text

from dgspoc.constant import FWTYPE

# from dgspoc import parser
from dgspoc.parser import ParsedOperation
from dgspoc.parser import CheckStatement

from dgspoc.exceptions import NotImplementedFrameworkError
from dgspoc.exceptions import ComparisonOperatorError
from dgspoc.exceptions import ConnectDataStatementError
from dgspoc.exceptions import UseTestcaseStatementError
from dgspoc.exceptions import ConnectDeviceStatementError
from dgspoc.exceptions import DisconnectDeviceStatementError
from dgspoc.exceptions import ReleaseDeviceStatementError
from dgspoc.exceptions import ReleaseResourceStatementError
from dgspoc.exceptions import WaitForStatementError
from dgspoc.exceptions import PerformerStatementError
from dgspoc.exceptions import VerificationStatementError


class ScriptInfo(DotObject):
    def __init__(self, *args, testcase='', **kwargs):
        super().__init__(*args, **kwargs)
        self.testcase = testcase
        self.devices_vars = dict()
        self.variables = dict(
            test_resource_var='test_resource',
            test_resource_ref='',
            test_data_var='test_data'
        )
        self._enabled_testing = False

    @property
    def is_testing_enabled(self):
        return self._enabled_testing

    def enable_testing(self):
        self._enabled_testing = True

    def disable_testing(self):
        self._enabled_testing = False

    def load_testing_data(self):
        if not self.is_testing_enabled:
            return

        data = """
            devices:
              1.1.1.1:
                name: device1
              1.1.1.2:
                name: device2
            testcases:
              test1:
                ref_1: blab blab
                script_builder:
                  class_name: Testcase1
                  test_precondition: precondition
                  test_case1: case1
                  test_case2: case2
              test2:
                ref_2: blab blab
                script_builder:
                  class_name: Testcase2
                  test_precondition: precondition
                  test_case1: case1
                  test_case2: case2
        """
        self.update(yaml.safe_load(data))

    def get_class_name(self):
        if 'testcases' in self:
            node = self.testcases.get(self.testcase)
            cls_name = node.get('class_name', 'TestClass') if node else 'TestClass'
            return cls_name
        else:
            return 'TestClass'

    def reset_devices_vars(self):
        self.devices_vars = dict()

    def reset_global_vars(self):
        self.variables = dict(
            test_resource_var='test_resource',
            test_resource_ref='',
            test_data_var='test_data'
        )

    def get_device_var(self, device_name):

        for var_name, var_val in self.devices_vars.items():
            if var_val == device_name:
                return var_name
        else:
            return 'not_found_var for %r' % device_name


SCRIPTINFO = ScriptInfo()


class Statement:
    def __init__(self, data, parent=None, framework='', indentation=4):
        self.data = data
        self.prev = None
        self.next = None
        self.current = None
        self.parent = parent
        self.framework = str(framework).strip()
        self._children = []
        self._name = ''
        self._is_parsed = False

        self._stmt_data = ''
        self._remaining_data = ''

        self._prev_spacers = ''
        self._spacers = ''
        self._level = 0
        self.indentation = indentation

        self.spacer_pattern = r'(?P<spacers> *)[^ ].*'

        self.validate_framework()
        self.prepare()

    def __len__(self):
        return 1 if self.name != '' else 0

    @property
    def is_parsed(self):
        return self._is_parsed

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def children(self):
        return self._children

    @property
    def level(self):
        return self._level

    @property
    def is_unittest(self):
        return self.framework == FWTYPE.UNITTEST

    @property
    def is_pytest(self):
        return self.framework == FWTYPE.PYTEST

    @property
    def is_robotframework(self):
        return self.framework == FWTYPE.ROBOTFRAMEWORK

    @property
    def is_not_robotframework(self):
        return not self.is_robotframework

    @property
    def is_empty(self):
        return self.data.strip() == ''

    @property
    def is_statement(self):
        return self._name != ''

    @property
    def statement_data(self):
        return self._stmt_data

    @property
    def remaining_data(self):
        return self._remaining_data

    @property
    def is_setup_statement(self):
        pattern = r'setup *$'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_teardown_statement(self):
        pattern = r'teardown *$'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_setup_or_teardown_statement(self):
        return self.is_setup_statement or self.is_teardown_statement

    @property
    def is_parent_setup_or_teardown_statement(self):
        chk = isinstance(self.parent, (SetupStatement, TeardownStatement))
        return chk

    @property
    def is_ancestor_setup_or_teardown_for_unittest(self):
        if not self.is_unittest or not self.parent:
            return False

        node = self.parent

        while isinstance(node, Statement):
            if node.is_setup_or_teardown_statement:
                return True
            node = node.parent
        return False

    @property
    def is_ancestor_base_statement(self):
        if not self.parent:
            return False

        chk_lst = (SetupStatement, SectionStatement, TeardownStatement)

        node = self.parent

        while isinstance(node, Statement):
            if isinstance(node, chk_lst):
                return True
            node = node.parent
        return False

    @property
    def is_ancestor_section_statement(self):
        if not self.parent:
            return False

        node = self.parent

        while isinstance(node, Statement):
            if isinstance(node, SectionStatement):
                return True
            node = node.parent
        return False

    @property
    def is_ancestor_setup_statement(self):
        if not self.parent:
            return False

        if isinstance(self.parent, SetupStatement):
            return True

        node = self.parent

        while isinstance(node, Statement):
            if isinstance(node, SetupStatement):
                return True
            node = node.parent
        return False

    @property
    def is_ancestor_teardown_statement(self):
        if not self.parent:
            return False

        if isinstance(self.parent, TeardownStatement):
            return True

        node = self.parent

        while isinstance(node, Statement):
            if isinstance(node, TeardownStatement):
                return True
            node = node.parent
        return False

    @property
    def is_section_statement(self):
        pattern = r'section'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_base_statement(self):
        is_base_stmt = self.is_setup_statement
        is_base_stmt |= self.is_section_statement
        is_base_stmt |= self.is_teardown_statement
        return is_base_stmt

    def is_matched_statement(self, pat, data=None):
        data = data or [self.name, self.statement_data]
        lst = data if Misc.is_list(data) else [data]
        is_matched = any(bool(re.match(pat, str(item), re.I)) for item in lst)
        return is_matched

    def substitute_new_format(self, fmt):
        replacing = '{_replace_}'

        is_ancestor_setup_or_teardown = self.is_ancestor_setup_statement
        is_ancestor_setup_or_teardown |= self.is_ancestor_teardown_statement
        is_ancestor_base_statement = self.is_ancestor_base_statement

        if self.is_unittest or self.is_pytest:
            replaced = ''
            if is_ancestor_base_statement:
                if self.is_unittest and is_ancestor_setup_or_teardown:
                    replaced = 'cls'
                else:
                    replaced = 'self'

            lst = fmt.split(replacing)
            if len(lst) == 1:
                return fmt

            for index, item in enumerate(lst[1:], 1):
                if replaced == '' and item.startswith('.'):
                    lst[index] = item[1:]
            new_fmt = replaced.join(lst)
            return new_fmt
        else:
            if self.parent:
                return fmt
            else:
                lines = fmt.splitlines()
                last_line = lines[-1] if lines else ''
                if re.search('(?i)set +global +variable ', last_line):
                    new_fmt = '\n'.join(lines[:-1])
                    return new_fmt
                else:
                    return fmt

    def prepare(self):
        if self.is_empty:
            self._stmt_data = ''
            self._remaining_data = ''
        else:
            lst = self.data.splitlines()
            for index, line in enumerate(lst):
                line = str(line).rstrip()
                if line.strip():
                    match = re.match(self.spacer_pattern, line)
                    if match:
                        self._spacers = match.group('spacers')
                        length = len(self._spacers)
                        if length == 0:
                            self.set_level(level=0)
                        else:
                            if self.parent:
                                chk_lst = ['setup', 'teardown', 'section']
                                if self.parent.name in chk_lst:
                                    self.set_level(level=1)
                                else:
                                    self.increase_level()
                            else:
                                if self._prev_spacers > self._spacers:
                                    self.increase_level()

                    self._prev_spacers = self._spacers
                    self._stmt_data = line
                    self._remaining_data = '\n'.join(lst[index+1:])

                    if self.is_base_statement:
                        self.set_level(level=0)
                        self._spacers = ''

                    return

    def add_child(self, child):
        if isinstance(child, Statement):
            self._children.append(child)
            if isinstance(child.parent, Statement):
                child.set_level(level=self.level+1)

    def set_level(self, level=0):
        self._level = level

    def increase_level(self):
        self.set_level(level=self.level+1)

    def update_level_from_parent(self):
        if isinstance(self.parent, Statement):
            self.set_level(level=self.parent.level+1)

    def get_next_statement_data(self):
        for line in self.remaining_data.splitlines():
            if line.strip():
                return line
        else:
            return ''

    def has_next_statement(self):
        next_stmt_data = self.get_next_statement_data()
        return next_stmt_data.strip() != ''

    def check_next_statement(self, op):
        op = str(op).strip().lower()
        if op not in ['eq', 'le', 'lt', 'gt', 'ge', 'ne']:
            failure = 'Operator MUST BE eq, ne, le, lt, ge, or gt'
            raise ComparisonOperatorError(failure)

        if not self.has_next_statement():
            return False
        next_stmt_data = self.get_next_statement_data()
        match = re.match(self.spacer_pattern, next_stmt_data)
        spacers = match.group('spacers') if match else ''

        result = getattr(operator, op)(spacers, self._spacers)
        return result

    def is_next_statement_sibling(self):
        result = self.check_next_statement('eq')
        return result

    def is_next_statement_children(self):
        result = self.check_next_statement('gt')
        return result

    def is_next_statement_ancestor(self):
        result = self.check_next_statement('lt')
        return result

    def validate_framework(self):

        if self.framework.strip() == '':
            failure = 'framework MUST be "unittest", "pytest", or "robotframework"'
            raise NotImplementedFrameworkError(failure)

        is_valid_framework = self.is_unittest
        is_valid_framework |= self.is_pytest
        is_valid_framework |= self.is_robotframework

        if not is_valid_framework:
            fmt = ('{!r} framework is not implemented.  It MUST be '
                   '"unittest", "pytest", or "robotframework"')
            raise NotImplementedFrameworkError(fmt.format(self.framework))

    def indent_data(self, data, lvl):
        new_data = indent(data, ' ' * lvl * self.indentation)
        return new_data

    def get_display_statement(self, message=''):
        message = getattr(self, 'message', message)
        is_logger = getattr(self, 'is_logger', False)
        func_name = 'self.logger.info' if is_logger else 'print'
        if self.is_unittest or self.is_pytest:
            stmt = '%s(%r)' % (func_name, message)
        else:   # i.e ROBOTFRAMEWORK
            stmt = 'log   %s' % message

        level = self.parent.level + 1 if self.parent else self.level
        stmt = self.indent_data(stmt, level)
        return stmt

    def get_assert_statement(self, expected_result, assert_only=False):
        is_eresult_number, eresult = Misc.try_to_get_number(expected_result)
        if Misc.is_boolean(eresult):
            eresult = int(eresult)

        if self.is_unittest:
            if self.is_parent_setup_or_teardown_statement:
                fmt1 = 'assert True == %s'
                fmt2 = 'total_count = len(result)\nassert total_count == %s'
            else:
                fmt1 = 'self.assertTrue(True == %s)'
                fmt2 = 'total_count = len(result)\nself.assertTrue(total_count == %s)'
        elif self.is_pytest:
            fmt1 = 'assert True == %s'
            fmt2 = 'total_count = len(result)\nassert total_count == %s'
        else:   # i.e ROBOTFRAMEWORK
            fmt1 = 'should be true   True == %s'
            fmt2 = ('${total_count}=   get length ${result}\nshould be '
                    'true   ${result} == %s')

        fmt = fmt1 if assert_only else fmt2
        eresult = expected_result if assert_only else eresult
        level = self.parent.level + 1 if self.parent else self.level
        stmt = self.indent_data(fmt % eresult, level)
        return stmt

    def try_to_get_base_statement(self):
        if self.is_base_statement:
            tbl = dict(setup=SetupStatement,
                       teardown=TeardownStatement)
            key = self.statement_data.lower().strip()
            cls = tbl.get(key, SectionStatement)
            stmt = cls(self.data, framework=self.framework,
                       indentation=self.indentation)
            return stmt if isinstance(stmt, Statement) else self

        else:
            return self


class DummyStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
        self.case = ''
        self.message = ''
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        fmt = 'DUMMY {} - {}'
        expected_result = True if self.case.lower() == 'pass' else False

        message = fmt.format(self.case.upper(), self.message)
        displayed_stmt = self.get_display_statement(message=message)
        assert_stmt = self.get_assert_statement(expected_result, assert_only=True)
        return '{}\n{}'.format(displayed_stmt, assert_stmt)

    def parse(self):
        pattern = ' *dummy[_. -]*(?P<case>pass|fail) *[^a-z0-9]*(?P<message> *.+) *$'
        match = re.match(pattern, self.statement_data, re.I)
        if match:
            self._is_parsed = True
            self.case = match.group('case').lower()
            self.message = match.group('message')
            self.name = 'dummy'
        else:
            self._is_parsed = False


class SetupStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        lst = []

        if self.is_unittest:
            lst.append('@classmethod')
            lst.append('def setUpClass(cls):')
        elif self.is_pytest:
            lst.append('def setup_class(self):')
        else:   # i.e ROBOTFRAMEWORK
            lst.append('setup')

        for child in self.children:
            lst.append(child.snippet)

        level = 0 if self.is_robotframework else 1
        script = self.indent_data('\n'.join(lst), level)
        return script

    def parse(self):
        if self.is_setup_statement:
            self.name = 'setup'
            self._is_parsed = True
            if self.is_next_statement_children():
                node = self.create_child(self)
                self.add_child(node)
                while node and node.is_next_statement_sibling():
                    node = self.create_child(node)
                    self.add_child(node)
                if self.children:
                    last_child = self._children[-1]
                    self._remaining_data = last_child.remaining_data
            if not self.children:
                kwargs = dict(framework=self.framework, indentation=self.indentation)
                data = 'dummy_pass - Dummy Setup'
                dummy_stmt = DummyStatement(data, **kwargs, parent=self)
                self.add_child(dummy_stmt)
        else:
            self._is_parsed = False

    def create_child(self, node):
        kwargs = dict(framework=self.framework, indentation=self.indentation)
        next_line = node.get_next_statement_data()

        if node.is_matched_statement('(?i) +connect +data', next_line):
            other = ConnectDataStatement(node.remaining_data, **kwargs)
        elif node.is_matched_statement('(?i) +use +testcase', next_line):
            other = UseTestCaseStatement(node.remaining_data, **kwargs)
        elif node.is_matched_statement('(?i) +connect +device', next_line):
            other = ConnectDeviceStatement(node.remaining_data, **kwargs)
        else:
            return None

        other.prev = node
        # node.next = other
        if isinstance(node, self.__class__):
            other.parent = node
            other.update_level_from_parent()
        else:
            other.parent = node.parent
            other.update_level_from_parent()
        return other


class ConnectDataStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
        self.var_name = ''
        self.test_resource_ref = ''
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        kwargs = dict(v1=self.var_name, v2=self.test_resource_ref)
        if self.is_robotframework:
            fmt = ("${%(v1)s}=   connect data   filename=%(v2)s\nset global "
                   "variable   ${%(v1)s}")
            new_fmt = self.substitute_new_format(fmt)
            stmt = new_fmt % kwargs
        else:
            fmt = "{_replace_}.%(v1)s = ta.connect_data(filename=%(v2)r)"
            new_fmt = self.substitute_new_format(fmt)
            stmt = new_fmt % kwargs

        level = self.parent.level + 1 if self.parent else self.level
        stmt = self.indent_data(stmt, level)

        return stmt

    def parse(self):
        pattern = r'(?i) *connect +data +(?P<capture_data>.+)'
        match = re.match(pattern, self.statement_data)
        if match:
            capture_data = match.group('capture_data').strip()
            pattern = r'(?i)(?P<test_resource_ref>.+?)( +as +(?P<var_name>[a-z]\w*))?$'
            match = re.match(pattern, capture_data)
            
            if not match:
                fmt = 'Invalid connect data statement - "{}"'
                raise ConnectDataStatementError(fmt.format(self.statement_data))
            
            test_resource_ref = match.group('test_resource_ref').strip()
            var_name = match.group('var_name') or 'test_resource'
            self.reserve_data(test_resource_ref, var_name)
            self.name = 'connect_data'
            self._is_parsed = True
        else:
            self._is_parsed = False

    def reserve_data(self, test_resource_ref, var_name):
        try:
            SCRIPTINFO.variables.test_resource_var = var_name
            SCRIPTINFO.variables.test_resource_ref = test_resource_ref
            self.var_name = var_name
            self.test_resource_ref = test_resource_ref
            with open(test_resource_ref) as stream:
                content = stream.read().strip()
                if not content:
                    if SCRIPTINFO.is_testing_enabled:
                        SCRIPTINFO.load_testing_data()
                        return
                    fmt = '"{}" test resource reference has no data'
                    raise ConnectDataStatementError(fmt.format(test_resource_ref))
                yaml_obj = yaml.safe_load(content)
                
                if not Misc.is_dict(yaml_obj):
                    if SCRIPTINFO.is_testing_enabled:
                        SCRIPTINFO.load_testing_data()
                        return
                    fmt = '"" test resource reference has invalid format'
                    raise ConnectDataStatementError(fmt.format(test_resource_ref))
                
                SCRIPTINFO.update(yaml_obj)
        except Exception as ex:
            if SCRIPTINFO.is_testing_enabled:
                SCRIPTINFO.load_testing_data()
            else:
                raise ConnectDataStatementError(Text(ex))


class UseTestCaseStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
        self.var_name = ''
        self.test_name = ''
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        test_resource_var = SCRIPTINFO.variables.get('test_resource_var', 'test_resource')

        kwargs = dict(v1=self.var_name, v2=test_resource_var, v3=self.test_name)
        if self.is_robotframework:
            fmt = ("${%(v1)s}=  use testcase   ${%(v2)s}  testcase=%(v3)s\n"
                   "set global variable   ${%(v1)s}")
            new_fmt = self.substitute_new_format(fmt)
            stmt = new_fmt % kwargs
        else:
            fmt = ("{_replace_}.%(v1)s = ta.use_testcase({_replace_}.%(v2)s, "
                   "testcase=%(v3)r)")
            new_fmt = self.substitute_new_format(fmt)
            stmt = new_fmt % kwargs

        level = self.parent.level + 1 if self.parent else self.level
        stmt = self.indent_data(stmt, level)

        return stmt

    def parse(self):
        pattern = r'(?i) *use +testcase +(?P<capture_data>[a-z0-9].+)'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        capture_data = match.group('capture_data').strip()
        pattern = r'(?i)(?P<test_name>.+?)( +as +(?P<var_name>[a-z]\w*))? *$'
        match = re.match(pattern, capture_data)
        if not match:
            fmt = 'Invalid use testcase statement - {}'
            raise UseTestcaseStatementError(fmt.format(self.statement_data))

        test_name = match.group('test_name')
        var_name = match.group('var_name') or 'test_data'

        if test_name in SCRIPTINFO.get('testcases', dict()):
            self.reserve_data(test_name, var_name)
            self.name = 'use_testcase'
            self._is_parsed = True
        else:
            fmt = 'CANT find "{}" test name in test resource'
            raise UseTestcaseStatementError(fmt.format(test_name))

    def reserve_data(self, test_name, var_name):
        variables = SCRIPTINFO.get('variables', dict())
        SCRIPTINFO.variables = variables
        SCRIPTINFO.variables.test_data_var = self.var_name
        SCRIPTINFO.testcase = test_name
        self.var_name = var_name
        self.test_name = test_name


class ConnectDeviceStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.devices_vars = dict()
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        if not self.has_devices_variables():
            fmt = 'Failed to generate invalid connect device statement - {}'
            failure = fmt.format(self.statement_data)
            raise ConnectDeviceStatementError(failure)

        test_resource_var = SCRIPTINFO.variables.test_resource_var  # noqa

        lst = []
        for var_name, device_name in self.devices_vars.items():
            kwargs = dict(v1=var_name, v2=test_resource_var, v3=device_name)
            if self.is_robotframework:
                fmt = ("${%(v1)s}=   connect device   ${%(v2)s}   "
                       "name=%(v3)s\nset global variable   ${%(v1)s}")
                new_fmt = self.substitute_new_format(fmt)
                stmt = new_fmt % kwargs
            else:
                fmt = ("{_replace_}.%(v1)s = ta.connect_device({_replace_}."
                       "%(v2)s, name=%(v3)r)")
                new_fmt = self.substitute_new_format(fmt)
                stmt = new_fmt % kwargs
            lst.append(stmt)

        level = self.parent.level + 1 if self.parent else self.level
        connect_device_statements = self.indent_data('\n'.join(lst), level)

        return connect_device_statements

    def parse(self):
        pattern = r'(?i) *connect +device +(?P<devices_info>.+) *$'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        devices_info = match.group('devices_info').strip()
        devices_info = devices_info.replace('{', '').replace('}', '')

        pattern = r'(?i)(?P<host>\S+)( +as +(?P<var_name>[a-z]\w*))?$'
        for device_info in devices_info.split(','):
            match = re.match(pattern, device_info.strip())
            if match:
                host, var_name = match.group('host'), match.group('var_name')
                self.reserve_data(host, var_name)
            else:
                fmt = 'Invalid connect device statement - {}'
                failure = fmt.format(self.statement_data)
                raise ConnectDeviceStatementError(failure)

        self.name = 'connect_device'
        self._is_parsed = True

    def reserve_data(self, host, var_name):
        devices_vars = SCRIPTINFO.get('devices_vars', dict())
        SCRIPTINFO.devices_vars = devices_vars

        pattern = r'device[0-9]+$'

        if var_name and str(var_name).strip():
            if var_name not in devices_vars:
                devices_vars[var_name] = host
                self.devices_vars[var_name] = host
            else:
                failure = 'Duplicate device variable - "{}"'.format(var_name)
                raise ConnectDeviceStatementError(failure)
        else:
            var_names = [k for k in devices_vars if re.match(pattern, k)]
            if var_names:
                new_index = int(var_names[-1].strip('device')) + 1
                key = 'device{}'.format(new_index)
                devices_vars[key] = host
                self.devices_vars[key] = host
            else:
                devices_vars['device1'] = host
                self.devices_vars['device1'] = host

    def has_devices_variables(self):
        return bool(list(self.devices_vars))


class DisconnectStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.vars_lst = []
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        if not self.vars_lst:
            fmt = 'Failed to generate invalid disconnect device statement - {}'
            failure = fmt.format(self.statement_data)
            raise DisconnectDeviceStatementError(failure)

        lst = []
        for var_name in self.vars_lst:
            kwargs = dict(v1=var_name)
            if self.is_robotframework:
                stmt = "disconnect device   ${%(v1)s}" % kwargs
            else:
                fmt = "ta.disconnect_device({_replace_}.%(v1)s)"
                new_fmt = self.substitute_new_format(fmt)
                stmt = new_fmt % kwargs
            lst.append(stmt)

        level = self.parent.level + 1 if self.parent else self.level
        disconnect_device_statements = self.indent_data('\n'.join(lst), level)

        return disconnect_device_statements

    def parse(self):
        pattern = r'(?i) *disconnect *(device)? +(?P<devices_info>.+) *$'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        devices_info = match.group('devices_info').strip()
        devices_info = devices_info.replace('{', '').replace('}', '')

        pattern = r'(?i)(?P<host>\S+)$'
        for index, device_info in enumerate(devices_info.split(',')):
            match = re.match(pattern, device_info.strip())
            if match:
                host = match.group('host')
                self.reserve_data(host, index)
            else:
                fmt = 'Invalid disconnect device statement - {}'
                failure = fmt.format(self.statement_data)
                raise DisconnectDeviceStatementError(failure)

        self.name = 'disconnect_device'
        self._is_parsed = True

    def reserve_data(self, host, index):
        for var_name, host_name in SCRIPTINFO.devices_vars.items():
            if host == host_name:
                self.vars_lst.append(var_name)
                return

        self.vars_lst.append('device{}'.format(index + 1))


class ReleaseDeviceStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.vars_lst = []
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        if not self.vars_lst:
            fmt = 'Failed to generate invalid release device statement - {}'
            failure = fmt.format(self.statement_data)
            raise ReleaseDeviceStatementError(failure)

        lst = []
        for var_name in self.vars_lst:
            kwargs = dict(v1=var_name)
            if self.is_robotframework:
                stmt = "release device   ${%(v1)s}" % kwargs
            else:
                fmt = "ta.release_device({_replace_}.%(v1)s)"
                new_fmt = self.substitute_new_format(fmt)
                stmt = new_fmt % kwargs
            lst.append(stmt)

        level = self.parent.level + 1 if self.parent else self.level
        release_device_statements = self.indent_data('\n'.join(lst), level)

        return release_device_statements

    def parse(self):
        pattern = r'(?i) *release +device +(?P<devices_info>.+) *$'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        devices_info = match.group('devices_info').strip()
        devices_info = devices_info.replace('{', '').replace('}', '')

        pattern = r'(?i)(?P<host>\S+)$'
        for index, device_info in enumerate(devices_info.split(',')):
            match = re.match(pattern, device_info.strip())
            if match:
                host = match.group('host')
                self.reserve_data(host, index)
            else:
                fmt = 'Invalid release device statement - {}'
                failure = fmt.format(self.statement_data)
                raise ReleaseDeviceStatementError(failure)

        self.name = 'release_device'
        self._is_parsed = True

    def reserve_data(self, host, index):
        for var_name, host_name in SCRIPTINFO.devices_vars.items():
            if host == host_name:
                self.vars_lst.append(var_name)
                return

        self.vars_lst.append('device{}'.format(index + 1))


class ReleaseResourceStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.var_name = ''
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        if not self.var_name:
            fmt = 'Failed to generate invalid release resource statement - {}'
            failure = fmt.format(self.statement_data)
            raise ReleaseResourceStatementError(failure)

        kwargs = dict(v1=self.var_name)
        if self.is_robotframework:
            stmt = "release resource   ${%(v1)s}" % kwargs
        else:
            fmt = "ta.release_resource({_replace_}.%(v1)s)"
            new_fmt = self.substitute_new_format(fmt)
            stmt = new_fmt % kwargs

        level = self.parent.level + 1 if self.parent else self.level
        release_resource_statement = self.indent_data(stmt, level)

        return release_resource_statement

    def parse(self):
        pattern = r'(?i) *release +resource +(?P<resource_ref>\w(\S*\w)?) *$'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        resource_ref = match.group('resource_ref').strip()

        if SCRIPTINFO.variables.test_resource_ref != resource_ref:  # noqa
            if SCRIPTINFO.is_testing_enabled:
                self.var_name = 'test_resource'
            else:
                fmt = 'CANT find {!r} resource for release resource statement'
                failure = fmt.format(resource_ref)
                raise ReleaseResourceStatementError(failure)
        else:
            self.var_name = SCRIPTINFO.variables.test_resource_var  # noqa

        self.name = 'release_resource'
        self._is_parsed = True


class TeardownStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        lst = []

        if self.is_unittest:
            lst.append('@classmethod')
            lst.append('def tearDownClass(cls):')
        elif self.is_pytest:
            lst.append('def teardown_class(self):')
        else:   # i.e ROBOTFRAMEWORK
            lst.append('teardown')

        for child in self.children:
            lst.append(child.snippet)

        level = 0 if self.is_robotframework else 1
        script = self.indent_data('\n'.join(lst), level)
        return script

    def parse(self):
        if self.is_teardown_statement:
            self.name = self.statement_data.strip().lower()
            self._is_parsed = True
            if self.is_next_statement_children():
                node = self.create_child(self)
                self.add_child(node)
                while node and node.is_next_statement_sibling():
                    node = self.create_child(node)
                    self.add_child(node)
                if self.children:
                    last_child = self._children[-1]
                    self._remaining_data = last_child.remaining_data
            if not self.children:
                kwargs = dict(framework=self.framework, indentation=self.indentation)
                data = 'dummy_pass - Dummy %s' % self.name.title()
                dummy_stmt = DummyStatement(data, **kwargs, parent=self)
                self.add_child(dummy_stmt)
        else:
            self._is_parsed = False

    def create_child(self, node):
        kwargs = dict(framework=self.framework, indentation=self.indentation)
        next_line = node.get_next_statement_data()

        if node.is_matched_statement('(?i) +disconnect( +device)? ', next_line):
            other = DisconnectStatement(node.remaining_data, **kwargs)
        elif node.is_matched_statement('(?i) +release +device', next_line):
            other = ReleaseDeviceStatement(node.remaining_data, **kwargs)
        elif node.is_matched_statement('(?i) +release +resource', next_line):
            other = ReleaseResourceStatement(node.remaining_data, **kwargs)
        else:
            return None

        other.prev = node
        # node.next = other
        if isinstance(node, self.__class__):
            other.parent = node
            other.update_level_from_parent()
        else:
            other.parent = node.parent
            other.update_level_from_parent()
        return other


class SectionStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.description = ''
        self._method_name = ''
        self.parse()

    @property
    def method_name(self):
        return self._method_name

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        lst = []

        fmt = '%s' if self.is_robotframework else 'def %s(self):'
        lst.append(fmt % self.method_name)

        if self.description and self.description.strip():
            if self.is_robotframework:
                lst1 = wrap(self.description, width=56)
                for index, item in enumerate(lst1):
                    prefix = '[Documentation]' if index == 0 else '...'
                    lst1[index] = '{:18} {}'.format(prefix, item)

                method_doc = '\n'.join(lst1)
                lst.append(self.indent_data(method_doc, 1))
                pass
            else:
                method_doc = '"""%s"""' % self.description
                method_doc = '\n'.join(wrap(method_doc, width=70))
                lst.append(self.indent_data(method_doc, 1))

        for child in self.children:
            lst.append(child.snippet)

        level = 0 if self.is_robotframework else 1
        script = self.indent_data('\n'.join(lst), level)
        return script

    def parse(self):
        if not self.is_section_statement:
            self._is_parsed = False
            return

        pattern = r'(?i) *section([^a-z0-9]+)?(?P<description>\w+.+)?'
        match = re.match(pattern, self.statement_data)
        description = match.group('description') if match else 'test_default'
        self.parse_description(description)

        self.name = 'section'
        self._is_parsed = True
        if self.is_next_statement_children():
            node = self.create_child(self)
            self.add_child(node)
            while node and node.is_next_statement_sibling():
                node = self.create_child(node)
                self.add_child(node)
            if self.children:
                last_child = self._children[-1]
                self._remaining_data = last_child.remaining_data
        if not self.children:
            kwargs = dict(framework=self.framework, indentation=self.indentation)
            data = 'dummy_pass - Dummy for section'
            dummy_stmt = DummyStatement(data, **kwargs, parent=self)
            self.add_child(dummy_stmt)

    def parse_description(self, description):
        if not description or description == 'test_default':
            self.description = 'test default'
            self._method_name = 'test default' if self.is_robotframework else 'test_default'
        else:
            description = ' '.join(str(description).splitlines()).strip()
            pattern = r'(?i)(?P<desc>.+)( +as +(?P<ref>[a-z]\w*( +\w+)?))?$'
            match = re.match(pattern, description)
            desc, ref = match.group('desc'), match.group('ref')
            ref = ref or desc
            ref = re.sub('(?i)[^a-z0-9]+', '_', ref).strip('_')

            self.description = desc

            if not ref.startswith('test'):
                ref = 'test_%s' % ref

            if self.is_robotframework:
                self._method_name = ref.replace('_', ' ')
            else:
                if len(ref) > 70:
                    ref = '%s_%.3f' % (ref[:50], time.time())
                    ref = ref.replace('.', '_')
                self._method_name = ref

    def create_child(self, node):
        kwargs = dict(framework=self.framework, indentation=self.indentation)
        next_line = node.get_next_statement_data()

        if CheckStatement.is_verification_statement(next_line):
            other = VerificationStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_performer_statement(next_line):
            other = PerformerStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_connect_device_statement(next_line):
            other = ConnectDeviceStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_disconnect_device_statement(next_line):
            other = DisconnectStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_release_device_statement(next_line):
            other = ReleaseDeviceStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_pausing_statement(next_line):
            other = WaitForStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_iterative_statement(next_line):
            other = LoopStatement(node.remaining_data, **kwargs)
        else:
            return None

        other.prev = node
        # node.next = other
        if isinstance(node, self.__class__):
            other.parent = node
            other.update_level_from_parent()
        else:
            other.parent = node.parent
            other.update_level_from_parent()
        return other


class LoopStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.ntimes = 0
        self.parse()

    @property
    def is_regular_iterative(self):
        result = CheckStatement.is_regular_iterative_statement(self.statement_data)
        return result

    @property
    def is_util_iterative(self):
        result = CheckStatement.is_until_iterative_statement(self.statement_data)
        return result

    @property
    def is_to_last_iterative(self):
        result = CheckStatement.is_to_last_iterative_statement(self.statement_data)
        return result

    @property
    def is_iterative_statement(self):
        result = self.is_regular_iterative
        result |= self.is_util_iterative
        result |= self.is_to_last_iterative
        return result

    @property
    def snippet(self):
        if self.is_regular_iterative:
            stmt = self.regular_iterative_snippet
            return stmt
        elif self.is_util_iterative:
            stmt = self.until_iterative_snippet
            return stmt
        else:
            stmt = self.to_last_iterative_snippet
            return stmt

    @property
    def regular_iterative_snippet(self):
        if not self.is_parsed:
            return ''
        if self.ntimes <= 0:
            return ''

        lst = []
        if self.is_robotframework:
            lst.append('${ntimes}=   set variable   %s' % self.ntimes)
            lst.append('@{indexes}=   evaluate   range(1, ${ntimes} + 1)')
            lst.append('FOR   ${index}   IN   @{indexes}')
            for child in self.children:
                if child.name == 'verification':
                    msg = 'Failed at iteration ${index}/${ntimes}'
                    child_snippet = child.render_assertion_message(msg)
                    lst.append(child_snippet)
                else:
                    lst.append(child.snippet)
            lst.append('END')
        else:
            lst.append('ntimes = %s' % self.ntimes)
            lst.append('indexes = range(1, times + 1)')
            lst.append('for index in indexes:')
            for child in self.children:
                if child.name == 'verification':
                    msg = "'Failed at iteration {}/{}'.format(index, ntimes)"
                    child_snippet = child.render_assertion_message(msg)
                    lst.append(child_snippet)
                else:
                    lst.append(child.snippet)

        stmt = self.indent_data('\n'.join(lst), self.level)
        return stmt

    @property
    def until_iterative_snippet(self):
        if not self.is_parsed:
            return ''
        if self.ntimes <= 0:
            return ''

        lst = []
        if self.is_robotframework:
            lst.append('${ntimes}=   set variable   %s' % self.ntimes)
            lst.append('@{indexes}=   evaluate   range(1, ${ntimes} + 1)')
            lst.append('${is_passed}=   set variable   ${True}')
            lst.append('FOR   ${index}   IN   @{indexes}')
            for child in self.children:
                if child.name == 'verification':
                    msg = 'Failed at iteration ${index}/${ntimes}'
                    child_snippet = child.render_assertion_message(msg)
                    lst.append(child_snippet)
                else:
                    lst.append(child.snippet)

            lst.append(self.indent_data('exit for loop if   ${is_passed}', 1))
            lst.append('END')
        else:
            lst.append('ntimes = %s' % self.ntimes)
            lst.append('indexes = range(1, times + 1)')
            lst.append('is_passed = True')
            lst.append('for index in indexes:')
            for child in self.children:
                if child.name == 'verification':
                    msg = "'Failed at iteration {}/{}'.format(index, ntimes)"
                    child_snippet = child.render_assertion_message(msg)
                    lst.append(child_snippet)
                else:
                    lst.append(child.snippet)

            lst.append(self.indent_data('if is_passed:', 1))
            lst.append(self.indent_data('break', 2))

        stmt = self.indent_data('\n'.join(lst), self.level)
        return stmt

    @property
    def to_last_iterative_snippet(self):
        if not self.is_parsed:
            return ''
        if self.ntimes <= 0:
            return ''

        lst = []
        if self.is_robotframework:
            lst.append('${ntimes}=   set variable   %s' % self.ntimes)
            lst.append('@{indexes}=   evaluate   range(1, ${ntimes} + 1)')
            lst.append('${is_passed}=   set variable   ${True}')
            lst.append('FOR   ${index}   IN   @{indexes}')
            for child in self.children:
                if child.name == 'verification':
                    addition = '${is_passed}=   evaluate   ${is_passed} and ${check}'
                    child_snippet = child.convert_assertion_to_check(addition=addition)
                    lst.append(child_snippet)
                else:
                    lst.append(child.snippet)
            lst.append(('run keyword if   ${is_passed} == False   Log   '
                        'failed verification(s) at iteration '
                        '${index}/${ntimes}   WARN'))
            lst.append('END')
            lst.append('should be true   ${is_passed}')
        else:
            lst.append('ntimes = %s' % self.ntimes)
            lst.append('indexes = range(1, times + 1)')
            lst.append('is_passed = True')
            lst.append('for index in indexes:')
            for child in self.children:
                if child.name == 'verification':
                    addition = 'is_passed = is_passed and check'
                    child_snippet = child.convert_assertion_to_check(addition=addition)
                    lst.append(child_snippet)
                else:
                    lst.append(child.snippet)

            lst.append(self.indent_data('if not is_passed:', 1))
            warned_msg = "'Warning: failed verification(s) at iteration {}/{}'.format(index, ntimes)"
            lst.append(self.indent_data('print(%s)' % warned_msg, 2))

            if self.is_unittest:
                lst.append('self.assertTrue(is_passed)')
            else:
                lst.append('assert is_passed')

        stmt = self.indent_data('\n'.join(lst), self.level)
        return stmt

    def parse(self):
        if not self.is_iterative_statement:
            self._is_parsed = False
            return

        pattern = r'(?i) *loop +(?P<ntimes>[0-9]+) +'
        match = re.match(pattern, self.statement_data)
        self.ntimes = int(match.group('ntimes'))

        if self.is_next_statement_children():
            node = self.create_child(self)
            self.add_child(node)
            while node and node.is_next_statement_sibling():
                node = self.create_child(node)
                self.add_child(node)
            if self.children:
                last_child = self._children[-1]
                self._remaining_data = last_child.remaining_data
        if not self.children:
            kwargs = dict(framework=self.framework, indentation=self.indentation)
            data = 'dummy_pass - Dummy iterative statement'
            dummy_stmt = DummyStatement(data, **kwargs, parent=self)
            self.add_child(dummy_stmt)

        self.name = 'loop'
        self._is_parsed = True
        self.update_level_from_parent()

    def create_child(self, node):
        kwargs = dict(framework=self.framework, indentation=self.indentation)
        next_line = node.get_next_statement_data()

        if CheckStatement.is_verification_statement(next_line):
            other = VerificationStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_performer_statement(next_line):
            other = PerformerStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_connect_device_statement(next_line):
            other = ConnectDeviceStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_disconnect_device_statement(next_line):
            other = DisconnectStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_release_device_statement(next_line):
            other = ReleaseDeviceStatement(node.remaining_data, **kwargs)
        elif CheckStatement.is_pausing_statement(next_line):
            other = WaitForStatement(node.remaining_data, **kwargs)
        else:
            return None

        other.prev = node
        # node.next = other
        if isinstance(node, self.__class__):
            other.parent = node
            other.update_level_from_parent()
        else:
            other.parent = node.parent
            other.update_level_from_parent()
        return other


class PerformerStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.result = None
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        lst = []

        result = self.result

        if self.is_robotframework:
            for device_name in result.devices_names:
                var_name = SCRIPTINFO.get_device_var(device_name)
                if result.has_select_statement:
                    fmt = '{output}=   execute   ${%s}   cmdline=%s'
                    lst.append(fmt % (var_name, result.operation_ref))
                    if result.is_template:
                        fmt = ('filter   ${output}   convertor=%s   template_ref=%s\n'
                               '...   select_statement=%s')
                        stmt = fmt % (result.convertor, result.convertor_arg,
                                      result.select_statement)
                        lst.append(stmt)
                    else:
                        fmt = ('filter   ${output}   convertor=%s\n'
                               '...   select_statement=%s')
                        stmt = fmt % (result.convertor, result.select_statement)
                        lst.append(stmt)
                else:
                    fmt = 'execute   ${%s}   cmdline=%s'
                    lst.append(fmt % (var_name, self.result.operation_ref))
        else:
            for device_name in self.result.devices_names:
                var_name = SCRIPTINFO.get_device_var(device_name)

                if result.has_select_statement:
                    fmt = 'output = ta.execute({_replace_}.%s, cmdline=%r)'
                    new_fmt = self.substitute_new_format(fmt)
                    lst.append(new_fmt % (var_name, result.operation_ref))
                    if result.is_template:
                        fmt = ('ta.filter(output, convertor=%r, template_ref=%r,\n'
                               '          select_statement=%r)')
                        stmt = fmt % (result.convertor, result.convertor_arg,
                                      result.select_statement)
                        lst.append(stmt)
                    else:
                        fmt = ('ta.filter(output, convertor=%r,\n'
                               '          select_statement=%r)')
                        stmt = fmt % (result.convertor, result.select_statement)
                        lst.append(stmt)
                else:
                    fmt = 'ta.execute({_replace_}.%s, cmdline=%r)'
                    new_fmt = self.substitute_new_format(fmt)
                    lst.append(new_fmt % (var_name, result.operation_ref))

        stmt = self.indent_data('\n'.join(lst), self.level)
        return stmt

    def parse(self):
        if not CheckStatement.is_performer_statement(self.statement_data):
            self._is_parsed = False
            return

        result = ParsedOperation(self.statement_data)
        self.result = result
        self._is_parsed = result.is_parsed
        self.name = self.result.name
        self.update_level_from_parent()

        if result.error:
            raise PerformerStatementError(result.error)


class VerificationStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)

        self.result = None
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        lst = []

        result = self.result

        if self.is_robotframework:
            for device_name in result.devices_names:
                var_name = SCRIPTINFO.get_device_var(device_name)

                fmt = '{output}=   execute   ${%s}   cmdline=%s'
                lst.append(fmt % (var_name, result.operation_ref))
                if result.is_template:
                    fmt = ('${result}=   filter   ${output}   convertor=%s   template_ref=%s\n'
                           '...   select_statement=%s')
                    stmt = fmt % (result.convertor, result.convertor_arg,
                                  result.select_statement)
                    lst.append(stmt)
                else:
                    fmt = ('${result}=   filter   ${output}   convertor=%s\n'
                           '...   select_statement=%s')
                    stmt = fmt % (result.convertor, result.select_statement)
                    lst.append(stmt)

                lst.append('${total_count}=  get length   ${result}')
                lst.append('should be true   ${total_count} == %s' % result.expected_condition)

        else:
            for device_name in self.result.devices_names:
                var_name = SCRIPTINFO.get_device_var(device_name)

                fmt = 'output = ta.execute({_replace_}.%s, cmdline=%r)'
                new_fmt = self.substitute_new_format(fmt)
                lst.append(new_fmt % (var_name, result.operation_ref))
                if result.is_template:
                    fmt = ('result = ta.filter(output, convertor=%r, template_ref=%r,\n'
                           '                   select_statement=%r)')
                    stmt = fmt % (result.convertor, result.convertor_arg,
                                  result.select_statement)
                    lst.append(stmt)
                else:
                    fmt = ('result = ta.filter(output, convertor=%r,\n'
                           '                   select_statement=%r)')
                    stmt = fmt % (result.convertor, result.select_statement)
                    lst.append(stmt)

                lst.append('total_count = len(result)')
                if self.is_unittest:
                    fmt = 'self.assertTrue(total_count == %s)'
                    lst.append(fmt % result.expected_condition)
                else:
                    lst.append('assert total_count == %s' % result.expected_condition)

        stmt = self.indent_data('\n'.join(lst), self.level)
        return stmt

    def render_assertion_message(self, msg):
        if not self.snippet:
            return ''

        lines = dedent(self.snippet).splitlines()
        tbl = dict(unittest='%s, msg=%s)', pytest='%s, %s', robotframework='%s   %s')
        fmt = tbl[self.framework.lower()]
        pattern = '(?i)(should be true)|(self[.])?assert(True)?'

        lst = []
        for line in lines:
            if re.match(pattern, line):
                txt = line[:-1] if self.is_unittest else line
                new_line = fmt % (txt, msg)
                lst.append(new_line)
            else:
                lst.append(line)

        new_snippet = self.indent_data('\n'.join(lst), self.level)
        return new_snippet

    def convert_assertion_to_check(self, addition=''):
        if not self.snippet:
            return ''

        lines = dedent(self.snippet).splitlines()
        pattern = ('(?i)(?P<case>(should be true)|(self[.])?assert(True)?) *'
                   '(?P<val>[^ ].*[^ ]?) *$')

        lst = []
        for index, line in enumerate(lines):
            match = re.match(pattern, line)
            if match:
                val = match.group('val').strip()
                if self.is_robotframework:
                    lst.append('${check}=   evaluate   %s' % val)
                else:
                    val = val.lstrip('(').rstrip(')')
                    lst.append('check = %s' % val)
                addition and lst.append(addition)
            else:
                lst.append(line)

        new_snippet = self.indent_data('\n'.join(lst), self.level)
        return new_snippet

    def parse(self):
        if not CheckStatement.is_execute_cmdline(self.statement_data):
            self._is_parsed = False
            return

        result = ParsedOperation(self.statement_data)
        self.result = result
        self._is_parsed = result.is_parsed
        self.name = 'verification'
        self.update_level_from_parent()

        if result.error:
            raise PerformerStatementError(result.error)

        if not self.result.is_verification:
            fmt = 'Invalid verification statement format\n %s'
            raise VerificationStatementError(fmt % self.statement_data)


class WaitForStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
        self.total_seconds = 0
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        fmt = 'wait for   %s' if self.is_robotframework else 'ta.wait_for(%s)'
        stmt = self.indent_data(fmt % self.total_seconds, self.level)
        return stmt

    def parse(self):
        pattern = r'(?i) *((wait +for)|sleep) +(?P<capture_data>[0-9].+) *$'
        match = re.match(pattern, self.statement_data)
        if not match:
            self._is_parsed = False
            return

        capture_data = match.group('capture_data').strip()

        pattern = ('(?P<val>([0-9]*[.])?[0-9]+) *'
                   '(?P<unit>h((ou)?rs?)?|m(in(utes?)?)?|'
                   's(ec(onds?)?)?|d(ays?)?)?')
        match = re.match(pattern, capture_data, re. I)
        if not match:
            failure = 'Invalid wait for statement format'
            raise WaitForStatementError(failure)

        result = DotObject(match.groupdict())
        tbl = dict(s=1, m=60, h=60 * 60, d=60 * 60 * 24)
        multiplier = tbl.get(str(result.unit).lower()[:1], 1)
        seconds = float(result.val) * multiplier
        self.total_seconds = int(seconds) if int(seconds) == seconds else seconds
        self._is_parsed = True
        self.name = 'wait_for'
        self.update_level_from_parent()


class ScriptBuilder:
    def __init__(self, data, framework='', indentation=4,
                 username='', email='', company='',):
        self.data = data
        self.framework = str(framework).strip()
        self.indentation = indentation
        self.username = str(username).strip()
        self.email = str(email).strip()
        self.company = str(company).strip() or self.username

        self.setup_statement = None
        self.teardown_statement = None
        self.section_statements = []
        self.build()

    @property
    def testscript(self):
        if self.setup_statement and self.teardown_statement:
            if self.framework == FWTYPE.UNITTEST:
                script = self.unittest_script
                return script
            elif self.framework == FWTYPE.PYTEST:
                script = self.pytest_script
                return script
            else:
                script = self.robotframework_script
                return script
        else:
            pass

    @property
    def unittest_script(self):
        cls_name = SCRIPTINFO.get_class_name()
        lst = [
            self.script_intro,
            '',
            'import unittest',
            'import dgspoc as ta',
            '\n',
            'class {}(unittest.Testcase):'.format(cls_name),
            self.setup_statement.snippet,
            '',
            self.teardown_statement.snippet,
        ]

        for index, stmt in enumerate(self.section_statements, 1):
            lst.append('')
            replaced = 'def test_%03i_' % index
            if stmt.snippet:
                lst.append(stmt.snippet.replace('def test_', replaced))

        lst.append('')
        lst.append("if __name__ == '__main__':")
        lst.append(indent('unittest.main()', ' ' * self.indentation))

        script = '\n'.join(lst)

        return script

    @property
    def pytest_script(self):
        cls_name = SCRIPTINFO.get_class_name()
        lst = [
            self.script_intro,
            '',
            '# import pytest',
            'import dgspoc as ta',
            '\n',
            'class {}:'.format(cls_name),
            self.setup_statement.snippet,
            '',
            self.teardown_statement.snippet,
        ]

        method_names = []

        for stmt in self.section_statements:
            lst.append('')
            snippet = stmt.snippet
            method_name = stmt.method_name
            if snippet:
                if method_name not in method_names:
                    method_names.append(method_name)
                else:
                    replacing = 'def %s(:' % method_name
                    replaced = 'def %s_%.3f(:' % (method_name, time.time())
                    replaced = replaced.replace('.', '_')
                    snippet = snippet.replace(replacing, replaced)
                lst.append(snippet)

        script = '\n'.join(lst)
        return script

    @property
    def robotframework_script(self):
        lst = [
            self.script_intro,
            '',
            '*** Settings ***',
            'library         builtin',
            'library         collections',
            'library         describegetsystempoc',
            'test setup      setup',
            'test teardown   {}'.format(self.teardown_statement.name),
        ]

        method_names = []

        if self.section_statements:
            lst.append('\n*** Test Cases ***')
            for stmt in self.section_statements:
                snippet = stmt.snippet
                method_name = stmt.method_name
                if snippet:
                    if method_name not in method_names:
                        method_names.append(method_name)
                    else:
                        postfix = (' %.3f' % time.time()).replace('.', '_')
                        lines = snippet.splitlines()
                        lines[0] = lines[0] + postfix
                        snippet = '\n'.join(lines)
                    lst.append(snippet)
                    lst.append('')

        not self.section_statements and lst.append('')

        lst.append('*** Keywords ***')
        lst.append(self.setup_statement.snippet)
        lst.append('')
        lst.append(self.teardown_statement.snippet)

        script = '\n'.join(lst)
        return script

    @property
    def script_intro(self):
        fmt = '# {} script is generated by Describe-Get-System Proof of Concept'
        user_fmt = '# Created by  : {0.username}'
        email_fmt = '# Email       : {0.email}'
        company_fmt = '# Company     : {0.company}'
        date_fmt = '# Created date: {}'
        lst = [fmt.format(self.framework.lower())]
        self.username and lst.append(user_fmt.format(self))
        self.email and lst.append(email_fmt.format(self))
        self.company and lst.append(company_fmt.format(self))
        not SCRIPTINFO.is_testing_enabled and lst.append(date_fmt)

        intro = '\n'.join(['#' * 80] + lst + ['#' * 80])
        return intro

    def build(self):
        data = self.data
        count = 2000

        while data.strip() and count > 0:
            stmt = Statement(data, framework=self.framework,
                             indentation=self.indentation)
            stmt = stmt.try_to_get_base_statement()
            self.add_statement(stmt)
            data = stmt.remaining_data
            count -= 1

    def add_statement(self, stmt):
        if stmt.is_setup_statement:
            if not self.setup_statement:
                self.setup_statement = stmt
            else:
                self.warn_duplicate_statement(stmt)
        elif stmt.is_teardown_statement:
            if not self.teardown_statement:
                self.teardown_statement = stmt
            else:
                self.warn_duplicate_statement(stmt)
        elif stmt.is_section_statement:
            if self.is_uniq_section_statement(stmt):
                self.section_statements.append(stmt)
            else:
                self.warn_duplicate_statement(stmt)
        else:
            self.warn_not_implement_statement(stmt)

    def is_uniq_section_statement(self, stmt):
        if not self.section_statements:
            return True

        chk = stmt.snippet
        is_duplicate = any(chk == k.snippet for k in self.section_statements)
        return not is_duplicate

    def warn_duplicate_statement(self, stmt):
        fmt = 'IncompleteTask - Need to implement warn_duplicate_statement\n{}'
        raise NotImplementedError(fmt.format(stmt.statement_data))

    def warn_not_implement_statement(self, stmt):
        fmt = 'IncompleteTask - Need to implement warn_not_implement_statement\n{}'
        raise NotImplementedError(fmt.format(stmt.statement_data))
