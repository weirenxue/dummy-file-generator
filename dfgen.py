import argparse
import os, sys, re, random, shutil

B  = 1
KB = 1024 * B
MB = 1024 * KB
GB = 1024 * MB
TB = 1024 * GB
UNIT = {}
for i in ['B', 'KB', 'MB', 'GB', 'TB']:
    UNIT[i] = locals()[i]
    
def checkSizeType(arg_value, pattern = re.compile(r'(\d+(B|KB|MB|GB|TB)|\d+)', re.IGNORECASE)):
    if not pattern.match(arg_value):
        raise argparse.ArgumentTypeError
    if arg_value.isdigit():
        return arg_value + 'B'
    return arg_value.upper()

def toByte(*args: str) -> int:
    ret = []
    for size in args:
        try:
            match = re.match(r"^(\d+)([a-zA-Z]+)$", size, re.I)
            if match:
                g = match.groups()
                ret.append(int(g[0]) * UNIT[g[1]])
            else:
                raise Exception()
        except:
            raise Exception(f'({size}) Size parsed error')
    return ret

def toReadableSize(size: int) -> str:
    ret = ''
    for key, value in sorted(UNIT.items(), key=lambda x:-x[1]):
        if size >= value:
            ret += '_' * (4 - len(str(size//value))) + f'{size//value} {key} '
            size = size % value
        else:
            ret += f'____ {key} '
    return ret

def generateDummy(destination, targetSize, minSize, maxSize, showProgress=True):
    accumulation = 0
    while accumulation < targetSize:
        with open(os.path.join(destination, str(accumulation)), 'wb') as outfile:
            dummySize = random.randint(minSize, maxSize)
            if accumulation + dummySize > targetSize:
                dummySize -= (accumulation + dummySize - targetSize)
                dummySize = max(minSize,dummySize)
            accumulation += dummySize
            outfile.write(os.urandom(dummySize))
            if showProgress:
                print(f'\r{accumulation/targetSize:3.2%} {toReadableSize(accumulation)}', end="")
            
def clearDirectory(path):
    for somethingName in os.listdir(path):
        somethingPath = os.path.join(destinationPath, somethingName)
        if os.path.isdir(somethingPath):
            shutil.rmtree(somethingPath)
        elif os.path.isfile(somethingPath):
            os.remove(somethingPath)
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('destination', help='Where are the dummy files stored to.')
    parser.add_argument('-t', '--target-size', help='The total size of target. ([B|KB|MB|GB|TB] default unit is Byte)', type=checkSizeType)
    parser.add_argument('--min-size', help='The minimim size of a dummy file. ([B|KB|MB|GB|TB] default unit is Byte)', type=checkSizeType)
    parser.add_argument('--max-size', help='The maximum size of a dummy file. ([B|KB|MB|GB|TB] default unit is Byte)', type=checkSizeType)
    parser.add_argument('-c', '--clear-first', help='Whether to clear the files in the destination directory first. (Default is false)', action='store_true')
    args = parser.parse_args()
    
    # convert size string to int in byte
    [targetSize, minSize, maxSize] = toByte(args.target_size, args.min_size, args.max_size)
    # if the user makes a mistake, the min and max valuse are automatically changed
    [minSize, maxSize] = [minSize, maxSize] if minSize < maxSize else [maxSize, minSize]
    clearFirst = args.clear_first
    
    # for convenient using, get absolute path.
    destinationPath = os.path.realpath(args.destination)
    # get available size of the disk
    if not os.path.exists(destinationPath):
        sys.exit(f'{destinationPath} doesn\'t exists!')
        
    [totalSize, usedSize, freeSize] = shutil.disk_usage(destinationPath)
    if freeSize < targetSize + maxSize:
        sys.exit(f'Free size is\t{toReadableSize(freeSize)} \nTarget size is\t{toReadableSize(targetSize)} \nNot enough space!')
        
    if not os.path.isdir(destinationPath):
        sys.exit(f'{destinationPath} is not a directory!')
    if clearFirst:
        clearDirectory(destinationPath)
    elif os.listdir(destinationPath):
        sys.exit(f'{destinationPath} is not an empty direcotry!')
    generateDummy(destinationPath, targetSize, minSize,maxSize)