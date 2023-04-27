from datetime import datetime

from backend.database.history import History

def save_history(req_body):
    try:
        date = datetime.strptime(req_body["video_published"], "%Y-%m-%d")
        history = History(req_body["user_id"], req_body["channel_view_count"], req_body["channel_elapsed_time"],
                          req_body["channel_video_count"], req_body["channel_subscriber_count"],
                          req_body["channel_comment_count"], req_body["video_category_id"], req_body["likes"],
                          req_body["dislikes"], req_body["comments"], req_body["elapsed_time"], date)
        history.save()
        return {"message": "Successfully saved history", "status_code": 201}
    except ValueError:
        return {"message": "History was not saved", "status_code": 400}


def read_history(user_id):
    history = History.find_all_by_id(record_id=user_id)
    histories = [history[i].to_dict() for i in range(len(history))]
    return {"histories": histories, "status_code": 200}
