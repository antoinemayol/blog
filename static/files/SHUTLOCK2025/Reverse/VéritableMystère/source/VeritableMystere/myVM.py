class MyVM:
  def __init__(self, bytecode):
    '''
    userInput needs to be null terminated
    '''
    self.bytecode = bytecode

    self.stack = []

    self.registers = [0] * 8
    self.flags = [0] * 8

    self.InstructionPointer = 0
    self.StackPointer = 0

    self.InstructionSet = {
34: MyVM.opADDREG,
145: MyVM.opADDVAL,
216: MyVM.opAND,
205: MyVM.opINPUT,
195: MyVM.opJMP,
16: MyVM.opJZ,
65: MyVM.opJZNTH,
30: MyVM.opLODSB,
126: MyVM.opMOVREG,
194: MyVM.opMOVVAL,
115: MyVM.opPOP,
120: MyVM.opPUSH,
166: MyVM.opRET,
97: MyVM.opSHR,
201: MyVM.opTEST,
53: MyVM.opXOR
}

    self.isRunning = False

    if not self.execBytecode():
      print("Mot de passe valide !")
    else:
      print("Mot de passe invalide !")

  def execBytecode(self):

    '''
    If this function return 1, there is an error or the password is wrong.
    The return code will be stored in the first register.
    '''
    self.isRunning = True
    while self.isRunning:
      try:
        opCode = self.eatBytecode()
      except:
        return 1
      if(self.parseOpcode(opCode)):
        return 1
      else:
        pass
    return self.getRegister(0)

  def parseOpcode(self, opCode):
    if self.InstructionSet[opCode] != None:
      self.InstructionSet[opCode](self)
    else:
      return 1
    return 0

  def getRegister(self, i):
    return self.registers[i]

  def setRegister(self, i, val):
    self.registers[i] = val

  def eatBytecode(self):
    res = self.bytecode[self.InstructionPointer]
    self.InstructionPointer += 1
    return res

  # Implementation of opcodes functions
  def opMOVVAL(self):
    regIndex = self.eatBytecode()
    val = self.eatBytecode()

    self.setRegister(regIndex, val)

  def opMOVREG(self):
    reg1Index = self.eatBytecode()
    reg2Index = self.eatBytecode()
    self.setRegister(reg1Index, self.getRegister(reg2Index))

  def opADDVAL(self):
    regIndex = self.eatBytecode()
    val = self.eatBytecode()

    self.setRegister(regIndex, self.getRegister(regIndex) + val)

  def opADDREG(self):
    reg1Index = self.eatBytecode()
    reg2Index = self.eatBytecode()

    self.setRegister(reg1Index, (self.getRegister(reg1Index) + self.getRegister(reg2Index)))

  def opRET(self):
    self.isRunning = False

  def opPUSH(self):
    regIndex = self.eatBytecode()
    self.stack.append(self.getRegister(regIndex))

  def opPOP(self):
    regIndex = self.eatBytecode()
    self.setRegister(regIndex, self.stack.pop() if self.stack else 0 )

  def opJMP(self):
    addr = self.eatBytecode()
    self.InstructionPointer = addr

  def opJZ(self):
    addr = self.eatBytecode()
    if (self.flags[0]) :
        self.InstructionPointer = addr

  def opJZNTH(self):
    nb = self.eatBytecode()
    if (self.flags[0]) :
      self.InstructionPointer += 1 + nb

  def opTEST(self):
    reg1Val = self.getRegister(self.eatBytecode())
    reg2Val = self.getRegister(self.eatBytecode())
    if reg1Val > reg2Val:
      self.flags[0] = 0
      self.flags[1] = 0
    elif reg1Val == reg2Val:
      self.flags[0] = 1
      self.flags[1] = 0
    else:
      self.flags[0] = 0
      self.flags[1] = 1

  def opXOR(self):
    reg1 = self.eatBytecode()
    xor_val = self.eatBytecode()

    self.setRegister(reg1, int(self.getRegister(reg1)) ^ xor_val)

  def opSHR(self):
    reg1 = self.eatBytecode()
    nb = self.eatBytecode()

    self.setRegister(reg1, self.getRegister(reg1) >> nb)

  def opAND(self):
    reg1 = self.eatBytecode()
    and_value = self.eatBytecode()
    self.setRegister(reg1, self.getRegister(reg1) & and_value)


  def opLODSB(self): # Get first char from string in register n° regIndex to first register
    destRegIndex = self.eatBytecode()
    sourceRegIndex = self.eatBytecode()
    if (len(self.getRegister(sourceRegIndex)) < 1): #If string empty still works just put 0
      self.setRegister(destRegIndex, 0)
    else:
      self.setRegister(destRegIndex, ord(self.getRegister(sourceRegIndex)[0]))
      self.setRegister(sourceRegIndex, self.getRegister(sourceRegIndex)[1:])

  def opINPUT(self):
    destRegIndex = self.eatBytecode()
    userInput = input()
    self.setRegister(destRegIndex, userInput)
