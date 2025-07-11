from datetime import datetime, timedelta, timezone
from quality_gates.utils.logger import logger


def convertTime(isotime):
    try:
        form_time = datetime.fromisoformat(isotime).strftime("%d.%m.%Y %H:%M")
    except Exception as e:
        print(e)
        return isotime
    return form_time


def timeValidate(start_time,end_time):
    """
    Checker for allow time for running build on production ( MSK TZ )
    This checker get time in UTC and make timedelta +3 hours to current time, then check maintenance window for deploy
    If time allow in production maintenance window, method return True if not allowed return False
    """
    Msk = (datetime.now(timezone.utc) + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

    logger.info(f"Current time Msk: {Msk}")
    if (Msk > start_time) and ( Msk < end_time):
        logger.info("Time is in production maintenance window")
        return {
            "status": True,
            "message": "Time is in production maintenance window"
        }
    else:
        logger.info("Time is not in production maintenance window")
        return {
            "status": False,
            "message": "Time is not in production maintenance window"
        }
