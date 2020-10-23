class HitObject:
    objType = {'circle': 1<<0, 'slider': 1<<1, 'spinner': 1<<3, 'hold': 1<<7}
    invObjType = {v: k for k, v in objType.items()}

    def __init__(self, line):
        elements = line.split(',')
        for i in range(5):
            elements[i] = int(elements[i])

        self.x = elements[0]
        self.y = elements[1]
        self.time = elements[2]
        self.objType = HitObject.invObjType[elements[3] & 0b010001011]
        self.newCombo = bool(elements[3] & 0b00000100)
        self.colourSkip = ((elements[3] & 0b01110000) >> 4) + int(self.newCombo)
        self.hitSound = elements[4] & 0b00001111
        self.circleType = elements[4] >> 4
        self.params = ','.join(elements[5:])
        self.params = self.params.rstrip()

    def write(self, file):
        # sanitize the object
        if not self.newCombo or self.colourSkip == 0:  # sanitize colourSkip value
            self.colourSkip = 1
        if self.objType == 'circle':
            self.params = ''

        # encode
        type = HitObject.objType[self.objType] | int(self.newCombo)<<2 | (self.colourSkip-1)<<4
        hitSound = self.hitSound | self.circleType << 4

        # convert and write to file
        nums = [self.x, self.y, self.time, type, hitSound]
        nums = list(map(str, nums))
        if self.params == '':
            line = ','.join(nums) + '\n'
        else:
            line = ','.join(nums) + ',' + self.params + '\n'
        file.write(line)
