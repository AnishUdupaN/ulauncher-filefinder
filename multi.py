import subprocess
import os
def command(filename,search_path):
    if search_path=="anywhere":
        result = subprocess.run(['fd', filename, '/'], capture_output=True, text=True)
        output = result.stdout.split('\n')
        return output
    result = subprocess.run(['fd', search_path,'/'], capture_output=True, text=True)
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

    flag=True
    while flag:
        if '' in lines:
            lines.remove('')
        else:
            flag=False
    return lines

if __name__=="__main__":
    stringinput =input("Enter the string : ")
    args = stringinput.strip().split(' in ')
    filename=args[0]
    search_path=args[1]
    lines=command(filename,search_path)
    for i in lines:
        print(i)
