from enum import Enum


class ResponseError(Enum):
    repository_already_exists = 'Repository already exists: %s'
