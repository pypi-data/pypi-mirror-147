"""
Should Include:
Basic error classes and their descriptors
"""


class ErrorHandle():
    """Class that handles errors the user can identify / recover from
    """

    handleName = "Generic Error Handle: "

    @classmethod
    def __init__(self, msg, *msgs, **extra):
        msg = str(msg)
        _msgs = [str(m) for m in msgs]
        _msgs = '\n'.join(_msgs)
        self.msg = f"{self.handleName}\n{msg}\n{_msgs}"
        self.extras = extra

    def __str__(self):
        return f"{self.msg}"


class UserErrorHandle(ErrorHandle):
    handleName = "User Error Handle: "


class ProgrammerErrorHandle(ErrorHandle):
    handleName = "Programmer Error Handle: "


class Error(Exception):
    """Exception class that is root of all custom exceptions
    """

    def __init__(self, msg, *msgs, errorHandle: ErrorHandle = ..., **extra):
        msg = str(msg)
        _msgs = [str(m) for m in msgs]
        _msgs = '\n'.join(_msgs)
        self.msg = f"Message: \n{msg}\n{_msgs}"
        self.extras = extra
        self.errorHandle = errorHandle

    def __str__(self):
        return f"{self.msg}\n" + "\n".join(f"{k}: {v}" for k, v in self.extras.items()) + f"\n{str(self.errorHandle)}"


class SafeCatchAll(Error, Exception):
    """Use instead of "catch Exception:" to catch all safe-to-catch exceptions

    This is to allow for a custom error deriving from errors.Error to indicate a system shutdown and not have to change any code
    """
    ...

class ProgrammerError(Error):
    """Exception class that is root of all internal / implementation / programmer related errors
    """
    ...


class InappropriateRequest(ProgrammerError):
    """Exception class that is raised when a request on some programming object / function / property is inappropriate
    """
    ...


class SimpleUserError(Error):
  """Error class used to refer to errors that are not programmer errors

  Args:
      Error (str / strings): Represents the error message and attached error handles
  """
  ...
