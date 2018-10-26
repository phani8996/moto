from __future__ import unicode_literals
from moto.core.exceptions import RESTError


class AthenaBadRequestError(RESTError):
    code = 400


class ClientRequestTokenError(AthenaBadRequestError):

    def __init__(self, clientRequestToken):
        super(ClientRequestTokenError, self).__init__("ClientRequestTokenError",
                                                      "Token {0} does not match submitted query"
                                                      .format(clientRequestToken))


class ModelNotFoundError(AthenaBadRequestError):

    def __init__(self, model_name):
        super(ModelNotFoundError).__init__("ModelNotFoundError", "Model - {0} not found".format(model_name))


class InvalidDataTypeError(AthenaBadRequestError):

    def __init__(self, field, required_datatype, actual_datatype):
        super(InvalidDataTypeError).__init__("InvalidDataTypeError", "Expected {0} of type {1} but found {1}"
                                             .format(field, type(required_datatype).__name__,
                                                     type(actual_datatype).__name__))


class RequiredParameterMissingError(AthenaBadRequestError):

    def __init__(self, field):
        super(RequiredParameterMissingError).__init__("RequiredParameterMissingError", "Parameter {0} missing"
                                                      .format(field))


class InvalidValueError(AthenaBadRequestError):

    def __init__(self, field, not_in_allowed_values=False):
        if not_in_allowed_values:
            super(InvalidDataTypeError).__init__("InvalidValueError", "{0} value is not in allowed values"
                                                 .format(field))
        else:
            super(InvalidDataTypeError).__init__("InvalidValueError", "{0} value is in denied values"
                                                 .format(field))


class InvalidModelError(AthenaBadRequestError):

    def __init__(self, model, ex):
        super(InvalidModelError).__init__(InvalidModelError, "Exception occurred while validating {0}".format(model),
                                          ex)
