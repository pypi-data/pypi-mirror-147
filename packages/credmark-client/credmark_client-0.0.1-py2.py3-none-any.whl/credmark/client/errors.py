import logging

logger = logging.getLogger(__name__)


class ModelBaseError(Exception):
    """
    Base error class for Credmark model errors.

    The main error types are:
     - ``ModelDataError``: An error that occurs during the lookup, generation,
       or processing of data. It is not an error in the code but an
       but an unexpected situation with the data. For example, a request
       for a contract at an address that does not exist will return a
       ``ModelDataError``. This error is considered deterministic and permanent,
       in the sense that for the given context, the same error will always occur.

     - ``ModelInputError``: An error that occurs when the input data for a
       model is being validated. Usually it is caused by missing fields,
       fields of the wrong type, or conficting data. In the returned error
       the last stack entry is the model whose input triggered the error.

     - ``ModelRunError``: An error that occurs during the running of a model.
       This error is usually related to a model coding error or
       not properly handling exceptions from web3, math libraries etc.
       These errors are considered transient because it is expected
       they could give a different result if run again, for example
       if the code was fixed or a web3 connection issue was resolved etc.

     - ``ModelEngineError``: An error occurred in the model running engine.
       These errors are considered transient because they usually
       relate to network or resource issues.

    Error data is available at ``error.data``
    """

    # Map of class name to class
    class_map = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.class_map[cls.__name__] = cls

    @ classmethod
    def class_for_name(cls, name: str):
        """
        Return a specific error class for a name.
        Must be a subclass of ``ModelBaseError``.
        """
        return cls.class_map.get(name)

    def __init__(self, message: str,
                 **data):
        super().__init__(message)
        self.data = data

    def dict(self):
        """
        Return a dict for the error data
        """
        return self.data


class ModelDataError(ModelBaseError):
    """
    An error that occurs during the lookup, generation, or
    processing of data this is considered deterministic and
    permanent, in the sense that for the given context, the
    same error will always occur.

    A model may raise a ``ModelDataError`` in situations such as:
     - the requested data does not exist or is not available for
       the current context block number.
     - the input data is incomplete, references non-existent
       items, or cannot be processed
    """


class ModelRunError(ModelBaseError):
    """
    An error that occurs during the running of a model.

    This error is usually related to a model coding error or
    not properly handling exceptions from web3, math libraries etc.

    A ``ModelRunError`` will terminate the model run of a parent model.

    These errors are considered transient because it is expected
    they could give a different result if run again, for example
    if the code was fixed or a web3 connection issue was resolved
    etc.
    """


class ModelInputError(ModelBaseError):
    """
    An error that occurs when invalid input is sent to a model.
    The message describes the invalid or missing fields.

    The last model on the call stack is the model that received the
    invalid input.
    """


class ModelInvalidStateError(ModelRunError):
    """
    A request was made that conflicts with the current context,
    for example `context.run_model()` was called with a block number higher
    than the block number of the current context.

    Although these errors are permanent for a given context,
    these are considered a logic or coding error.
    """


class ModelTypeError(ModelRunError):
    """
    There was an error in a model while converting data to a DTO class.
    This can happen when constructing a new DTO instance, for example
    from a model run output.

    Although these errors are permanent for a given context,
    these are considered a logic or coding error.
    """


class ModelOutputError(ModelRunError):
    """
    There was an error validating the output of the model.

    Although these errors are permanent for a given context,
    these are considered a logic or coding error.
    """


class ModelNoContextError(ModelRunError):
    """
    An attempt was made to use a core data object outside
    the context of a model run.
    """


class MaxModelRunDepthError(ModelRunError):
    """
    Models successively calling `context.run_model()` with nesting too deep.
    """


class ModelEngineError(ModelBaseError):
    """
    An error occurred before, during, or after a model run
    relating to the runner engine and not the model code itself.

    These errors are considered transient.
    """


class ModelRunRequestError(ModelEngineError):
    """
    An error occurred when a model requested another model to run.

    These errors are considered transient.
    """


class ModelNotFoundError(ModelEngineError):
    """
    A model requested to run was not found.

    The detail contains the fields:
    - slug: Slug of model not found
    - version: Version of model not found
    """


def create_instance_from_error_dict(err_obj: dict) -> ModelBaseError:
    err_type = err_obj.get('type')
    del err_obj['type']

    message = err_obj.get('message')
    if message is None:
        err_obj['message'] = message = 'Unknown model engine error'

    if err_type:
        err_class = ModelBaseError.class_for_name(err_type)
    else:
        err_class = ModelEngineError

    if err_class is not None:
        try:
            return err_class(**err_obj)
        except Exception as e:
            logger.error(f'Error creating error {err_type} instance: {e}')
    else:
        logger.error(f'Missing error class for error type {err_type}')

    raise ModelEngineError(f'{err_type}: {message}')
