from enum import Enum


class Resource(Enum):
    """This enum is a wrapper around the official resource types supported by on office"""

    ESTATE = "estate"
    ADDRESS = "address"
    SEARCH_CRITERIA = "searchcriteria"
    AGENTSLOG = "agentslog"
    RELATION = "relation"
    CALENDAR = "calendar"
    TASK = "task"
    WORKING_LIST = "workinglist"
    IMPRESSUM = "impressum"
    USER = "user"
    USERPHOTO = "userphoto"
    BASIC_SETTINGS = "basicsettings"
