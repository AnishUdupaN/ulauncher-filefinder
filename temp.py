import os
import subprocess
filename=""
foldername=""
result = subprocess.run(['fd', foldername], capture_output=True, text=True)
res = result.stdout.split('\n')
resfolders=[]
resfiles=[]
for line in res:
    if not os.path.isfile(line):
        resfolders.append(line)

for folder in resfolders:
    result = subprocess.run(['fd', filename, folder], capture_output=True, text=True)
    output = result.stdout.split('\n')
    resfiles.extend(output)


def on_event(self, event, extension):
    items = []
    stringinput = event.get_argument() or ""
    args = stringinput.strip().split(' in ')
    filename=args[0]
    if len(args)==1:
        search_path =os.path.expanduser("~")  #change if the user gives additional path
        result = subprocess.run(['fd', filename, search_path], capture_output=True, text=True)
        output = result.stdout
        lines = [line for line in output.split('\n') if line.strip()]
    else:
        search_path=args[1]
        result = subprocess.run(['fd', search_path], capture_output=True, text=True)
        res = result.stdout.split('\n')
        resfolders=[]
        lines=[]
        for line in res:
            if not os.path.isfile(line):
                resfolders.append(line)

        for folder in resfolders:
            result = subprocess.run(['fd', filename, folder], capture_output=True, text=True)
            output = result.stdout.split('\n')
            lines.extend(output)


    for i in range(len(lines)):
        items.append(ExtensionResultItem(
            icon=os.path.join(os.getcwd(),'images/icon.png'),
            name=lines[i],
            description="Click to Open",
            on_enter=RunScriptAction(f'xdg-open "{lines[i]}"', [])
        ))
    num_entries = int(extension.preferences.get('num_entries', 10))
    return RenderResultListAction(items[:num_entries])
