import traceback

import falcon
from sqlalchemy.orm.exc import NoResultFound

from log.quant_logging import logger

RESOURCE_NOT_FOUND_EXCEPTION = {
    'status': falcon.HTTP_404,
    'code': 404,
    'title': 'Resource not found'
}

ERR_UNKNOWN = {
    'status': falcon.HTTP_500,
    'code': 500,
    'title': 'Unknown Error'
}

INVALID_REQUEST_EXCEPTION = {
    'status': falcon.HTTP_400,
    'code': 400,
    'title': 'Invalid Request'
}

class AppError(Exception):
    def __init__(self, error=ERR_UNKNOWN, description=None):
        self.error = error
        self.error['description'] = description

    @property
    def code(self):
        return self.error['code']

    @property
    def title(self):
        return self.error['title']

    @property
    def status(self):
        return self.error['status']

    @property
    def description(self):
        return self.error['description']

    @staticmethod
    def handle(exception, req, res, error=None):

        if isinstance(exception, AppError):
            res.status = exception.status
            error = {'code': exception.code, 'message': exception.title}
            if exception.description:
                error['description'] = exception.description
            res.body = falcon.json.dumps({'error': error})
        elif isinstance(exception, falcon.HTTPNotFound):
            error = {'code': RESOURCE_NOT_FOUND_EXCEPTION['code'], 'message': RESOURCE_NOT_FOUND_EXCEPTION['title']}
            res.status = RESOURCE_NOT_FOUND_EXCEPTION['status']
            res.body = falcon.json.dumps({'error': error})
        elif isinstance(exception, NoResultFound):
            error = {'code': RESOURCE_NOT_FOUND_EXCEPTION['code'], 'message': RESOURCE_NOT_FOUND_EXCEPTION['title']}
            res.status = RESOURCE_NOT_FOUND_EXCEPTION['status']
            res.body = falcon.json.dumps({'error': error})
        else:
            error_msg = traceback.format_exc()
            error = {'code': ERR_UNKNOWN['code'], 'message': error_msg}
            res.status = ERR_UNKNOWN['status']
            res.body = falcon.json.dumps({'error': error})
            logger.error(error_msg)

class ResourceNotFoundException(AppError):
    def __init__(self, description=None):
        super().__init__(RESOURCE_NOT_FOUND_EXCEPTION)
        self.error['description'] = description


class InvalidRequestException(AppError):
    def __init__(self, description=None):
        super().__init__(INVALID_REQUEST_EXCEPTION)
        self.error['description'] = description