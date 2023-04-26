from backend.extensions import db


class History(db.Model):
    __tablename__ = "histories"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    channel_view_count = db.Column(db.Float, unique=False)
    channel_elapsed_time = db.Column(db.Float, unique=False)
    video_count = db.Column(db.Float, unique=False)
    subscriber_count = db.Column(db.Float, unique=False)
    channel_comment_count = db.Column(db.Float, unique=False)
    video_category_id = db.Column(db.Float, unique=False)
    likes = db.Column(db.Float, unique=False)
    dislikes = db.Column(db.Float, unique=False)
    comments = db.Column(db.Float, unique=False)
    elapsed_time = db.Column(db.Float, unique=False)
    video_published = db.Column(db.DateTime, unique=False)

    def __init__(self, channel_view_count, channel_elapsed_time, video_count, subscriber_count, channel_comment_count,
                 video_category_id, likes, dislikes, comments, elapsed_time, video_published):
        self.channel_view_count = channel_view_count
        self.channel_elapsed_time = channel_elapsed_time
        self.video_count = video_count
        self.subscriber_count = subscriber_count
        self.channel_comment_count = channel_comment_count
        self.video_category_id = video_category_id
        self.likes = likes
        self.dislikes = dislikes
        self.comments = comments
        self.elapsed_time = elapsed_time
        self.video_published = video_published
