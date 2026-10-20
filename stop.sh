#!/bin/sh
# Mac / Linux ke liye. Chalao: ./stop.sh
cd "$(dirname "$0")" || exit 1
if [ -f .server.pid ] && kill "$(cat .server.pid)" 2>/dev/null; then
  rm -f .server.pid
  echo "Jan Sahayak band ho gaya."
else
  rm -f .server.pid
  echo "Jan Sahayak chal hi nahi raha tha."
fi
