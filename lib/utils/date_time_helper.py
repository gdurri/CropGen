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
    def get_elapsed_seconds_since(start_date_time):
        end_date_time = DateTimeHelper.get_date_time()
        delta = end_date_time - start_date_time
        return delta.total_seconds()
    
    #
    # Gets the time since now as a time string.
    #
    @staticmethod
    def get_elapsed_time_since(start_date_time):
        return DateTimeHelper.seconds_to_hhmmss_ms(
            DateTimeHelper.get_elapsed_seconds_since(start_date_time)
        )
    
    #
    # convert seconds to hh:mm:ss
    #
    @staticmethod
    def seconds_to_hhmmss_ms(seconds):
        # Calculate the hours, minutes, and remaining seconds
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        # Extract milliseconds
        milliseconds = int((seconds % 1) * 1000)
        
        # Create a formatted time string
        time_string = '{:02d}:{:02d}:{:02d}.{:03d}'.format(hours, minutes, seconds, milliseconds)
        
        return time_string
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
