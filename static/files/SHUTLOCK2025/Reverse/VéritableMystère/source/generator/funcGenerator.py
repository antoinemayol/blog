import os, sys

def ask_input(file=sys.stdout):
  template = """INPUT 1
MOVVAL 0 0"""
  print(template, file=file)

def xor_input(xor, file=sys.stdout):
  template = """LODSB 2 1
XOR 2 %i
PUSH 2
  """
  for c in xor:
    print(template % c, file=file)

def bit(xor, file=sys.stdout):
  template = """MOVREG 4 3
AND 4 1
MOVVAL 5 %i
TEST 4 5
JZNTH 2
MOVVAL 0 1
SHR 3 1
"""
  for i in range(0,8):  # From bit 7 to bit 0 (MSB to LSB)
    bit = (xor >> i) & 1
    print(template % bit, file=file)

def generate_assembly_cmp(flag, file=sys.stdout):
  template1 = """
POP 2
MOVREG 3 2
"""

  for c in flag:
    print(template1, file=file)
    bit(c, file=file)

def ret(file=sys.stdout):
  template = """LODSB 2 1
MOVVAL 1 0
TEST 2 1
JZNTH 2
MOVVAL 0 1
RET"""
  print(template, file=file)

if __name__ == "__main__":

  #flag = "cE5TUNVRa!My$7eRe3NPY7h0nEnPlUs!"
  flag = sys.argv[1]
  out_file = sys.argv[2]

  xor = os.urandom(len(flag))
  xored = bytes([b ^ k for b, k in zip(flag.encode(), xor)])
  with open(out_file, "w+") as f:
    ask_input(file=f)
    xor_input(xor,file=f)
    generate_assembly_cmp(xored[::-1],file=f)
    ret(file=f)
