# encoding:utf-8
"""
Handles all geoprocessing requests and results
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import importlib.util
from json import dumps
from os import listdir
from os.path import basename, dirname, exists, join as osjoin

from geoprocessing import config


class GPRequestHandler(BaseHTTPRequestHandler):
    """
    Handles request for GP Services
    """
    # Get Request
    def do_GET(self):

        # Response status code

        print(self.path)

        request_gp, data_fields = self.path.split('?')

        if '.' in request_gp:
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('invalid directory', 'utf8'))
            return

        else:
            print('got request')

            script_dir = request_gp.split('/')[1]
            script_basename = request_gp.split('/')[2]

            script_name = f'{script_basename}.py'

            print([script_dir, script_basename, script_name])

            script_path = ''

            for f in listdir(config.VIRTUAL_DIRECTORY):
                if f == script_dir:
                    print('got dir')
                    for j in listdir(osjoin(config.VIRTUAL_DIRECTORY,
                                            script_dir)):
                        if j.lower() == script_name.lower():
                            script_path = osjoin(config.VIRTUAL_DIRECTORY,
                                                 script_dir,
                                                 script_name)
                            break
                    else:
                        print('cannot find file')
                        self.send_response(403)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(bytes('invalid request', 'utf8'))
                        return
                    break
            else:
                print('cannot find directory')
                self.send_response(403)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes('invalid request', 'utf8'))
                return

            scr_spec = importlib.util.spec_from_file_location(script_basename,
                                                              script_path)

            script_mod = importlib.util.module_from_spec(scr_spec)

            scr_spec.loader.exec_module(script_mod)

            print(script_mod.CONFIG_INFO)

            data_list = data_fields.split('&')
            if len(data_list) != len(script_mod.CONFIG_INFO['inputs']):
                print('invalid inputs')
                self.send_response(403)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes('invalid number of inputs', 'utf8'))

            params = []
            for i, data_item in enumerate(data_list):
                name, value = data_item.split('=')
                params.append(script_mod.CONFIG_INFO['inputs'][i](name, value))

            results = script_mod.CONFIG_INFO['main_function'](*params)

            result_data = {}
            for param in results:
                result_data[param.name] = param.value

            result_text = dumps(result_data)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(result_text, 'utf8'))


def run():
    print('Starting server...')

    # Server settings
    server_address = ('localhost', 80)
    httpd = HTTPServer(server_address, GPRequestHandler)
    print('Running server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()



