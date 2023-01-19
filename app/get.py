from urllib.request import urlopen


def my_ip():
    ip_service = 'https://icanhazip.com'
    ip = urlopen(ip_service, )
    return ip.read().decode('utf-8')
