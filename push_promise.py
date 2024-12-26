import re
from misc import *
from errors import *

class Promise:
    def __init__(self, tls_socket, request, curr_stream_id, content):
        self.stream_id = curr_stream_id + 2
        self.curr_stream_id = curr_stream_id
        self.request = request
        self.socket = tls_socket
        self.content = content

    def make_promise(self, resource_name, content, status):
        """
        Function that sends the first PUSH_PROMISE frame
        """
        headerBF = make_frame({
            "status": f"{status}",
            "content-type": f"text/{resource_name.split(".")[0]}",
            "date": f"{datetime.now()}",
            "content-length": f"{len(content)}"
        })

        header_frame = {
            "length": len(headerBF),
            "type": 5, # 5 for PUSH_PROMISE
            "flags": 4, # 4 for END_HEADERS
            "stream-identifier": self.curr_stream_id,
            "promised-stream-id": self.stream_id,
            "header-block-fragment": b64_encode(headerBF)
        }
        self.stream_id += 2

        send(self.socket, make_frame(header_frame))

    def find_promised(self, content):
        """
        Function that takes in content of a file and checks for any embedded files and returns their names/paths
        If no paths found returns empty list
        """
        try:
            found_embd = re.findall("[\"][a-zA-Z\S]+[.][a-zA-Z\S]+[\"]", content)
        except re.PatternError:
            print_cmd("No match found.")
            return []

        found_emb_rt = []

        for match in found_embd:
            found_emb_rt.append(match.replace("\"", ""))

        return found_emb_rt

    def get_promised(self, path):
        try:
            with open(path) as file:
                return file.read()
        except FileNotFoundError:
            print("No resource found. (THIS SHOULDN'T HAPPEN)")

    def keep_promise(self, content, stream_id):
        """
        Function to send DATA frames for a promised resource
        """
        data_frame = {
            "length": len(content),
            "type": 0, # 0 for DATA
            "flags": 1, # 1 for END_STREAM
            "stream-identifier": stream_id,
            "payload": f"{content}",
        }

        send(self.socket, make_frame(data_frame))

    def __main__(self):
        emb_files = self.find_promised(self.content) # get embedded files

        stream_ids = []

        if emb_files != []:
            for resource in emb_files:
                # MAKE PROMISES
                content = self.get_promised(resource)
                stream_ids.append(self.stream_id)
                self.make_promise(self.request, resource, content, self.request["status"])
        
            for resource, stream_id in zip(emb_files, stream_ids):
                content = self.get_promised(resource)
                self.keep_promise(content, stream_id)

        raise PromiseError("No embedded resources found.")
