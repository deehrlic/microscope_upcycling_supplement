import subprocess
import yaml, time
from datetime import datetime


def ticcmd(*args):
  return subprocess.check_output(['ticcmd'] + list(args))

def upbyx(x, mid):
    status = yaml.load(ticcmd('-s', '--full', '-d', mid), Loader=yaml.Loader)
    
    position = status['Current position']
    print("Current position is {}.".format(position))
    
    new_target = position+x
    print("Setting target position to {}.".format(new_target))
    ticcmd('--exit-safe-start', '--position', str(new_target), '-d', mid)
def downbyx(x, mid):
    status = yaml.load(ticcmd('-s', '--full', '-d', mid), Loader=yaml.Loader)
 
    position = status['Current position']
    print("Current position is {}.".format(position))
    
    new_target = position-x
    print("Setting target position to {}.".format(new_target))
    ticcmd('--exit-safe-start', '--position', str(new_target), '-d', mid)

def deenergize(mid):
    print("Deenergizing")
    ticcmd('--deenergize', '-d', mid)

def energize(mid):
    print("Energizing")
    ticcmd('--energize', '-d', mid)

motor1 = "00426475"
motor2 = "00381236"

energize(motor2)
upbyx(200,motor2)
time.sleep(5)
deenergize(motor2)
