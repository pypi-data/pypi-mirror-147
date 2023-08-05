import os
import re
import time
import xml.etree.ElementTree as ET

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class MyHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        FileSystemEventHandler.__init__(self)
        self.counter = 0
        self.file_path = file_path
        self.pattern = re.compile("[a-zA-Z0-9]\/\.[a-zA-Z0-9].")
        self.clean_content()

    def on_moved(self, event):
        if event.is_directory:
            return

        if self.file_path != event.dest_path:
            return

        print(f"{self.counter}: {event.dest_path}")
        self.clean_content(5)
        self.counter += 1

    def clean_content(self, num_to_check=0):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        bookmarks = root.findall('bookmark')

        if num_to_check > len(bookmarks) or num_to_check <= 0:
            num_to_check = len(bookmarks)

        bookmarks = bookmarks[-num_to_check:]

        changed = False
        for bookmark in bookmarks:
            path = bookmark.attrib['href']
            res = re.search(self.pattern, path)
            if res:
                root.remove(bookmark)
                changed = True
                print("Match!")
        if changed:
            tree.write(self.file_path)


def run():
    path = os.path.join(os.environ["HOME"], ".local", "share")
    observer = Observer()
    handler = MyHandler(os.path.join(path, "recently-used.xbel"))
    observer.schedule(handler, path, recursive=False)
    observer.daemon = True
    observer.start()
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    run()