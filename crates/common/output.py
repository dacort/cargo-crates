from datetime import datetime, timezone


class OutputRecord:
    def __init__(self, record, path_template) -> None:
        self._record = record
        self._template = path_template

    def path(self):
        # I realize this is *dangerous* but
        # a) It's what I want to do and
        # b) I control the input :)

        # There *MUST* be a better way to do this
        json = lambda k: self.json(k)
        today = lambda: self.today()

        return eval(f"f'{self._template}'")

    def json(self, path):
        """
        Currently only supports top-level attributes
        """
        return self._record.get(path)

    def today(self):
        return f"{datetime.now(tz=timezone.utc).date()}"