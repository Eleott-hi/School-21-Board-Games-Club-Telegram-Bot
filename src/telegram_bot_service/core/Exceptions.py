import json
import httpx
import enum


class TelegramExceptions(str, enum.Enum):
    UNKNOWN_EXCEPTION = "Unknown exception"
    CUSTOM_EXCEPTION = "Custom exception"
    GAME_NOT_FOUND_EXCEPTION = "Game not found"
    BOOKING_ALREADY_EXISTS_EXCEPTION = "Booking already exists"
    BOOKING_NOT_FOUND_EXCEPTION = "Booking not found"
    REGISTRATION_FAILD_EXCEPTION = "Registration faild exception"


class TelegramException(Exception):
    def __init__(
        self,
        exception_type: TelegramExceptions = TelegramExceptions.UNKNOWN_EXCEPTION,
        title: str = "Unknown exception",
        description: str = "Something went wrong, please try again",
    ) -> None:
        self.exception_type = exception_type

        match exception_type:
            case TelegramExceptions.CUSTOM_EXCEPTION:
                self.title = title
                self.description = description

            case TelegramExceptions.GAME_NOT_FOUND_EXCEPTION:
                self.title = "Game not found"
                self.description = "Can not find game"

            case TelegramExceptions.BOOKING_ALREADY_EXISTS_EXCEPTION:
                self.title = "Booking already exists"
                self.description = "You can't book a game that already booked"

            case TelegramExceptions.BOOKING_NOT_FOUND_EXCEPTION:
                self.title = "Booking not found"
                self.description = "There is no such booking"

            case TelegramExceptions.REGISTRATION_FAILD_EXCEPTION:
                self.title = "Registration faild"
                self.description = "Something went wrong while registration process.Please, check your input"

            case _:
                self.exception_type = TelegramExceptions.UNKNOWN_EXCEPTION
                self.title = "Unknown error"
                self.description = "Something went wrong, please try again"

    def __str__(self):
        return f"{self.title}\n{self.description}"


def process_fastapi_error(response: httpx.Response) -> TelegramException:
    err = json.loads(response.text)

    print("status code: ", response.status_code)
    print("detail: ", err["detail"])

    raise TelegramException()
