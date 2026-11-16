import http.server
import socket
import os
import sys
import urllib.parse
import re

PORT = 5501
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

MIME_MAP = {
    '.wasm': 'application/wasm',
    '.buf': 'application/octet-stream',
    '.sog': 'application/octet-stream',
    '.riv': 'application/octet-stream',
    '.webp': 'image/webp',
    '.avif': 'image/avif',
    '.json': 'application/json',
    '.js': 'application/javascript',
    '.mjs': 'application/javascript',
    '.css': 'text/css',
    '.mp4': 'video/mp4',
    '.woff2': 'font/woff2',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
}

class AmitFastHandler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def setup(self):
        super().setup()
        # Set short socket timeout to prevent hung connections on Windows
        if hasattr(self, 'request') and self.request:
            try:
                self.request.settimeout(5.0)
            except Exception:
                pass

    def address_string(self):
        # Avoid reverse DNS lookup delay on Windows
        return self.client_address[0]

    def guess_type(self, path):
        base, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext in MIME_MAP:
            return MIME_MAP[ext]
        return super().guess_type(path)

    def translate_path(self, path):
        path = path.split('?', 1)[0].split('#', 1)[0]
        path = urllib.parse.unquote(path)
        
        clean_path = path.lstrip('/')
        if clean_path in ('', 'index.htm'):
            clean_path = 'index.html'
            
        local_path = os.path.normpath(os.path.join(DIRECTORY, clean_path))
        if os.path.exists(local_path):
            return local_path

        # Fallback 1: Mobile variant fallback to desktop
        if '_MOBILE.' in clean_path:
            cand = clean_path.replace('_MOBILE.', '.')
            cand_path = os.path.normpath(os.path.join(DIRECTORY, cand))
            if os.path.exists(cand_path):
                return cand_path

        # Fallback 2: Wasm location flexibility (_astro or root)
        if clean_path.endswith('.wasm'):
            name = os.path.basename(clean_path)
            in_astro = os.path.join(DIRECTORY, '_astro', name)
            in_root = os.path.join(DIRECTORY, name)
            if os.path.exists(in_astro):
                return in_astro
            if os.path.exists(in_root):
                return in_root

        # Fallback 3: Wearable gallery full webp to thumbs webp if full is missing
        if 'wearable-gallery' in clean_path and clean_path.endswith('.webp') and 'thumbs' not in clean_path:
            name = os.path.basename(clean_path)
            thumb_path = os.path.join(DIRECTORY, 'images', 'wearable-gallery', 'thumbs', name)
            if os.path.exists(thumb_path):
                return thumb_path

        return local_path

    def end_headers(self):
        self.send_header('Connection', 'close')
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.close_connection = True
        super().end_headers()

    def do_GET(self):
        self.close_connection = True
        path = self.translate_path(self.path)
        
        if os.path.isdir(path):
            index_path = os.path.join(path, "index.html")
            if os.path.exists(index_path):
                path = index_path
            else:
                self.send_error(404, "File not found")
                return

        if not os.path.exists(path) or not os.path.isfile(path):
            self.send_error(404, "File not found")
            return

        range_header = self.headers.get('Range')
        file_size = os.path.getsize(path)
        ctype = self.guess_type(path)

        if range_header and range_header.startswith('bytes='):
            # HTTP Range Request
            try:
                range_match = re.search(r'bytes=(\d+)-(\d*)', range_header)
                if not range_match:
                    return self._serve_full(path, file_size, ctype)

                start = int(range_match.group(1))
                end = int(range_match.group(2)) if range_match.group(2) else file_size - 1

                if start >= file_size or end >= file_size or start > end:
                    self.send_response(416)
                    self.send_header('Content-Range', f'bytes */{file_size}')
                    self.end_headers()
                    return

                length = end - start + 1
                self.send_response(206)
                self.send_header('Content-Type', ctype)
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.send_header('Content-Length', str(length))
                self.end_headers()

                with open(path, 'rb') as f:
                    f.seek(start)
                    sent = 0
                    buf_size = 64 * 1024
                    while sent < length:
                        to_read = min(buf_size, length - sent)
                        chunk = f.read(to_read)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        sent += len(chunk)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, TimeoutError, socket.timeout):
                pass
            except Exception as e:
                try:
                    self.send_error(500, str(e))
                except Exception:
                    pass
            return

        self._serve_full(path, file_size, ctype)

    def _serve_full(self, path, file_size, ctype):
        try:
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(file_size))
            self.end_headers()

            with open(path, 'rb') as f:
                buf_size = 64 * 1024
                while True:
                    chunk = f.read(buf_size)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, TimeoutError, socket.timeout):
            pass
        except Exception as e:
            try:
                self.send_error(500, str(e))
            except Exception:
                pass

    def log_message(self, format, *args):
        status = args[1] if len(args) > 1 else ''
        path = args[0] if len(args) > 0 else ''
        if str(status).startswith('4'):
            print(f"[\033[91m{status}\033[0m] {path}")
        else:
            print(f"[{status}] {path}")

class ThreadingV4Server(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET
    daemon_threads = True

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

def main():
    os.chdir(DIRECTORY)
    server_address = ("0.0.0.0", PORT)
    httpd = ThreadingV4Server(server_address, AmitFastHandler)

    url_localhost = f"http://localhost:{PORT}/"
    url_ip = f"http://127.0.0.1:{PORT}/"
    print("=" * 65)
    print("  AMIT AI - High-Performance Non-Blocking Local Server")
    print(f"  Localhost: {url_localhost}")
    print(f"  Direct IP: {url_ip}")
    print("  Connection Pool Stalling: PREVENTED (Fast socket recycle)")
    print("  HTTP/1.1 Range & Explicit Content-Length: ENABLED")
    print("=" * 65)
    print("Listening for requests... Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
