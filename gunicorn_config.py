# Gunicorn configuration file

# Logging settings
accesslog = '/var/log/tts/gunicorn_access.log'  # The path to the access log file
errorlog = '/var/log/tts/gunicorn_error.log'    # The path to the error log file
loglevel = 'info'                               # The granularity of error log outputs
capture_output = True                           # Redirect stdout/stderr to the error log
