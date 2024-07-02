import json
import httpx
import enum


class TelegramExceptions(str, enum.Enum):
    UNKNOWN_ERROR = "Unknown error"
    GAME_NOT_FOUND_EXCEPTION = "Game not found"
    BOOKING_ALREADY_EXISTS_EXCEPTION = "Booking already exists"


class TelegramException(Exception):
    def __init__(
        self,
        exception_type: TelegramExceptions = TelegramExceptions.UNKNOWN_ERROR,
        title: str = "Something went wrong",
        description: str = "Something went wrong, please try again",
    ) -> None:
        self.exception_type = exception_type
        match exception_type:
            case TelegramExceptions.GAME_NOT_FOUND_EXCEPTION:
                self.title = title
                self.description = description

            case TelegramExceptions.BOOKING_ALREADY_EXISTS_EXCEPTION:
                self.title = "Booking already exists"
                self.description = "You can't book a game that already booked"

            case _:
                self.title = "Something went wrong"
                self.description = "Something went wrong, please try again"

    def __str__(self):
        return f"{self.title}\n{self.description}"


def process_fastapi_error(response: httpx.Response) -> TelegramException:
    err = json.loads(response.text)

    print("status code: ", response.status_code)
    print("detail: ", err["detail"])

    raise TelegramException()
