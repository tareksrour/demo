from flask import Flask, Response
from pymongo.mongo_client import MongoClient
import threading
import ast
import datetime
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask("API")
kwargs = {"socketTimeoutMS": 3000, "retryWrites": True}

client = MongoClient("mongodb-primary", replicaSet="rs0", **kwargs)


def parse_type(s):
    try:
        value = ast.literal_eval(s)
    except:
        try:
            value = datetime.datetime.strptime(s, '%m/%d/%Y')
            return value
        except:
            return s
    else:
        return value


class Watcher:
    DIRECTORY_TO_WATCH = "/tmp/watched/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        print("******Starting watching directory "+self.DIRECTORY_TO_WATCH)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error Watching Directory")

        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, ):
        super().__init__()

    @staticmethod
    def on_any_event(event, **kwargs):
        print("****"+event.event_type+"  "+event.src_path+"*****")
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            try:
                print("Importing for - %s." % event.src_path)
                cols = None
                data_list = []
                count=0
                with open(event.src_path, 'r') as file:
                    for line in file:
                        data = line.strip().split(",")
                        if cols:
                            data = [parse_type(x) for x in data]
                            d = dict(zip(cols, data))
                            data_list.append(d)
                            count+=1
                            if count%100==0:
                                done = False
                                while not done:
                                    try:
                                        client.data.imported.insert_many(data_list)
                                        done = True
                                        data_list.clear()
                                        print("%d Entries Imported" % (count,),end="\r")
                                    except Exception as e:
                                        time.sleep(5)
                        else:
                            cols = data
                    if len(data_list)>0:
                        done = False
                        while not done:
                            try:
                                client.data.imported.insert_many(data_list)
                                done = True
                                data_list.clear()
                            except Exception as e:
                                time.sleep(5)
                print("%d Entries Imported from - %s." % (count, event.src_path))
            except Exception as e:
                print(e)


@app.route("/web")
def list_db():
    try:
        cols = list(client.data.imported.find_one().keys())

        del cols[0]

        def generate():
            yield "<style>\n" + \
                  "table, th, td {\n" + \
                  "border: 1px solid black;\n" + \
                  "border-collapse: collapse;\n" + \
                  "}\n" + \
                  "</style>\n" + \
                  "<table>\n" + \
                  "<tr>"
            for x in cols:
                yield "<th>" + x + "</th>"
            yield "</tr>"
            for row in client.data.imported.find():
                yield "<tr>"
                for x in cols:
                    yield "<td>" + str(row[x]) + "</td>"
                yield "</tr>"
            yield "</table>"

        return Response(generate(), mimetype="text/html")
    except:
        return "No Data", 412


class FlaskThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        app.run(host="0.0.0.0",port=8000)


class WatcherThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        Watcher().run()


if __name__ == '__main__':
    f_thread = FlaskThread()
    w_thread = WatcherThread()
    f_thread.start()
    w_thread.start()
    f_thread.join()
    w_thread.join()
