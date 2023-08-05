#----- The cloud request handler class
import _cloud
import time
from _encoder import *
import math

class CloudRequests:

    def __init__(self, cloud_connection : _cloud.CloudConnection):
        print("\033[1mIf you use CloudRequests in your Scratch project, please credit TimMcCool!\033[0m")
        self.connection = cloud_connection
        self.project_id = cloud_connection.project_id
        self.requests = []
        self.current_var = 1

    def request(self, function):

        self.requests.append(function)

    def event(self, function):

        if function.__name__ == "on_ready":
            self.on_ready = function

    def _respond(self, request_id, response):

        remaining_response = str(response)

        i = 0
        while not remaining_response == "":
            if len(remaining_response) > 220:
                response_part = remaining_response[:220]
                remaining_response = remaining_response[220:]

                i+=1
                if i > 9:
                    iteration_string = str(i)
                else:
                    iteration_string = "0"+str(i)

                self.connection.set_var(f"FROM_HOST_{self.current_var}", f"{response_part}.{request_id}{iteration_string}1")
                self.current_var += 1
                if self.current_var == 10:
                    self.current_var = 1
                time.sleep(0.1)
            else:
                self.connection.set_var(f"FROM_HOST_{self.current_var}", f"{remaining_response}.{request_id}2222")
                self.current_var += 1
                if self.current_var == 10:
                    self.current_var = 1

                remaining_response = ""
                time.sleep(0.1)



    def run(self):
        self.on_ready()
        self.last_data = _cloud.get_cloud_logs(self.project_id, limit=100)
        self.last_timestamp = 0

        while True:
            data = _cloud.get_cloud_logs(self.project_id, limit=100)
            if data == []:
                continue
            data.reverse()
            if not self.last_data == data:
                for activity in data:
                    if activity['timestamp'] > self.last_timestamp and activity['name'] == "☁ TO_HOST":
                        self.last_timestamp = activity['timestamp']

                        raw_request, request_id = activity["value"].split(".")
                        request = Encoding.decode(raw_request)
                        arguments = request.split("&")
                        request = arguments.pop(0)

                        commands = list(filter(lambda k: k.__name__ == request, self.requests))
                        if len(commands) == 0:
                            print("Unknown command issued")
                            continue
                        else:
                            try:
                                if len(arguments) == 0:
                                    output = commands[0]()
                                elif len(arguments) == 1:
                                    output = commands[0](arguments[0])
                                elif len(arguments) == 2:
                                    output = commands[0](arguments[0],arguments[1])
                                else:
                                    print("Too many arguments")
                                    output = Encoding.encode("Error: Too many arguments")
                            except Exception as e:
                                self._respond(request_id, Encoding.encode("Error: Check the Python script"))
                                raise(e)
                        print(isinstance(output, list))

                        if not isinstance(output, list):
                            output = Encoding.encode(output)
                        else:
                            input = output
                            output = ""
                            for i in input:
                                output += Encoding.encode(i)
                                output += "89"
                        self._respond(request_id, output)
