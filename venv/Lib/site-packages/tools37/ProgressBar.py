from datetime import datetime


class ProgressBar:
    def __init__(self, data: list):
        self.data: list = data
        self.length: int = len(data)
        self.number: int = 0
        self.start: datetime = datetime.now()

    def __iter__(self):
        for index, item in enumerate(self.data):
            self.number = index + 1
            yield item

    def percent(self) -> int:
        return int(100 * self.number / self.length)

    def estimate(self) -> str:
        seconds = int((datetime.now() - self.start).total_seconds() * (self.length - self.number) / self.number)

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if days > 0:
            return f"{days}d {str(hours).zfill(2)}h {str(minutes).zfill(2)}m {str(seconds).zfill(2)}s"
        elif hours > 0:
            return f"{str(hours).zfill(2)}h {str(minutes).zfill(2)}m {str(seconds).zfill(2)}s"
        elif minutes > 0:
            return f"{str(minutes).zfill(2)}m {str(seconds).zfill(2)}s"
        else:
            return f"{str(seconds).zfill(2)}s"

    @property
    def progress(self) -> str:
        slen = len(str(self.length))
        return f"{str(self.number).zfill(slen)}/{str(self.length)}"
