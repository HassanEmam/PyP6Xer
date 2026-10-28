# PyP6XER
# Copyright (C) 2020, 2021 Hassan Emam <hassan@constology.com>
#
# This file is part of PyP6XER.
#
# PyP6XER library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v2.1 as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyP6XER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>.


'''
This file starts the process of reading and parsing xer files

'''
import csv
import io
import mmap
import codecs
import sys
from xerparser import *
from typing import List
from xerparser.model.classes.data import Data
from xerparser.write import writeXER

class Reader:

    """
    Reader class is the main parser for xer files. It takes a file path as a parameter.
    The read records are parsed into classes depending on their types like activities, wbs,etc.

    :param <file>: is an xer file that need to be parsed
    :return: Reader object that contains collection of parsed records
    :Example:

    from xerparser.reader import Reader
    file = Reader('file.xer')

    """

    current_table = ''
    current_headers = []
    xer_header = None

    def write(self, filename=None):
        if filename is None:
            raise Exception("You have to provide the filename")
        writeXER(self, filename)

    _DISPATCH = {
        "CURRTYPE": "_currencies", "ROLES": "_roles", "ACCOUNT": "_accounts",
        "ROLERATE": "_rolerates", "OBS": "_obss", "RCATTYPE": "_rcattypes",
        "UDFTYPE": "_udftypes", "RCATVAL": "_rcatvals", "PROJECT": "_projects",
        "CALENDAR": "_calendars", "SCHEDOPTIONS": "_schedoptions",
        "PROJWBS": "_wbss", "RSRC": "_resources", "RSRCCURVDATA": "_rsrcurves",
        "ACTVTYPE": "_acttypes", "PCATTYPE": "_pcattypes", "PROJPCAT": "_projpcats",
        "PCATVAL": "_pcatvals", "RSRCRATE": "_rsrcrates", "RSRCRCAT": "_rsrccats",
        "TASK": "_tasks", "ACTVCODE": "_actvcodes", "TASKPRED": "_predecessors",
        "TASKRSRC": "_activityresources", "TASKPROC": "_taskprocs",
        "TASKACTV": "_activitycodes", "UDFVALUE": "_udfvalues",
        "FINTMPL": "_fintmpls", "NONWORK": "_nonworks",
    }
    # Collections that receive the shared Data instance as a second argument.
    _NEEDS_DATA = {"PROJECT", "PROJWBS", "TASK", "TASKRSRC", "TASKACTV"}

    # Table -> collection attribute. O(1) dict dispatch instead of a ~30-way
    # elif chain, which dominated the parse profile on large files.
    _DISPATCH = {
        "CURRTYPE": "_currencies",
        "ROLE": "_roles",
        "ROLES": "_roles",
        "ACCOUNT": "_accounts",
        "ROLERATE": "_rolerates",
        "OBS": "_obss",
        "RCATTYPE": "_rcattypes",
        "UDFTYPE": "_udftypes",
        "RCATVAL": "_rcatvals",
        "PROJECT": "_projects",
        "CALENDAR": "_calendars",
        "SCHEDOPTIONS": "_schedoptions",
        "PROJWBS": "_wbss",
        "RSRC": "_resources",
        "RSRCCURVDATA": "_rsrcurves",
        "ACTVTYPE": "_acttypes",
        "PCATTYPE": "_pcattypes",
        "PROJPCAT": "_projpcats",
        "PCATVAL": "_pcatvals",
        "RSRCRATE": "_rsrcrates",
        "RSRCRCAT": "_rsrccats",
        "TASK": "_tasks",
        "ACTVCODE": "_actvcodes",
        "TASKPRED": "_predecessors",
        "TASKRSRC": "_activityresources",
        "TASKPROC": "_taskprocs",
        "TASKACTV": "_activitycodes",
        "UDFVALUE": "_udfvalues",
        "FINTMPL": "_fintmpls",
        "NONWORK": "_nonworks",
    }

    def create_object(self, object_type, params):
        """Add a parsed record to the matching collection (O(1) dispatch)."""
        attr = self._DISPATCH.get(object_type)
        if attr is None:
            return
        collection = getattr(self, attr)
        if object_type in self._NEEDS_DATA:
            collection.add(params, self._data)
        else:
            collection.add(params)

    @property
    def projects(self) -> Projects:
        """
        Projects

        :return: list of all projects contained in the xer file

        todo:: text

        """
        return self._projects

    @property
    def activities(self) -> Tasks:
        """
        Property to retrieve list of tasks
        Returns: list of tasks
        """
        return self._tasks

    @property
    def wbss(self) -> WBSs:
        """
        Property to return all wbs elements in the parsed file
        Returns:
            list of wbs elements
        """
        return self._wbss

    @property
    def relations(self) -> Predecessors:
        """
        Property to retrieve relationships from parsed file
        Returns:
            list of relations
        """
        return self._predecessors

    @property
    def resources(self) -> Resources:
        """
        Property to return a list of resources from parsed file
        Returns:
            list of resources of type Resources
        """
        return self._resources

    @property
    def accounts(self) -> Accounts:
        """
        Property to return a list of accounts from parsed files
        Returns:
            list of accounts of type Accounts
        """
        return self._accounts

    @property
    def activitycodes(self) -> ActivityCodes:
        """
        Property to return a list of activity codes from parsed files
        Returns:
            list of activity codes of type ActivityCode

        """
        return self._actvcodes

    @property
    def actvcodes(self) -> ActivityCodes:
        """Backward-compatible alias for activitycodes."""
        return self._actvcodes

    @property
    def taskactvs(self) -> TaskActvs:
        """Return the task-to-activity-code assignments from TASKACTV."""
        return self._activitycodes

    @property
    def acttypes(self) -> ActTypes:
        return self._acttypes

    @property
    def calendars(self) -> Calendars:
        return self._calendars

    @property
    def currencies(self) -> Currencies:
        return self._currencies

    @property
    def obss(self) -> OBSs:
        return self._obss

    @property
    def rcattypes(self) -> RCatTypes:
        return self._rcattypes

    @property
    def rcatvals(self) -> RCatVals:
        return self._rcatvals

    @property
    def rolerates(self) -> RoleRates:
        return self._rolerates

    @property
    def roles(self) -> Roles:
        return self._roles

    @property
    def resourcecurves(self) -> ResourceCurves:
        return self._rsrcurves

    @property
    def resourcerates(self) -> ResourceRates:
        return self._rsrcrates

    @property
    def resourcecategories(self) -> ResourceCategories:
        return self._rsrccats

    @property
    def scheduleoptions(self) -> SchedOptions:
        return self._schedoptions

    @property
    def activityresources(self) -> ActivityResources:
        return self._activityresources

    @property
    def udfvalues(self) -> UDFValues:
        return self._udfvalues

    @property
    def udftypes(self) -> UDFTypes:
        return self._udftypes

    @property
    def pcattypes(self) -> List[PCatTypes]:
        return self._pcattypes

    @property
    def pcatvals(self) -> List[PCatVals]:
        return self._pcatvals

    @property
    def projpcats(self) -> List[ProjCat]:
        return self._projpcats

    @property
    def taskprocs(self) -> List[TaskProc]:
        return self._taskprocs

    @property
    def fintmpls(self) -> List[FinTmpl]:
        return self._fintmpls

    @property
    def nonworks(self) -> List[NonWork]:
        return self._nonworks

    def summary(self):
        print('Number of activities: ', self.activities.count)
        print('Number of relationships: ', len(self.relations))

    def __init__(self, filename):
        self.file = filename
        self._tasks = Tasks()
        self._predecessors = Predecessors()
        self._projects = Projects()
        self._wbss = WBSs()
        self._resources = Resources()
        self._accounts = Accounts()
        self._actvcodes = ActivityCodes()
        self._activitycodes = TaskActvs()
        self._acttypes = ActTypes()
        self._calendars = Calendars()
        self._currencies = Currencies()
        self._obss = OBSs()
        self._rcatvals = RCatVals()
        self._rcattypes = RCatTypes()
        self._rolerates = RoleRates()
        self._roles = Roles()
        self._rsrcurves = ResourceCurves()
        self._rsrcrates = ResourceRates()
        self._rsrccats = ResourceCategories()
        self._schedoptions = SchedOptions()
        self._activityresources = ActivityResources()
        self._udftypes = UDFTypes()
        self._udfvalues = UDFValues()
        self._pcattypes = PCatTypes()
        self._pcatvals = PCatVals()
        self._projpcats = ProjCats()
        self._taskprocs = TaskProcs()
        self._fintmpls = FinTmpls()
        self._nonworks = NonWorks()
        self._data = Data()
        self._data.projects = self._projects
        self._data.wbss = self._wbss
        self._data.tasks = self._tasks
        self._data.resources = self._resources
        self._data.taskresource = self._activityresources
        self._data.taskactvcodes = self._activitycodes
        self._data.predecessors = self._predecessors
        self._data.calendars = self._calendars
        self._tasks.data = self._data
        self.xer_header = None
        # Reset class-level registries so parsing a new file cannot
        # resolve lookups against records from a previously parsed file.
        self._reset_class_registries()
        content, header = self._decode_file(filename)
        self.xer_header = header
        # XER fields (e.g. clndr_data) can exceed the default 128 KiB csv field limit.
        limit = sys.maxsize
        while limit > 0:
            try:
                csv.field_size_limit(limit)
                break
            except OverflowError:
                limit //= 10
        stream = csv.reader(io.StringIO(content, newline=''), delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in stream:
            if not row or not row[0]:
                continue
            tag = row[0].strip()
            if tag == "%T":
                current_table = row[1].strip()
            elif tag == "%F":
                current_headers = [r.strip() for r in row[1:]]
            elif tag == "%R":
                zipped_record = dict(zip(current_headers, row[1:]))
                self.create_object(current_table, zipped_record)

    @staticmethod
    def _reset_class_registries():
        """Clear class-level obj_list registries before a fresh parse.

        The model classes keep registries at class level for backwards
        compatibility, but they must not leak records between files.
        """
        from xerparser.model.classes.task import Task
        from xerparser.model.classes.taskpred import TaskPred
        from xerparser.model.classes.calendar import Calendar
        from xerparser.model.classes.calendar_data import CalendarData
        from xerparser.model.classes.wbs import WBS
        from xerparser.model.classes.rsrc import Resource
        from xerparser.model.classes.role import Role
        from xerparser.model.classes.rolerate import RoleRate
        from xerparser.model.classes.account import Account
        from xerparser.model.classes.obs import OBS
        from xerparser.model.classes.currency import Currency
        from xerparser.model.classes.activitycode import ActivityCode
        from xerparser.model.classes.taskactv import TaskActv
        from xerparser.model.classes.rsrcrate import ResourceRate
        from xerparser.model.classes.rsrccurv import ResourceCurve
        from xerparser.model.classes.rcattype import RCatType
        from xerparser.model.classes.rcatval import RCatVal
        from xerparser.model.classes.rsrcrcat import ResourceCat
        from xerparser.model.classes.schedoption import SchedOption
        from xerparser.model.classes.pcattype import PCatType
        from xerparser.model.classes.pcatval import PCatVal
        from xerparser.model.classes.acttype import ActType
        from xerparser.model.classes.taskproc import TaskProc
        from xerparser.model.classes.fintmpl import FinTmpl
        from xerparser.model.classes.nonwork import NonWork
        from xerparser.model.classes.udftype import UDFType
        from xerparser.model.classes.udfvalue import UDFValue
        from xerparser.model.classes.projcat import ProjCat
        for cls in (Task, TaskPred, Calendar, CalendarData, WBS, Resource, Role,
                    RoleRate, Account, OBS, Currency, ActivityCode, TaskActv,
                    ResourceRate, ResourceCurve, RCatType, RCatVal, ResourceCat,
                    SchedOption, PCatType, PCatVal, ActType, TaskProc, FinTmpl,
                    NonWork, UDFType, UDFValue, ProjCat):
            if hasattr(cls, 'obj_list'):
                cls.obj_list = []

    @staticmethod
    def _decode_file(filename):
        """Read an XER file handling both UTF-8 and CP1252 (ANSI) encodings.

        P6 exports XER files in the system ANSI codepage (typically CP1252).
        Decoding those as UTF-8 with errors='ignore' silently deletes every
        non-ASCII character, so we try UTF-8 strictly first and fall back.
        """
        with open(filename, 'rb') as fh:
            raw = fh.read()
        for encoding in ('utf-8-sig', 'cp1252'):
            try:
                text = raw.decode(encoding)
                break
            except (UnicodeDecodeError, LookupError):
                continue
        else:
            text = raw.decode('utf-8', errors='replace')
        lines = text.splitlines()
        header = None
        if lines and lines[0].startswith('ERMHDR'):
            header = lines[0].split('\t')
            lines = lines[1:]
        Reader.xer_header = header
        return '\n'.join(lines), header


    def get_num_lines(self, file_path):
        fp = open(file_path, "r+")
        buf = mmap.mmap(fp.fileno(), 0)
        lines = 0
        while buf.readline():
            lines += 1
        return lines
