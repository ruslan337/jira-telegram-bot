import os
from config import db_dir, attach_dir, log_dir
def init_dirs():
    try:
        os.mkdir(db_dir)
    except:
        pass
    try:
        os.mkdir(attach_dir)
    except:
        pass
    try:
        os.mkdir(log_dir)
    except:
        pass
