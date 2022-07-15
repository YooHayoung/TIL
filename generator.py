import os

os.chdir(os.getcwd())

rootPath = os.getcwd()
level = 0
fileCount = 0

f = open(rootPath + '/' + "README.md", 'w')

def readFolder(path, level, prevDir):
    pathRoot = prevDir
    dirName = path.split('/').pop()
    # print(pathRoot)
    if level == 1:
        f.write('### [***' + dirName + '***]' + '(' + dirName + ')' + '\n\n')
    elif level > 1:
        prefixk = ''
        for i in range(1, level):
            prefixk = prefixk + '  '
        f.write(prefixk + '- [***' + dirName + '***]' + '(' + prevDir + '/' + dirName + ')' + '\n\n')
    listdir = sorted(os.listdir(path))
    dir_list = [dir for dir in listdir if not dir.__contains__('.')]
    for idx, dir in enumerate(dir_list):
        if dir == 'venv':
            continue
        readFolder(path + '/' + dir, level + 1, pathRoot+"/"+dir)
    file_list = [file for file in listdir if file.endswith('.md')]
    for idx, file in enumerate(file_list):
        if file == 'README.md':
            continue
        prefix = '  '
        for i in range(1, level):
            prefix = prefix + '  '
        f.write(prefix + '- [' + file.replace('.md', '').replace('-', ' ').replace('_', ' ') + ']' + '(' + pathRoot + '/' + file + ')\n')
    if idx == len(file_list) - 1:
        f.write('\n')

def countTILs(path):
    count = 0
    listdir = sorted(os.listdir(path))
    # print(path)
    dir_list = [dir for dir in listdir if not dir.__contains__('.')]
    for idx, dir in enumerate(dir_list):
        if dir == 'venv':
            continue
        # print(path + '/' + dir)
        count += countTILs(path + '/' + dir)

    file_list = [file for file in listdir if file.endswith('.md')]
    for idx, file in enumerate(file_list):
        if file == 'README.md':
            continue
        count += 1
    return count


if __name__ == '__main__':
    f.write('''# TIL\n> Today I Learned\n\nYoo Hayoung's [TIL collection](https://github.com/YooHayoung/TIL).\n\n''')
    count = countTILs(os.getcwd())
    f.write(f'''*{count} TILs and counting...*\n\n---\n\n\n''')

    readFolder(os.getcwd(), 0, '')
    f.close()

