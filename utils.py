def mask(ip):
    splt = ip.split('.')
    subnet = '.'.join(splt[0:3])
    return subnet


def check_ip(fn):
    def wrapper(*args, **kwargs):
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr