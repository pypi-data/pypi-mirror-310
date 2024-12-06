from enum import Enum


class Action(Enum):
    """This enum is a wrapper around the official actions defined by on office"""

    READ = "urn:onoffice-de-ns:smart:2.5:smartml:action:read"
    CREATE = "urn:onoffice-de-ns:smart:2.5:smartml:action:create"
    EDIT = "urn:onoffice-de-ns:smart:2.5:smartml:action:modify"
    DELETE = "urn:onoffice-de-ns:smart:2.5:smartml:action:delete"
    INFORMATION = "urn:onoffice-de-ns:smart:2.5:smartml:action:get"
    DO = "urn:onoffice-de-ns:smart:2.5:smartml:action:do"
