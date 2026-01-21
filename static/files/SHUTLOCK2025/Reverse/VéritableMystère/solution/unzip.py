import re
import bz2
import base64
import sys

with open(sys.argv[1], 'r') as f:
    content = f.read()

p = r"base64\.b64decode\(\s*'([^']+)'\s*\)"
match = re.search(p, content)

b64_data = match.group(1)

decoded = base64.b64decode(b64_data)
decompressed = bz2.decompress(decoded)

print(decompressed.decode())
