from jeeachinto.universal_lock import Lock
import socket, time
from kthread import KThread
import uuid
from . import utils

class Server:
    def __init__(self,bind_ip="0.0.0.0",bind_port=4545):
        self.clienttable = {}
        self.clienttablelock = Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.heartbeater_thread = KThread(target=self.heartbeater)

    def heartbeater(self):
        while True:
            with self.clienttablelock:
                testtable = list(dict(self.clienttable).items())
            testtable.sort(key=lambda a: a[1]["checked"])
            if len(testtable) > 0:
                client_name = testtable[0][0]
                try:
                    self.send_msg_client(client_name)
                except Exception:
                    utils.pdbg(client_name,"disconnected!")
                    utils.pexc()
                    conn = testtable[0][1]["conn"]
                    try:
                        conn.close()
                    except Exception:
                        pass
                    with self.clienttablelock:
                        try:
                            if self.clienttable[client_name]["conn"] == conn:
                                self.clienttable[client_name]["thread"].kill()
                                del self.clienttable[client_name]
                        except Exception:
                            pass
            time.sleep(1)

                

    def start(self):
        self.socket.bind((self.bind_ip, self.bind_port))
        self.socket.listen()
        self.heartbeater_thread.start()
        while True:
            conn, _ = self.socket.accept()
            self.client_accept_handle(conn)
            utils.pdbg("Status:",list(self.clienttable.keys()))


    def recv_msg_client(self, client):
        return utils.socket_msg_recv(client)

    def send_msg_client(self, client_name, header={}, body=b""):
        self.clienttablelock.acquire()
        if client_name in self.clienttable:
            target = self.clienttable[client_name]
            self.clienttablelock.release()
            target["lock"].acquire()
            target["conn"].settimeout(utils.TIMEOUT_SOCKS)
            try:
                target["conn"].sendall(utils.msg_encode(header,body))
            finally:
                target["conn"].settimeout(None)
                target["checked"] = time.time()
                target["lock"].release()
        else:
            self.clienttablelock.release()

    def send_msg_to_client(self, by, to, body):
        self.clienttablelock.acquire()
        if to in self.clienttable:
            self.clienttablelock.release()
            self.send_msg_client(to,{
                "action":"recv",
                "by": by
            },body)
            self.send_msg_client(by,{
                "action":"send-status",
                "status":None
            })
        else:
            self.clienttablelock.release()
            self.send_msg_client(by,{
                "action":"send-status",
                "status":"Target name not subscribed!"
            })

    def client_listener(self, client_name):
        with self.clienttablelock:
            try:
                conn = self.clienttable[client_name]["conn"]
            except Exception:
                return
        while True:
            try:
                header, data = self.recv_msg_client(conn)
                if "action" not in header:
                    continue
                if header["action"] == "send":
                    self.send_msg_to_client(client_name, header["to"], data)
            except Exception:
                utils.pdbg(client_name,"disconnected!")
                utils.pexc()
                try:
                    conn.close()
                except Exception:
                    pass
                with self.clienttablelock:
                    try:
                        if self.clienttable[client_name]["conn"] == conn:
                            del self.clienttable[client_name]
                    except Exception:
                        pass
                return
                    
    def client_accept_handle(self, client):
        try:
            header, _ = self.recv_msg_client(client)
            if header["action"] != "subscribe":
                client.close()
                return
            name_pc = None

            if "name" in header:
                name_pc = header["name"]
            else:
                name_pc = str(uuid.uuid4())
            
            

            with self.clienttablelock:
                try:
                    if name_pc in self.clienttable:
                        self.clienttable[name_pc]["conn"].close()
                except Exception:
                    pass
                self.clienttable[name_pc] = {
                    "conn":client,
                    "lock":Lock(),
                    "checked":time.time(),
                    "thread": KThread(target=self.client_listener, args=(name_pc,))
                }
                self.clienttable[name_pc]["thread"].start()
            
            utils.pdbg(name_pc,"connected!")
            client.sendall(utils.msg_encode(
                    {
                        "action": "subscribe-status",
                        "name-assigned": name_pc,
                        "status": None
                    }
            ))
        except socket.timeout:
            pass
