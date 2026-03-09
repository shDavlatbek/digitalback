from celery import shared_task


@shared_task
def test_task():
    """
    Simple test task to verify Celery is working
    """
    return "Celery is working correctly!"
