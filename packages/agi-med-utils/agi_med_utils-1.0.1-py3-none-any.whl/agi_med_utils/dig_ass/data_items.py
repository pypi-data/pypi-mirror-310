import typing as t


class ReplicaItem:
    def __init__(self, replica: dict[str, t.Any]) -> None:
        self.Body = replica["Body"]
        self.Role = replica["Role"]
        self.DateTime = replica["DateTime"]
        self.State = replica.get("State", "")

    def to_dict(self) -> dict[str, t.Any]:
        return self.__dict__


class InnerContextItem:
    def __init__(self, inner_context: dict[str, list[dict[str, t.Any]]]) -> None:
        self.Replicas = [ReplicaItem(r) for r in inner_context["Replicas"]]

    def to_dict(self) -> dict[str, list[dict[str, t.Any]]]:
        return {"Replicas": [r.to_dict() for r in self.Replicas]}


class OuterContextItem:
    def __init__(self, outer_context: dict[str, t.Any]) -> None:
        self.Sex = outer_context["Sex"]
        self.Age = outer_context["Age"]
        self.UserId = outer_context["UserId"]
        self.SessionId = outer_context["SessionId"]
        self.ClientId = outer_context["ClientId"]
        self.TrackId = outer_context.get("TrackId", "")

    def to_dict(self) -> dict[str, t.Any]:
        return self.__dict__


class ChatItem:
    def __init__(self, chat: dict[str, t.Any]) -> None:
        self.OuterContext = OuterContextItem(chat["OuterContext"])
        self.InnerContext = InnerContextItem(chat["InnerContext"])

    def to_dict(self) -> dict[str, t.Any]:
        return {"OuterContext": self.OuterContext.to_dict(), "InnerContext": self.InnerContext.to_dict()}
