from urllib.parse import urlparse

def parse_proxy_url(proxy_url: str):
    """
    Parses a proxy URL and returns username, password, proxy address, and port.
    
    Example input:
    http://user123:pass456@192.168.1.10:8080
    
    Returns:
    ('user123', 'pass456', '192.168.1.10', 8080)
    """
    parsed = urlparse(proxy_url)
    
    if not all([parsed.hostname, parsed.port]):
        raise ValueError("Invalid proxy URL. Make sure it includes address and port.")
    
    return parsed.username, parsed.password, parsed.hostname, parsed.port