import glob
from pathlib import Path
from HitObject import HitObject

dupCount = 1

for file in glob.glob("*.osu"):
    if 'duplicated' in file or 'keyBound' in file:
        continue
    with open(file, 'r', encoding='UTF8') as file_in:
        file_name = Path(file).stem
        with open(file_name + '_duplicated.osu', 'w', encoding='UTF8') as file_out:
            isHitObject = False
            isColour = False
            colourCount = 0
            isInitObj = True

            while True:
                line = file_in.readline()
                if not line:
                    break

                # Actions per sections
                if isHitObject:
                    origObj = HitObject(line)
                    frontObj = HitObject(line)
                    backObj = HitObject(line)

                    # Editor selects backObj first if they're overlapping
                    if origObj.newCombo or isInitObj:
                        isInitObj = False
                    else:
                        frontObj.colourSkip = colourCount

                    frontObj.newCombo = True
                    backObj.newCombo = False
                    backObj.objType = 'circle'

                    # Write to file
                    frontObj.write(file_out)  # Original object
                    for i in range(dupCount):
                        backObj.write(file_out)  # Cursor object(s)
                    continue

                elif isColour:
                    if 'Combo' in line:
                        colourCount += 1

                # simple line parsing
                segments = line.split(':')
                if 'Version' in segments:
                    version_string = segments[1][0:-1]
                    line = 'Version:' + version_string + '_duplicated' + '\n'
                # elif 'StackLeniency' in segments:
                #     line = 'StackLeniency: 0\n'

                # copy the line
                file_out.write(line)

                # next section detection
                if '[HitObjects]' in line:
                    isHitObject = True
                    if colourCount == 0:
                        colourCount = 4
                if '[Colours]' in line:
                    isColour = True
