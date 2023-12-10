from typing import List

import strawberry

from api.model.note import Note


class Notes:
    def __init__(self):
        self.data = []

    def all(self) -> List[Note]:
        return self.data

    def add(self, content: str) -> Note:
        note = Note(id=strawberry.ID(content), content=content)
        self.data.append(note)
        return note
