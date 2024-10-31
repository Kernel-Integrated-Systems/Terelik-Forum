from datetime import datetime
from pydantic import BaseModel


class Reply(BaseModel):
    reply_id: int or None = None
    content: str
    user_id: int or None = None
    topic_id: int or None = None
    created_at: datetime = datetime.now()


class Vote(BaseModel):
    reply_id: int
    vote_type: int  # 1 for upvote / 0 for downvote


class VoteResponse(BaseModel):
    reply_id: int
    vote_type: str  # 'upvote' or 'downvote'
    created_at: datetime = datetime.now()

class NewReply(BaseModel):
    topic_id: int
    content: str

class BestReply(BaseModel):
    topic_id: int
    reply_id: int


