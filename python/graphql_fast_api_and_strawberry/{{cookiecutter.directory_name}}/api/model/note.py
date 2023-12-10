import strawberry


@strawberry.type
class Note:
    id: strawberry.ID
    content: str
