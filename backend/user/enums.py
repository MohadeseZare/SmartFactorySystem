from enum import Enum


class Genders(Enum):
    MALE = 1
    FEMALE = 2


"""
    use operation enum for create permissions_role that use the site different access to different people
"""


class Operations(Enum):
    VIEW = 1
    CREATE = 2
    UPDATE = 3
    DELETE = 4
    VIEW_TRASHED = 5
    DELETE_TRASHED = 6
