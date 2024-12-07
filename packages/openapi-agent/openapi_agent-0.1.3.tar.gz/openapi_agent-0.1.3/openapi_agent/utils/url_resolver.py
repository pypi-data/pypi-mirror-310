from urllib.parse import urlparse

API_HOSTNAMES = {
    'GitHub': 'https://api.github.com',
}

def resolve_base_url(title: str, url: str) -> str:
    """Resolves parameterized base URLs for OpenAPI specifications.
    Some APIs (like GitHub) use variables in their base URL to support multiple deployments.
    For example: {protocol}://{hostname}/api/v3 needs to be converted to https://api.github.com
    
    Args:
        title: API title to determine the correct hostname
        url: Original URL with potential variables
    """
    
    # Try parsing as URL first
    try:
        result = urlparse(url)
        if result.scheme and result.netloc:
            return url
    except ValueError:
        pass
        
    for name, host in API_HOSTNAMES.items():
        if name in title:
            return host
        
    return url