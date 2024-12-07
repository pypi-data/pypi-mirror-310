# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import ast
import logging
import threading
import time
import uuid

import pyarrow
import pyarrow.flight


logger = logging.getLogger('__main__.' + __name__)

class FlightServer(pyarrow.flight.FlightServerBase):
    def __init__(self, host="localhost", location=None,
                 tls_certificates=None, verify_client=False,
                 root_certificates=None, auth_handler=None, middleware=None):
        super(FlightServer, self).__init__(
            location, auth_handler, tls_certificates, verify_client,
            root_certificates, middleware)
        self.flights = {}
        self.host = host
        self.tls_certificates = tls_certificates
        self.location = location

    @classmethod
    def descriptor_to_key(self, descriptor):
        return (descriptor.descriptor_type.value, descriptor.command,
                tuple(descriptor.path or tuple()))

    def _make_flight_info(self, key, descriptor, table):
        if self.tls_certificates:
            location = pyarrow.flight.Location.for_grpc_tls(
                self.host, self.port)
        else:
            location = pyarrow.flight.Location.for_grpc_tcp(
                self.host, self.port)
        endpoints = [pyarrow.flight.FlightEndpoint(repr(key), [location]), ]

        mock_sink = pyarrow.MockOutputStream()
        stream_writer = pyarrow.RecordBatchStreamWriter(
            mock_sink, table.schema)
        stream_writer.write_table(table)
        stream_writer.close()
        data_size = mock_sink.size()

        return pyarrow.flight.FlightInfo(table.schema,
                                         descriptor, endpoints,
                                         table.num_rows, data_size)

    def list_flights(self, context, criteria):
        for key, table in self.flights.items():
            if key[1] is not None:
                descriptor = \
                    pyarrow.flight.FlightDescriptor.for_command(key[1])
            else:
                descriptor = pyarrow.flight.FlightDescriptor.for_path(*key[2])

            yield self._make_flight_info(key, descriptor, table)

    def get_flight_info(self, context, descriptor):
        key = FlightServer.descriptor_to_key(descriptor)
        logger.info(f"get_flight_info: key={key}")
        if key in self.flights:
            table = self.flights[key]
            return self._make_flight_info(key, descriptor, table)
        raise KeyError('Flight not found.')

    def do_put(self, context, descriptor, reader, writer):
        key = FlightServer.descriptor_to_key(descriptor)
        logger.info(f"do_put: key={key}")
        self.flights[key] = reader.read_all()

    def do_get(self, context, ticket):
        logger.info(f"do_get: ticket={ticket}")
        key = ast.literal_eval(ticket.ticket.decode())
        if key not in self.flights:
            logger.warn(f"do_get: key={key} not found")
            return None
        logger.info(f"do_get: returning key={key}")
        flight = self.flights.pop(key)
        return pyarrow.flight.RecordBatchStream(flight)

    def list_actions(self, context):
        return iter([
            ("getUniquePath", "Get a unique FlightDescriptor path to put data to."),
            ("clear", "Clear the stored flights."),
            ("shutdown", "Shut down this server."),
        ])

    def do_action(self, context, action):
        logger.info(f"do_action: action={action.type}")
        if action.type == "getUniquePath":
            uniqueId = str(uuid.uuid4())
            logger.info(f"getUniquePath id={uniqueId}")
            yield uniqueId.encode('utf-8')
        elif action.type == "clear":
            self._clear()
        elif action.type == "healthcheck":
            pass
        elif action.type == "shutdown":
            self._clear()
            yield pyarrow.flight.Result(pyarrow.py_buffer(b'Shutdown!'))
            # Shut down on background thread to avoid blocking current
            # request
            threading.Thread(target=self._shutdown).start()
        else:
            raise KeyError("Unknown action {!r}".format(action.type))

    def _clear(self):
        """Clear the stored flights."""
        self.flights = {}

    def _shutdown(self):
        """Shut down after a delay."""
        logger.info("Server is shutting down...")
        time.sleep(2)
        self.shutdown()

def start(server):
    logger.info(f"Serving on {server.location}")
    server.serve()


if __name__ == '__main__':
    start()