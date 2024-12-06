import os
import shutil

def prepare_log_folder() -> None:
    if not os.path.exists('logs'):
        os.makedirs('logs')
        os.makedirs(os.path.join('logs', 'package_logs'))
    else:
        shutil.rmtree('logs')
        os.makedirs('logs')
        os.makedirs(os.path.join('logs', 'package_logs'))