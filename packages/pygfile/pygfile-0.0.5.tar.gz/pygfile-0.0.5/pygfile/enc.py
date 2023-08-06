import pickle
import base64
import struct
import os
import socket

class NotBytesTypeError(Exception):
    pass
def dump(filename,string,stripln=True,enc_nums=1):
    #代码有个好处，可以伪装
    data = []
    file_info = struct.pack("128sl",filename.encode(),len(string) if stripln==False else len(string.strip("\n")))
    data.append(file_info)
    s = base64.b85encode(string.encode())
    data.append(s)

    loginname = os.getlogin()
    loginname = base64.a85encode(loginname.encode())
    data.append(loginname)

    ip = socket.gethostbyname(socket.gethostname())
    ip = base64.b16encode(ip.encode())
    data.append(ip)
    
    enc_over = data
    for x in range(enc_nums):
        enc_over = pickle.dumps(enc_over)
    return enc_over
def load(data,enc_nums=1):
    if type(data) != bytes:
        raise NotBytesTypeError()
    r = data
    for x in range(enc_nums):
        r = pickle.loads(r)
    file_info = struct.unpack("128sl",r[0])
    s = base64.b85decode(r[1])
    filename = file_info[0]
    filename = filename.decode()
    filename = filename.strip("\x00")
    s = s.decode()
    loginname = r[2]
    loginname = base64.a85decode(loginname).decode()
    ip = r[3]
    ip = base64.b16decode(ip).decode()
    return [filename,file_info[1],s,loginname,ip]
