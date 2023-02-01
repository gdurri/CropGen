import datetime

class DateTimeHelper():
    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%H.%M.%S'
    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    @staticmethod
    def _get_date_time():
        return datetime.datetime.now()

    @staticmethod
    def _get_seconds_since_now(start_date_time):
        end_date_time = DateTimeHelper._get_date_time()
        delta = end_date_time - start_date_time
        return delta.total_seconds()

    @staticmethod
    def _get_date_now_str():
        return DateTimeHelper._get_now_str(DateTimeHelper.DATE_FORMAT)

    @staticmethod
    def _get_time_now_str():
        return DateTimeHelper._get_now_str(DateTimeHelper.TIME_FORMAT)

    @staticmethod
    def _get_date_time_now_str():
        return DateTimeHelper._get_now_str(DateTimeHelper.DATE_TIME_FORMAT)

    @staticmethod
    def _get_now_str(format):
        return datetime.datetime.now().strftime(format)
