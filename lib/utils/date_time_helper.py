import datetime

#
# Simple date time helper class
#
class DateTimeHelper():
    # Constants
    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%H.%M.%S'
    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    #
    # Gets the full date time as a DateTime object.
    #
    @staticmethod
    def get_date_time():
        return datetime.datetime.now()

    #
    # Gets the seconds since now and the start time provided.
    #
    @staticmethod
    def get_seconds_since_now(start_date_time):
        end_date_time = DateTimeHelper.get_date_time()
        delta = end_date_time - start_date_time
        return delta.total_seconds()

    #
    # Gets now as a date (no time) string.
    #
    @staticmethod
    def get_date_now_str():
        return DateTimeHelper._get_now_str(DateTimeHelper.DATE_FORMAT)

    #
    # Gets now as a time (no date) string.
    #
    @staticmethod
    def get_time_now_str():
        return DateTimeHelper._get_now_str(DateTimeHelper.TIME_FORMAT)

    #
    # Gets now as a datetime string.
    #
    @staticmethod
    def get_date_time_now_str():
        return DateTimeHelper._get_now_str(DateTimeHelper.DATE_TIME_FORMAT)

    #
    # Helper that others call into, passing only the format.
    #
    @staticmethod
    def _get_now_str(format):
        return datetime.datetime.now().strftime(format)
