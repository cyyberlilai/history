#!/bin/zsh
# Circular Head · History Book — local preview
cd "$(dirname "$0")" || exit 1
PORT=8787
open "http://127.0.0.1:${PORT}/"
python3 -m http.server ${PORT} --bind 127.0.0.1
