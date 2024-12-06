def get_media_type(key: str) -> str:
    if key.endswith('.jpg'):
        return 'image/jpeg'
    elif key.endswith('.png'):
        return 'image/png'
    elif key.endswith('.txt'):
        return 'text/plain'
    else:
        return 'application/octet-stream'
