from enum import Enum


class ResponseError(Enum):
    repository_already_exists = 'Repository already exists: %s'
    repository_not_found = 'Repository not found: %s'
