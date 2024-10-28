from datetime import datetime
from pydantic import BaseModel


class Reply(BaseModel):
    reply_id: int or None = None
    content: str
    user_id: int or None = None
    topic_id: int or None = None
    created_at: datetime = datetime.now()


class Vote(BaseModel):
    vote_id: int | None = None
    user_id: int
    reply_id: int
    vote_type: str  # 'upvote' or 'downvote'
    created_at: datetime = datetime.now()


class NewReply(BaseModel):
    topic_id: int
    content: str

class GetReplyOnTopic(BaseModel):
    topic_id: int
    reply_id: int


class VoteRequest(BaseModel):
    vote: str
