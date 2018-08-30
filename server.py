#coding:utf-8
#!/usr/bin/env python
# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE
# Written by Nathan Hamiel (2010)

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import random
import json
import xlrd
import xlwt
import csv
from xlutils.copy import copy
import os.path
from pathlib import Path

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        f = open("index.html", "r")
        self.wfile.write(f.read())

    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        data = json.loads(self.data_string, strict=False)

        # Extract data from JSON POST and verify exists
        user_name = data['userName']
        full_name = data['fullName']
        diskutil_status = data['diskutilStatus']

        # Get IP address of sender
        ip_address = self.client_address[0]
        response_sent = 0

        # Verify all variables exist
        if user_name and full_name and diskutil_status:
            self.send_response(200)
            response_sent = 200
        else:
            self.send_response(400)
            response_sent = 400

        # Print incoming POST data
        print("\n -------------------------> ")
        print("\nUsername = " + user_name)
        print("Full Name = " + full_name)
        print("\nDiskUtil Status = \n" + diskutil_status)
        print("\nIP Address From = " + ip_address)
        print("Response Sent = " + str(response_sent) + "\n")
        print(" <------------------------- \n")

        self.print_to_spreadsheet(data, response_sent)
        return

    def print_to_spreadsheet(self, data, response_sent):

        # Read book
        rb = xlrd.open_workbook('encrypt_results.xls', formatting_info=True)

        # Make a copy of book
        book = copy(rb)
        sheet = book.get_sheet(0)

        # Get the number of last row
        i = rb.sheet_by_index(0).nrows

        # Write to the next row
        sheet.write(i, 0, data['userName'])
        sheet.write(i, 1, data['fullName'])
        sheet.write(i, 2, data['diskutilStatus'])
        sheet.write(i, 3, self.client_address[0])
        sheet.write(i, 4, response_sent)

        book.save('encrypt_results.xls')
        print 'Wrote new entry to encrypt_results.xls...'

def run(server_class=HTTPServer, handler_class=S, port=8080, host='192.168.10.3'):

    # Setup server config
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)

    # Check if spreadsheet already exists, if not - create
    my_file = Path("encrypt_results.xls")

    if not my_file.is_file():
        print 'Creating new spreadsheet to house results...'
        create_spreadsheet()

    print 'Starting httpd on ' + host + ':' + str(port) +'...'
    httpd.serve_forever()

def create_spreadsheet():

    # If you need to create a book, do this
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("PySheet1")

    # Define widths of columns
    sheet1.col(0).width = 256 * 20
    sheet1.col(1).width = 256 * 20
    sheet1.col(2).width = 256 * 40
    sheet1.col(3).width = 256 * 20
    sheet1.col(4).width = 256 * 20

    # Make font bold for headers
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True
    style.font = font

    sheet1.write(0, 0, "Username", style=style)
    sheet1.write(0, 1, "Full Name", style=style)
    sheet1.write(0, 2, "Diskutil APFS Status", style=style)
    sheet1.write(0, 3, "User IP Address", style=style)
    sheet1.write(0, 4, "HTTP Response", style=style)

    book.save('encrypt_results.xls')
    print 'Created spreadsheet and saved as encrypt_results.xls'
    return

if __name__ == "__main__":
    run()
