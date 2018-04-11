import os 
import time

QUERY_UP = "cat /proc/interrupts | grep 'Volume Up' | awk '{ print $2}'"

up = int(os.popen(QUERY_UP).read().strip('\n'))
diff_up = 0

def update():
  global up
  u = int(os.popen(QUERY_UP).read().strip('\n'))
  if up == u:
    reset()
  up = u

def reset():
  global diff_up
  if diff_up >= 10:
    print("WIN")
  diff_up = 0

while 42:
    print("UPDATE:", up)
    time.sleep(1)
    u = up
    update()
    diff_up = diff_up + up - u
