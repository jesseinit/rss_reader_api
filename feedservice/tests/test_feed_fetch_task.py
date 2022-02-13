import feedservice.tasks as Tasks
import pytest
from celery.exceptions import Retry


@pytest.mark.usefixtures("celery_session_app")
@pytest.mark.usefixtures("celery_session_worker")
class TestFeedUpdateTask:
    def test_background_task_backoff(self, mocker):
        """Test to check that feed task raises error"""

        mocker.patch("feedservice.tasks.update_feed_and_items", side_effect=Retry("something happened"))
        with pytest.raises(Retry):
            Tasks.update_feed_and_items()
