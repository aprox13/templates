from typing import List

import strawberry
from dependency_injector.wiring import Provide

from api.routes import query, mutation
from dependencies import AppDependencies
from api.model.note import Note
from services.notes import Notes


@strawberry.type
class NotesQuery:
    @query()
    def all(self, service: Notes = Provide[AppDependencies.notes]) -> List[Note]:
        return service.all()


@strawberry.type
class NotesMutation:
    @mutation()
    def add(
        self, content: str, service: Notes = Provide[AppDependencies.notes]
    ) -> Note:
        return service.add(content)
