#!/bin/sh
# Mac / Linux ke liye. Chalao: ./start.sh
cd "$(dirname "$0")" || exit 1
URL="http://127.0.0.1:5000"

port_up() { python3 -c "import socket,sys; s=socket.socket(); s.settimeout(0.5); sys.exit(0 if s.connect_ex(('127.0.0.1',5000))==0 else 1)"; }
open_browser() { (open "$URL" 2>/dev/null || xdg-open "$URL" 2>/dev/null || echo "Browser mein kholo: $URL") ; }

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 nahi mila. python.org se install karo."; exit 1
fi

if port_up; then open_browser; echo "Pehle se chal raha hai."; exit 0; fi

if [ ! -x .venv/bin/python ]; then
  echo "Pehli baar setup ho raha hai..."
  python3 -m venv .venv || { echo "venv nahi bana."; exit 1; }
fi
if [ ! -f .venv/installed.flag ]; then
  .venv/bin/python -m pip install -q -r requirements.txt || { echo "Flask install nahi hua. Internet check karo."; exit 1; }
  echo ok > .venv/installed.flag
fi

nohup .venv/bin/python app.py >/dev/null 2>&1 &
echo $! > .server.pid

i=0
while [ $i -lt 20 ]; do
  if port_up; then open_browser; echo "Chalu ho gaya. Band karne ke liye ./stop.sh"; exit 0; fi
  i=$((i+1)); sleep 1
done
echo "Server shuru nahi hua."; exit 1
