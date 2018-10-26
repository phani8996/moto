from .exceptions import ModelNotFoundError, InvalidDataTypeError, InvalidValueError, \
    RequiredParameterMissingError

models = {
    'start_query_execution': {
        'QueryString': {'datatype': str, 'required': True},
        'ClientRequestToken': {'datatype': str, 'required': False},
        'QueryExecutionContext': {'datatype': dict, 'required': False, 'fields': {
            'Database': {'datatype': str, 'required': True}
        }},
        'ResultConfiguration': {'datatype': dict, 'required': False, 'fields': {
            'OutputLocation': {'datatype': str, 'required': True},
            'EncryptionConfiguration': {'datatype': dict, 'required': False, 'fields': {
                'EncryptionOption': {'datatype': str, 'required': True,
                                     'allowed_values': ['SSE_S3', 'SSE_KMS', 'CSE_KMS']},
                'KmsKey': {'datatype': str, 'required': True}
            }}
        }},
    }
}


class ValidateModel(object):
    def __init__(self, model):
        if model not in models:
            raise ModelNotFoundError(model)
        self.model = models[model]

    def validate(self, **kwargs):
        for argument in self.model:
            validation = self.model[argument]
            value = kwargs[argument]
            required = validation['required']
            datatype = validation['datatype']
            fields = None
            allowed_values = None
            denied_values = None
            if 'fields' in validation:
                fields = validation['fields']
            if 'allowed_values' in validation:
                allowed_values = validation['allowed_values']
            if 'denied_values' in validation:
                denied_values = validation['denied_values']
            # Raise error if required argument is missing
            if required and argument not in kwargs:
                raise RequiredParameterMissingError
            # skip to next field if non compulsory field is missing
            if argument not in kwargs:
                continue
            if type(value) != datatype:
                raise InvalidDataTypeError(argument, datatype, type(value))
            if allowed_values and value not in allowed_values:
                raise InvalidValueError(argument, not_in_allowed_values=True)
            if denied_values and value in denied_values:
                raise InvalidValueError(argument, not_in_allowed_values=False)
            # TODO: validate iteratively for iterative datatypes like dict, list
            return True
