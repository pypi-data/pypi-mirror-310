class BaseParserError(Exception): ...


class ItemNotFoundError(BaseParserError):
    def __init__(self, msg: str, *, item_id: int | None = None):
        self.item_id = item_id
        self.msg = msg
        super().__init__(self.msg)
