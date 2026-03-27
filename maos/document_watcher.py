import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WatchHandler(FileSystemEventHandler):

    def __init__(self,callback):
        self.callback=callback

    def on_created(self,event):

        if not event.is_directory:
            self.callback(event.src_path)

def start_watcher(folder,callback):

    handler=WatchHandler(callback)

    observer=Observer()
    observer.schedule(handler,folder,recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
