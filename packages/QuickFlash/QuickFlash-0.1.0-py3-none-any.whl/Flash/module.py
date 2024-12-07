import asyncio
import json
import inspect
import os
import mimetypes
import re
from urllib.parse import parse_qs

class Next:
    def __init__(self):
        pass

class Request:
    def __init__(self, reader):
        self.reader = reader
        self.body = None
        self.path = None
        self.method = None
        self.params = {}

class Response:
    STATUS_MESSAGES = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }

    def __init__(self, writer):
        self.writer = writer
        self.status_code = 200

    def status(self, code):
        self.status_code = code

    def send(self, content, content_type="text/html"):
        status_message = self.STATUS_MESSAGES.get(self.status_code, "Unknown Status")
        
        if not isinstance(content, str):
            content = str(content)
        
        response_headers = (
            f"HTTP/1.1 {self.status_code} {status_message}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(content.encode())}\r\n"
            "\r\n"
        )
        
        print(f"Raw Response:\n{response_headers}{content}")
        
        try:
            self.writer.write(response_headers.encode())  # Write headers
            self.writer.write(content.encode())           # Write body
        except Exception as e:
            print(f"Error sending response: {e}")
        finally:
            self.writer.close()  
    
    def sendFile(self,file_path):
        if os.path.exists(file_path):
            try:
                content_type, _ = mimetypes.guess_type(file_path)
                content_type = content_type or "application/octet-stream"
                with open(file_path,'rb') as file:
                    content = file.read()

                    response_headers = (
                            "HTTP/1.1 200 OK\r\n"
                            f"Content-Length: {len(content)}\r\n"
                            f"Content-Type: {content_type}\r\n"
                            "Connection: close\r\n\r\n"
                        )
                    self.writer.write(response_headers.encode() + content)
            except Exception as e:
                print(e)
                return
        else:
            response_headers = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Length: 0\r\n"
            "Connection: close\r\n\r\n"
            )
            self.writer.write(response_headers.encode())
        self.writer.close()

    def json(self,content, content_type="application/json"):
        status_message = self.STATUS_MESSAGES.get(self.status_code, "")
            
        json_response = json.dumps(content)
        
        self.writer.write(f"HTTP/1.1 {self.status_code} {status_message}\r\n".encode())
        self.writer.write(f"Content-Type: {content_type}\r\n".encode())
        self.writer.write(f"Content-Length: {len(json_response)}\r\n".encode())
        self.writer.write("\r\n".encode())
        self.writer.write(json_response.encode())
        self.writer.close()

class Node:
    def __init__(self):
        self.get = []
        self.post = []
        self.patch = []
        self.delete = []
        self.middleware = []
        self.children = {}

    def addHandler(self, method, handler):
        if method == "get":
            self.get.append(handler)
        elif method == "post":
            self.post.append(handler)
        elif method == "patch":
            self.patch.append(handler)
        elif method == "delete":
            self.delete.append(handler)
        elif method == "middleware":
            self.middleware.append(handler)

    def addChildren(self, path, childNode):
        self.children[path] = childNode

class Flash:
    def __init__(self):
        self.root = Node()
        self.Host = "0.0.0.0"
        self.middleware = []

    def get(self, path, callback):
        self.registerRoutes("get", path, callback)

    def post(self, path, callback):
        self.registerRoutes("post", path, callback)

    def patch(self, path, callback):
        self.registerRoutes("patch", path, callback)

    def delete(self, path, callback):
        self.registerRoutes("delete", path, callback)
    
    def use(self,middleware=None,path=None):
        if path is None:
            self.middleware.append(middleware)
        else:
            self.registerRoutes("middleware",path,middleware)

    def registerRoutes(self, method, path, callback):
        currentNode = self.root
        normalized_path = path.rstrip('/') or '/'
        if normalized_path == "/":
            pass
        else:
            parts = list(filter(None, normalized_path.split('/')))
            for part in parts:
                if part not in currentNode.children:
                    currentNode.addChildren(part, Node())
                currentNode = currentNode.children[part]

        if method == "get" and currentNode.get:
            raise ValueError(f"Route '{path}' with GET method is already defined.")
        elif method == "post" and currentNode.post:
            raise ValueError(f"Route '{path}' with POST method is already defined.")
        elif method == "patch" and currentNode.patch:
            raise ValueError(f"Route '{path}' with PATCH method is already defined.")
        elif method == "delete" and currentNode.delete:
            raise ValueError(f"Route '{path}' with DELETE method is already defined.")

        if method == "middleware":
            if isinstance(callback,self.Router):
                self._addMiddlewareRoutes(callback.root, currentNode)
            else:
                currentNode.addHandler(method,callback)
        else:
            currentNode.addHandler(method, callback)        

    def _addMiddlewareRoutes(self, middlewareRoot, targetNode):
        for method in ['get', 'post', 'patch', 'delete']:
                handlers = getattr(middlewareRoot, method, [])
                for handler in handlers:
                    targetNode.addHandler(method, handler)
        
        for route, childNode in middlewareRoot.children.items():
            if route not in targetNode.children:
                targetNode.addChildren(route, Node())
            childTargetNode = targetNode.children[route]

            for handler in childNode.get:
                childTargetNode.addHandler('get', handler)
            for handler in childNode.post:
                childTargetNode.addHandler('post', handler)
            for handler in childNode.patch:
                childTargetNode.addHandler('patch', handler)
            for handler in childNode.delete:
                childTargetNode.addHandler('delete', handler)

            self._addMiddlewareRoutes(childNode, childTargetNode)

    async def handleRequest(self, method, path, req, writer):
        req.method = method.upper()
        req.path = path
        res = Response(writer)

        async def next_middleware(index=0):
            if index < len(self.middleware):
                await self.middleware[index](req, res, lambda: next_middleware(index + 1))
            else:
                await self.routeRequest(method, path, req, res)

        await next_middleware()

    async def routeRequest(self, method, path, req, res):
        currentNode = self.root

        normalized_path = path.rstrip('/') or '/'
        if normalized_path == "/":
            pass
        else:
            parts = list(filter(None, normalized_path.split('/')))
            for part in parts:
                matched = False
                for child_key, child_node in currentNode.children.items():
                    if child_key.startswith(':'):
                        param_name = child_key.lstrip(':')
                        req.params[param_name] = part
                        currentNode = child_node
                        matched = True
                        break
                    elif child_key == part: 
                        currentNode = child_node
                        matched = True
                        break
                if not matched:
                    res.status(404)
                    res.send(f"Cannot {method.upper()} {path}")
                    return
        
        if len(currentNode.middleware) >0 :
            async def next_middleware(index=0):
                if index < len(currentNode.middleware):
                    await currentNode.middleware[index](req,res,lambda:next_middleware(index + 1))
            await next_middleware()

        handlers = []
        if method == "get":
            handlers = currentNode.get
        elif method == 'post':
            handlers = currentNode.post
        elif method == 'patch':
            handlers = currentNode.patch
        elif method == 'delete':
            handlers = currentNode.delete

        if not handlers:
            res.status(404)
            res.send(f"Cannot {method.upper()} {path}")
            return

        async def next_handler(index=0):
            if index < len(handlers):
                handler_func = handlers[index]
                if inspect.iscoroutinefunction(handler_func):
                    await handler_func(req, res)
                else:
                    handler_func(req, res)
                await next_handler(index + 1)

        await next_handler()

    async def handle_client(self, reader, writer):
        request_line = await reader.readline()
        if not request_line:
            writer.close()
            await writer.wait_closed()
            return

        request_line = request_line.decode().strip()
        method, path, _ = request_line.split(" ", 2)

        headers = {}
        while True:
            header_line = await reader.readline()
            if header_line == b"\r\n":
                break 
            header_line = header_line.decode().strip()
            key, value = header_line.split(":", 1)
            headers[key.strip()] = value.strip()
        
        req = Request(reader)
        req.method = method.upper()
        req.path = path
        req.headers = headers 

        await self.handleRequest(method.lower(), path, req, writer)

    @staticmethod
    def urlencoded(extended=False):
        def parse_nested_form_data(form_data):
            result = {}
            for key,value in form_data.items():
                current_level = result
                parts = re.split(r'\[|\]',key)
                parts = [part for part in parts if part]

                for i,part in enumerate(parts):
                    if i == len(parts)-1:
                        current_level[part] = value[0]
                    else:
                        if part not in current_level:
                            current_level[part] = {}
                        current_level = current_level[part]
            return result
        
        async def middleware(req,res,next):
            content_length = req.headers.get("Content-Length")
            content_type = req.headers.get("Content-Type")
            if content_type == "application/x-www-form-urlencoded" and int(content_length) > 0:
                try:
                    body = await req.reader.read(int(content_length))
                    form_data =parse_qs(body.decode("utf-8"))
                    if extended:
                        form_data = parse_nested_form_data(form_data)
                        req.body = form_data
                    else:
                        req.body = form_data
                except Exception as e:
                    print(f"Error parsing urlencoded data: {e}")
                    req.body = {} 
            await next()
        return middleware

    @staticmethod
    def cors(options=None):
        if options is None:
            options = {}
        
        allowed_origins = options.get("origin", "*")
        allowed_methods = options.get("methods", "GET, POST, PUT, DELETE, OPTIONS")
        allowed_headers = options.get("allowedHeaders", "Content-Type, Authorization")
        exposed_headers = options.get("exposedHeaders", "")
        allow_credentials = options.get("credentials", False)
        max_age = options.get("maxAge", None)

        async def middleware(req,res,next):
            res.writer.write(f"Access-Control-Allow-Origin: {allowed_origins}\r\n".encode())
            res.writer.write(f"Access-Control-Allow-Methods: {allowed_methods}\r\n".encode())
            res.writer.write(f"Access-Control-Allow-Headers: {allowed_headers}\r\n".encode())
            if exposed_headers:
                res.writer.write(f"Access-Control-Expose-Headers: {exposed_headers}\r\n".encode())
            if allow_credentials:
                res.writer.write(f"Access-Control-Allow-Credentials: true\r\n".encode())
            if max_age is not None:
                res.writer.write(f"Access-Control-Max-Age: {max_age}\r\n".encode())
            
            if req.method == "OPTIONS":
                res.status(204)
                res.send("")
                return

            await next()
            
        return middleware

    @staticmethod
    def static(folder):
        async def middleware(req, res, next):
            static_file_path = os.path.join(folder, req.path.lstrip('/'))
            try:
                if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
                    mime_type, _ = mimetypes.guess_type(static_file_path)
                    mime_type = mime_type or 'application/octet-stream'

                    loop = asyncio.get_event_loop()
                    with open(static_file_path, 'rb') as file:
                        content = await loop.run_in_executor(None, file.read)

                    res.writer.write(f"HTTP/1.1 200 OK\r\n".encode())
                    res.writer.write(f"Content-Type: {mime_type}\r\n".encode())
                    res.writer.write(f"Content-Length: {len(content)}\r\n".encode())
                    res.writer.write("\r\n".encode())
                    res.writer.write(content)
                    res.writer.close()
                else:
                    await next()
            except Exception as err:
                print(f"Error in static middleware: {err}")
                await next()

        return middleware

    def set(self,name,value):
        if name == 'views':
            self.data[name] = value
            pass
        else:
            self.data[name] = value

    def listen(self, port, callback):
        async def start():
            server = await asyncio.start_server(self.handle_client, self.Host, port)
            addr = server.sockets[0].getsockname()
            callback(addr)

            async with server:
                await server.serve_forever()

        asyncio.run(start())

    class Json:
        def __init__(self):
            self.data = None
    
        async def read_headers(self,req):
            content_length = req.headers.get("Content-Length")
            content_type = req.headers.get("Content-Type")
            return content_length, content_type

        async def __call__(self, req, res, next):
            if req.method in ['POST', 'PUT', 'PATCH']:
                content_length, content_type = await self.read_headers(req)
                if content_type == 'application/json':
                    try:
                        raw_data = await req.reader.read(content_length)
                        req.body = json.loads(raw_data.decode())
                    except Exception as e:
                        print(e)
                        req.body = {}
                        return
            await next()
    
    class Router:
        def __init__(self):
            self.root = Node()
            self.currentPath = None
        
        def registerRoutes(self,path=None,method=None,callback=None):
            currentNode = self.root
            normalized_path = path.rstrip('/') or '/'
            if normalized_path == "/":
                pass
            else:
                parts = list(filter(None, normalized_path.split('/')))
                for part in parts:
                    if part not in currentNode.children:
                        currentNode.addChildren(part,Node())
                    currentNode = currentNode.children[part]

            if method == 'get' and currentNode.get:
                raise ValueError(f"Route '{path}' with GET method is already defined.")
            elif method == 'post' and currentNode.post:
                raise ValueError(f"Route '{path}' with POST method is already defined.")
            elif method == 'patch' and currentNode.patch:
                raise ValueError(f"Route '{path}' with PATCH method is already defined.")
            elif method == 'delete' and currentNode.delete:
                raise ValueError(f"Route '{path}' with DELETE method is already defined.")
            
            if method and callback:
                currentNode.addHandler(method,callback)
        
        def route(self,path):
            self.currentPath = path
            return self
        
        def get(self, path=None, callback=None):
            if callable(path):
                callback = path
                finalPath = self.currentPath
            else:
                finalPath = path if path else self.currentPath
            if not finalPath:
                raise ValueError("Path is required for the route.")
            
            self.registerRoutes(finalPath, 'get', callback)
            self.currentPath = None
            return self

        def post(self, path=None, callback=None):
            if callable(path):
                callback = path
                finalPath = self.currentPath
            else:
                finalPath = path if path else self.currentPath
            if not finalPath:
                raise ValueError("Path is required for the route.")
            
            self.registerRoutes(finalPath, 'post', callback)
            self.currentPath = None
            return self
        
        def patch(self, path=None, callback=None):
            if callable(path):
                callback = path
                finalPath = self.currentPath
            else:
                finalPath = path if path else self.currentPath
            if not finalPath:
                raise ValueError("Path is required for the route.")
            
            self.registerRoutes(finalPath, 'patch', callback)
            self.currentPath = None
            return self
        
        def delete(self, path=None, callback=None):
            if callable(path):
                callback = path
                finalPath = self.currentPath
            else:
                finalPath = path if path else self.currentPath
            if not finalPath:
                raise ValueError("Path is required for the route.")
            
            self.registerRoutes(finalPath, 'delete', callback)
            self.currentPath = None
            return self
                
