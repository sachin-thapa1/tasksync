import os

workers = 1
threads = 2
bind = "0.0.0.0:" + os.getenv("PORT", "10000")
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"