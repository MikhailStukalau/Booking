from fastapi import HTTPException, status


class BookingExceptions(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingExceptions):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists!"


class IncorrectEmailOrPasswordException(BookingExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class TokenExpiredException(BookingExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class TokenAbsentException(BookingExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token is missing"


class IncorrectTokenFormatException(BookingExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(BookingExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingExceptions):
    status_code = status.HTTP_409_CONFLICT
    detail = "There are no available rooms left"
