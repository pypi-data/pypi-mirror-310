import logging


class BaseError(Exception):
    """
    Base class for all errors in the payment system.

    Attributes:
        code (str or int): Error code identifying the type of error.
        message (str): A human-readable error message.
        data (dict, optional): Additional context or metadata for the error.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, code=None, message=None, data=None, *args, **kwargs):
        """
        Initialize the BaseError instance.

        Args:
            code (str or int, optional): Error code identifying the error type.
            message (str, optional): Human-readable error description.
            data (dict, optional): Additional context or metadata.
            *args: Additional positional arguments for exception context.
            **kwargs: Additional keyword arguments for exception context.
        """
        # Use default values if none provided
        code = code or "UNKNOWN_ERROR"
        message = message or "An unspecified error occurred."

        super().__init__(message)

        self.code = code
        self.data = data
        self.args = args
        self.kwargs = kwargs

        # Structured logging for better insights
        self.logger.error(
            f"[{self.__class__.__name__}] Code: {code}, Message: {message}, "
            f"Data: {data}, Args: {args}, Kwargs: {kwargs}",
            exc_info=True
        )

    def __repr__(self):
        """Provide a developer-friendly string representation."""
        return (
            f"<{self.__class__.__name__} code={self.code!r} message={self.message!r} "
            f"data={self.data!r}>"
        )


class CardError(BaseError):
    """Base class for card-related errors."""


class TransportError(CardError):
    """Transport error occurred during card operation."""
    message = "Transport error."

    def __init__(self, data=None):
        super().__init__(-32300, self.message, data)


class ParseError(CardError):
    """Parse error occurred during card operation."""
    message = "Parse error."

    def __init__(self, data=None):
        super().__init__(-32700, self.message, data)


class InvalidRequestError(CardError):
    """Invalid request made during card operation."""
    message = "Invalid Request."

    def __init__(self, data=None):
        super().__init__(-32600, self.message, data)


class InvalidResponseError(CardError):
    """Invalid response received during card operation."""
    message = "Invalid Response."

    def __init__(self, data=None):
        super().__init__(-32600, self.message, data)


class SystemError(CardError):
    """System error occurred during card operation."""
    message = "System error."

    def __init__(self, data=None):
        super().__init__(-32400, self.message, data)


class MethodNotFoundError(CardError):
    """Method not found during card operation."""
    message = "Method not found."

    def __init__(self, data=None):
        super().__init__(-32601, self.message, data)


class InvalidParamsError(CardError):
    """Invalid parameters provided during card operation."""
    message = "Invalid Params."

    def __init__(self, data=None):
        super().__init__(-32602, self.message, data)


class InvalidTokenFormat(CardError):
    """Invalid token format during card operation."""
    message = "Invalid token format."

    def __init__(self, data=None):
        super().__init__(-32500, self.message, data)


class AccessDeniedError(CardError):
    """Access denied for the card operation."""
    message = "Access denied."

    def __init__(self, data=None):
        super().__init__(-32504, self.message, data)


class CardNotFoundError(CardError):
    """Card not found during operation."""
    message = "Card not found."

    def __init__(self, data=None):
        super().__init__(-31400, self.message, data)


class SmsNotConnectedError(CardError):
    """SMS notification not connected."""
    message = "SMS notification not connected."

    def __init__(self, data=None):
        super().__init__(-31301, self.message, data)


class CardExpiredError(CardError):
    """Card has expired."""
    message = "Card has expired."

    def __init__(self, data=None):
        super().__init__(-31301, self.message, data)


class CardBlockedError(CardError):
    """Card is blocked."""
    message = "Card is blocked."

    def __init__(self, data=None):
        super().__init__(-31301, self.message, data)


class CorporateCardError(CardError):
    """Financial operations with corporate cards are not allowed."""
    message = "Financial operations with corporate cards are not allowed."

    def __init__(self, data=None):
        super().__init__(-31300, self.message, data)


class BalanceError(CardError):
    """Unable to retrieve card balance. Please try again later."""
    message = "Unable to retrieve card balance. Please try again later."

    def __init__(self, data=None):
        super().__init__(-31302, self.message, data)


class InsufficientFundsError(CardError):
    """Insufficient funds on the card."""
    message = "Insufficient funds on the card."

    def __init__(self, data=None):
        super().__init__(-31303, self.message, data)


class InvalidCardNumberError(CardError):
    """Invalid card number provided."""
    message = "Invalid card number."

    def __init__(self, data=None):
        super().__init__(-31300, self.message, data)


class CardNotFoundWithNumberError(CardError):
    """Card with the provided number not found."""
    message = "Card with this number not found."

    def __init__(self, data=None):
        super().__init__(-31300, self.message, data)


class InvalidExpiryDateError(CardError):
    """Invalid expiry date provided for the card."""
    message = "Invalid expiry date for the card."

    def __init__(self, data=None):
        super().__init__(-31300, self.message, data)


class ProcessingServerError(CardError):
    """Processing center server is unavailable. Please try again later."""
    message = \
        "Processing center server is unavailable. Please try again later."

    def __init__(self, data=None):
        super().__init__(-31002, self.message, data)


# OTP Module Errors

class OtpError(BaseError):
    """Base class for OTP-related errors."""


class OtpSendError(OtpError):
    """Error occurred while sending OTP."""
    message = "Error occurred while sending SMS. Please try again."

    def __init__(self, data=None):
        super().__init__(-31110, self.message, data)


class OtpCheckError(OtpError):
    """Base class for OTP check errors."""


class OtpExpiredError(OtpCheckError):
    """OTP code has expired. Request a new code."""
    message = "OTP code has expired. Request a new code."

    def __init__(self, data=None):
        super().__init__(-31101, self.message, data)


class OtpAttemptsExceededError(OtpCheckError):
    """
    Number of attempts to enter the code has been exceeded. Request a new code.
    """
    message = "Number of attempts to enter the code has been exceeded."

    def __init__(self, data=None):
        super().__init__(-31102, self.message, data)


class OtpInvalidCodeError(OtpCheckError):
    """Invalid OTP code entered."""
    message = "Invalid OTP code."

    def __init__(self, data=None):
        super().__init__(-31103, self.message, data)


class PaymeNetworkError(BaseError):
    """Network error occurred during request to Payme server."""
    message = "Network error occurred during request to Payme server."

    def __init__(self, data=None):
        super().__init__(self.message, data)


class ReceiptsNotFoundError(BaseException):
    """No receipts found for the given transaction ID."""
    def __init__(self, message="No receipts found for the given transaction ID.", data=None):
        super().__init__(message, data)


class UnknownError(BaseException):
    """An unknown error occurred."""
    def __init__(self, message="An unknown error occurred.", data=None):
        super().__init__(message, data)


errors_map = {
    -32300: TransportError,
    -32700: ParseError,
    -32600: InvalidRequestError,
    -32601: MethodNotFoundError,
    -32602: InvalidParamsError,
    -32504: AccessDeniedError,
    -31400: CardNotFoundError,
    -31301: SmsNotConnectedError,
    -31302: BalanceError,
    -31303: InsufficientFundsError,
    -31300: InvalidCardNumberError,
    -31002: ProcessingServerError,
    -31110: OtpSendError,
    -31101: OtpExpiredError,
    -31102: OtpAttemptsExceededError,
    -31103: OtpInvalidCodeError,
    -31602: ReceiptsNotFoundError,
    -32500: InvalidTokenFormat,
    "UNKNOWN_ERROR": UnknownError
}
