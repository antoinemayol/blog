import random
import inspect

from myVM import MyVM

def readFile(filepath):
    """This function reads a file containing some code and returns it as a matrix.

    Args:
        filepath (string): path to the code file to read

    Returns:
        matrix: list of lines
    """
    matrix = []
    with open(filepath, 'r') as file:
        for line in file:
            matrix.append(line.strip().split())
    return matrix

def compileCode(IS, reverseIS, data):
    res = b''
    addrMacro = {}
    bytesCount = 0

    for line in data:
       for i in range(len(line)):
          if (line[0][0] == "."):
              addrMacro[line[0]] = bytesCount
          elif (line[i][0] == '#'):
              break
          else:
              bytesCount += 1

    for line in data:
        for i in range(len(line)):
            if i == 0 and line[0][0] == ".":
                pass

            elif (line[i][0] == "."):
                res += bytes([addrMacro[line[i]]])

            elif (line[i][0] == '#'):
                break

            elif i == 0 or (i == 1 and (line[0][0] == ".")):
                res += bytes([reverseIS[line[i]]])

            else:
                res += bytes([int(line[i])])

    return res

def getReverseIS(IS):
    """
      This gives a dict such as : { 'ADD':\x01, 'SUB': \x02, ...}
    """
    return {func.__name__[2:]: idx for idx, func in IS.items()}

def generateRandomIS(mnemonics):
    """
      This generate a dict sush as { myVm.opADD: \x01: myVm.opADD: \x02, ...}
    """
    values = random.sample(range(255), len(mnemonics)) # 255 is sizeof(char)

    IS = {}
    for i, nmemo in enumerate(mnemonics):
        IS[values[i]] = nmemo

    return IS


def printIS(IS):
    formated = "{\n" + ",\n".join(f"{k}: MyVM.{v.__name__}" for k, v in IS.items()) + "\n}"
    print(formated)

def copy_and_append(source_file, destination_file, bytecode):
    data = f"VM=MyVM({bytecode})"
    try:
        with open(source_file, 'r') as src:
            content = src.read()

        with open(destination_file, 'w+') as dest:
            dest.write(content)
            dest.write(data)

        print("File copied and text appended successfully!")
    except FileNotFoundError:
        print(f"Error: The file {source_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import sys
    bytecode_file = sys.argv[1]
    VM_file = sys.argv[2]
    VM_out_file = sys.argv[3]

    random.seed(1)

    mnemonics = [
        method for name, method in inspect.getmembers(MyVM, predicate=inspect.isfunction)
        if name.startswith("op")
    ]

    print(mnemonics)
    IS = generateRandomIS(mnemonics)
    print()
    print("You can now copy paste the following InstructionSet in your VM code.")
    printIS(IS)

    # Getting the map to know what is the value of an opcode
    ReverseInstructionSet = getReverseIS(IS)

    print()
    print("Reverse IS, gives the value of an opcode.")
    print(ReverseInstructionSet)

    # Reading the file
    print()
    print(f"Reading data from {bytecode_file}.")
    data = readFile(bytecode_file)

    # Getting the bytecode to give to the VM
    print()
    print("Creating bytecode.")

    print()
    print("You can now copy paste the follwing bytecode in your VM code.")
    res = compileCode(IS, ReverseInstructionSet, data)

    copy_and_append(VM_file, VM_out_file, res)
