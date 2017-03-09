
from flask import Flask, render_template, request
import json , pprint
basestation = Flask(__name__)  # creates object for web page
#global variables
xx =2
yy =15
targetinfo = {'target1': {'V2': None}, 'target2': {'R1': None, 'R2': None}, 'target3': {'R2': None, 'R3': None},
                  'target4': {'R1': None, 'R3': None}, 'target5': {'R1': None, 'C1': None, 'Freq': None},
                  'target6': {'R1': None, 'C1': None, 'Freq': None},
                  'target7': {'R1': None, 'C1': None, 'Freq': None}}

with open('arduino_data.txt', 'w') as outfile:
        json.dump(targetinfo, outfile)
arena = dict()
for y in range(0, 11):
    arena[y] = dict()
    for x in range(0, 15):
        arena[y][x] = "0"
with open('maze_layout.txt', 'w') as outfile:
    json.dump(arena, outfile)
#routing
@basestation.route('/')   # routes to home page
def website():

    return user_interface()

@basestation.route('/cmd')
def cmd():

    started = 0
    with open('started.txt', 'r') as f:
        started = int(f.readline())
        f.close()

    if started:
        return 'start'
    else:
        return 'none'
@basestation.route('/ARENA')
def arena_layout():
    with open('arduino_data.txt', 'r') as infile:
        arena = json.load(infile)
    return '0'

@basestation.route('/VICTORY')
def victory_roll():
    with open('victory_roll.txt', 'w') as f:
        f.write(str(1))
        f.close()
    return '0'
@basestation.route('/isvictorious')
def victory_roll_notifier():
    started = 0
    with open('victory_roll.txt', 'r') as f:
        started = int(f.readline())
        f.close()
    if started:
        return '1'
    else:
        return '0'

@basestation.route('/start')
def start():

    with open('started.txt', 'w') as f:
        f.write(str(1))
        f.close()

    return 'starting trial...'

@basestation.route('/stop')
def stop():

    with open('started.txt', 'w') as f:
        f.write(str(0))
        f.close()

    return 'resetting'

@basestation.route('/UPDATE')
def update():
    with open('maze_layout.txt', 'r') as infile:
        arena = json.load(infile)
    position = request.args.get('position')
    orientation = int(request.args.get('orientation'))
    xx = int(position[0]+ position[1])
    yy = int(position[2]+ position[3])
    if orientation == 0:
        if arena[str(yy)][str(xx)] == "2":
            arena[str(yy)][str(xx)] = "5"
        elif arena[str(yy)][str(xx)] == "5":
            arena[str(yy)][str(xx)] == "5"
        else:
            arena[str(yy)][str(xx)] = "1"
    elif orientation == 1:
        if arena[str(yy)][str(xx)] == "1":
            arena[str(yy)][str(xx)] = "5"
        elif arena[str(yy)][str(xx)] == "5":
            arena[str(yy)][str(xx)] == "5"
        else:
            arena[str(yy)][str(xx)] = "2"
    with open('maze_layout.txt', 'w') as outfile:
        json.dump(arena, outfile)
    return str(orientation)


@basestation.route('/ANALYSIS')
def analysis():


    with open('arduino_data.txt', 'r') as infile:
        targetinfo = json.load(infile)


    target = request.args.get('target')  # identifies target and analysis data to correct variable
    target = int(target)
    if target == 1:
        V2 = request.args.get('V2')
        targetinfo['target1']['V2']= str(V2)
    elif target == 2:
        R1 = request.args.get('R1')
        R2 = request.args.get('R2')
        targetinfo['target2']['R1'] = str(R1)
        targetinfo['target2']['R2'] = str(R2)
    elif target ==3:
        R3 = request.args.get('R3')
        R2 = request.args.get('R2')
        targetinfo['target3']['R3'] = str(R3)
        targetinfo['target3']['R2'] = str(R2)
    elif target == 4:
        R3 = request.args.get('R3')
        R1 = request.args.get('R1')
        targetinfo['target4']['R3'] = str(R3)
        targetinfo['target4']['R1'] = str(R1)
    elif target == 5 :
        R1 = request.args.get('R1')
        C1 = request.args.get('C1')
        FREQ = request.args.get('FREQ')
        targetinfo['target5']['R1'] = str(R1)
        targetinfo['target5']['C1'] = str(C1)
        targetinfo['target5']['Freq'] = str(FREQ)
    elif target == 6 :
        R1 = request.args.get('R1')
        C1 = request.args.get('C1')
        FREQ = request.args.get('FREQ')
        targetinfo['target6']['R1'] = str(R1)
        targetinfo['target6']['C1'] = str(C1)
        targetinfo['target6']['Freq'] = str(FREQ)
    elif target == 7 :
        R1 = request.args.get('R1')
        C1 = request.args.get('C1')
        FREQ = request.args.get('FREQ')
        targetinfo['target7']['R1'] = str(R1)
        targetinfo['target7']['C1'] = str(C1)
        targetinfo['target7']['Freq'] = str(FREQ)
    with open('arduino_data.txt', 'w') as outfile:
        json.dump(targetinfo, outfile)




    return '0'


@basestation.route('/')
def user_interface():
    temp_vars = {  # creates arena as a table of width 14 height 10
        'GRID_SIZE_X': 16,
        "GRID_SIZE_Y": 12
    }
    with open('arduino_data.txt', 'r') as infile:
        temp_vars['target_info']= json.load(infile)
    with open('maze_layout.txt', 'r') as infile:
        gridlayout = json.load(infile)
    return render_template("website.html", infoset=temp_vars,gridlayout=gridlayout) # runs website template written in html using temp vars dictionary as an argument for interrogated info


if __name__ == "__main__":  # checks if flask is running
    basestation.run(debug=True)
