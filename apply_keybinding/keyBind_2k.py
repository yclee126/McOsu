import glob
from pathlib import Path
from HitObject import HitObject

versionInfo = '1.0'

for file in glob.glob("*.osu"):
    if 'duplicated' in file or 'keyBound' in file:
        continue
    with open(file, 'r', encoding='UTF8') as file_ref:
        file_name = Path(file).stem
        try:
            with open(file_name[0:-1] + '_duplicated].osu', 'r', encoding='UTF8') as file_in:
                with open(file_name + '_keyBound.osu', 'w', encoding='UTF8') as file_out:
                    print(file_name, "- Processing")

                    print('A', end='')
                    # key binding
                    # X-  -X
                    # XX  --
                    key_binding = ((1, 3), (2, 0))

                    # Skip the upper sections (ref)
                    isHitObject = False
                    while not isHitObject:
                        line = file_ref.readline()
                        segments = line.split(':')
                        if 'Version' in segments:
                            version_string = segments[1][0:-1]
                            version_string = version_string.split('_')
                            line = 'Version:' + version_string[0] + ' +2k_v' + versionInfo + '\n'
                        file_out.write(line)
                        if '[HitObjects]' in line:
                            isHitObject = True

                    # Skip the upper sections (in)
                    isHitObject = False
                    while not isHitObject:
                        line = file_in.readline()
                        if '[HitObjects]' in line:
                            isHitObject = True

                    # Copy from ref but bind the key
                    while True:
                        line = file_in.readline()
                        if not line:
                            break

                        frontObj = HitObject(line)
                        backObj = HitObject(file_in.readline())
                        refObj = HitObject(file_ref.readline())

                        x0, y0 = frontObj.x, frontObj.y
                        x1, y1 = backObj.x, backObj.y

                        if x0-x1 > 0:
                            x = 0
                        else:
                            x = 1
                        if y0-y1 > 0:
                            y = 0
                        else:
                            y = 1

                        refObj.circleType = key_binding[x][y]
                        refObj.write(file_out)

                        # unicodeMap = ('\u0484', '\u0485', '\u0486', '\u0487')
                        unicodeMap = (0x0315, 0x031b, 0x0321, 0x0322, 0x0327, 0x0328, 0x0334, 0x0335, 0x0336, 0x0337, 0x0338, 0x035c, 0x035d, 0x035e, 0x035f, 0x0360, 0x0361, 0x0362)
                        print(chr(unicodeMap[refObj.circleType]), end='')
            print('\nCompleted')

        except FileNotFoundError:
            print(file_name, "- passed")