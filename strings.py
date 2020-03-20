# regex patterms amd misc

regex_patterns = {
    'filename': r'(/*[^/]+(\.\w+)*)$',
    'link_pattern': r'https://*[^"\n \']+',
    'insta_media': r'https*://[^\?]+\.(jpg|mp4)[^ "]+',
    'link_filter': r'(\.(jpe*g|png|tiff*|gif|mp4|mov|flv))|images*|photos*|uploads*',
    'query': r'((\?|&).+)$',
    'filetype': r'\.[A-Za-z0-9]+',
    'type_id': r'\.(jpe*g|png|gif|mp4|web(p|m)|tiff*)',
    'tags': r'<[^>]+>',
    'filter': r'\.(js|css|pdf)|favicon',
    'insta_link': r'/p/[\w\-]+',
    'insta_crop': r'/(s|p)\d{3}x\d{3}/',
    'insta_username': r'(/*[^/]+/*)$'
}

format_patterns = [
    r'(-|_)*((\d+x(\d+)*|(\d+)*x\d+))',
    r'(-|_)*(large|big|thumb)(-|_)*',
    r'c_fill,f_auto,g_north,h_\d+,q_auto:best,w_\d+/v1/',
    r'expanded_[a-z]+/',
    r'w/\d+/',
    # r'(\.|-)\d+w',
    # NOTE: \-e\d+ catches some dashed filenames by mistake, consider changing
    # r'\-e\d+'
    r'/v/\d/.+\.webp$'
]

escape_to_ascii = {
    ' ': '%20',
    '%21': '!',
    '%22': '"',
    '%23': '#',
    '%24': '$',
    '%25': '%',
    '%26': '&',
    '%27': "'",
    '%28': '(',
    '%29': ')',
    '%2A': '*',
    '%2B': '+',
    '%2C': ',',
    '%2D': '-',
    '%2E': '.',
    '%2F': '/',
    '%3A': ':',
    '%3B': ';',
    '%3C': '<',
    '%3D': '=',
    '%3E': '>',
    '%3F': '?',
    '%40': '@',
    '%5B': '[',
    '%5C': '\\',
    '%5D': ']',
    '%5E': '^',
    '%5F': '_',
    '%60': '`',
    '%7B': '{',
    '%7C': '|',
    '%7D': '}',
    '%7E': '~',
    r'\u0021': '!',
    r'\u0022': '"',
    r'\u0023': '#',
    r'\u0024': '$',
    r'\u0025': '%',
    r'\u0026': '&',
    r'\u0027': "'",
    r'\u0028': '(',
    r'\u0029': ')',
    r'\u002A': '*',
    r'\u002B': '+',
    r'\u002C': ',',
    r'\u002D': '-',
    r'\u002E': '.',
    r'\u002F': '/',
    r'\u003A': ':',
    r'\u003B': ';',
    r'\u003C': '<',
    r'\u003D': '=',
    r'\u003E': '>',
    r'\u003F': '?',
    r'\u0040': '@',
    r'\u005B': '[',
    r'\u005C': '\\',
    r'\u005D': ']',
    r'\u005E': '^',
    r'\u005F': '_',
    r'\u0060': '`',
}
