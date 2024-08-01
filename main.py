branch_inputs = ['BRA', 'BRP', 'BRZ']

# Comments
comment = "//"

def tokenize():
  code = []
  f = open("lmc.dat","r")
  line_num = 1
  # Syntax analysis
  for line in f:
    branch = False
    data = line.strip('\n')

    if data.split(' ')[0] in branch_inputs:
      if len(data.split(' ')) >= 3:
        print(f"Program HALTED due to unknown data on line {line_num}")
        return False

    if data.split(' ')[0] in commands or data.split(' ')[1] in commands:
      if data.split(' ')[0] not in required_inputs or data.split(' ')[1] not in required_inputs:
        if len(data.split(' ')) >= 4:
          print(f"Program HALTED due to unknown data on line {line_num}")
          return False
    
    if data.split(' ')[0] not in commands:
      # Checking for comments
      if data.startswith('//') == False:
        if data.split(' ')[1] not in commands:
          # If there is invalid data on a line.
          print(f"Program HALTED due to unknown data on line {line_num}")
          return False
        else:
          branch = True
    else:
      code.append(data) # If the data is correct

    if branch == True:
      code.append(data)
  f.close()
  return code

# Command actions

def INP():
  try:
    number = int(input(": "))
  except:
    return False
  else:
    if number > -999 and number < 999:
      return number
    else:
      return False

def OUT(acc_val):
  print(acc_val)

def ADD(acc_val, address):
  return acc_val + int(address)

def SUB(acc_val, address):
  return acc_val +- int(address)

def STA(acc_val, address, memory):
  memory[address] = acc_val
  return memory[address]

def BRA(address_loc):
  return address_loc

def BRP(acc_val):
  if acc_val > 0:
    return address_loc
  else:
    return False

def BRZ(acc_val):
  if acc_val == 0:
    return address_loc
  else:
    return False

# Assemble memory with the inscructions
def assemble_ram(memory):
  mnemonics = tokenize()
  if mnemonics != False:
    for x in range(len(mnemonics)):
     try:
       if mnemonics[x] == "HLT":
         memory[x] = '000'
       else:
        memory[x] = mnemonics[x]
     except:
       return False
    return memory
  return False

print(assemble_ram(memory_locations))

# Main
def main():
  memory = assemble_ram(memory_locations)
  # If the data is false then stop the code.
  if memory == False:
    print("Error.")
    return
  pc = -1
  acc_val = 0
  while pc < len(memory)-1:
    pc += 1
    data = memory[pc]
    x = 0
    if len(data.split(" ")) >= 2:
      for y in range(len(data.split(" "))):
        if data.split(" ")[y] in commands:
          x = y
    if data.split(" ")[x] in required_inputs:
      # If the data requires an input.
      data_list = data.split(' ')
      if len(data_list) < 1 and len(data_list) >= 4:
        # If the data isn't correct.
        print(f"Program HALTED due to unknown data on line {pc+1}")
        return

      # If the data is correct.
      opcode = data_list[y-1]
      try:
        operand = data_list[y]
      except:
        print(f"Program HALTED due to unknown data on load.")
        return

      # Commands
      if opcode == 'LDA':
        try:
          acc_val = int(memory[int(operand)])
        except:
          print(f"Program HALTED due to unknown data on load.")
          return

      if opcode == 'STA':
        try:
          memory[int(operand)] = int(acc_val)
        except:
          print(f"Program HALTED due to unknown data on load.")
          return

      if opcode == 'ADD':
        try:
          acc_val += memory[int(operand)]
        except:
          print(f"Program HALTED due to unknown data on load.")
          return
        else:
          if acc_val > 999 or acc_val < -999:
            print(f"Program HALTED due to number being too large.")
            return

      if opcode == 'SUB':
        try:
          acc_val -= memory[int(operand)]
        except:
          print(f"Program HALTED due to unknown data on load.")
          return
        else:
          if acc_val > 999 or acc_val < -999:
            print(f"Program HALTED due to number being too small.")
            return
    else:
      when_branch = False
      z = 0
      while z < len(data)-1:
        if len(data.split(' ')) >= 2 and data.split(' ')[z] in branch_inputs:
          try:
            when_branch = data.split(' ')[x]
            break
          except:
            print(f"Program HALTED due to unknown data on branch.")
            return
      data = data.split(' ')[x]
        
      # If the program does not require any instructions.

      # Stop the code if the code is at HTL
      if data == '000':
        print('Program HALT')
        return

      if data == 'INP':
        acc_val = INP()
        if acc_val == False and acc_val != 0:
          print(f"Program HALTED due to unknown data on input.")
          return
          
      if data in branch_inputs:
        branch = False
        if data == 'OUT':
          OUT(acc_val)
  
        if data == 'BRA':
          branch = True
  
        if data == 'BRP':
          if acc_val > -1:
            branch = True
  
        if data == 'BRZ':
          if acc_val == 0:
            branch = True
            
        if branch == True:
          if when_branch != False:
            z = 0
            branch_found = False
            while z < len(memory)-1:
              if memory[z].startswith(when_branch):
                pc = z-1
                branch_found = True
                break
            if branch_found == False:
              pc = -1
          else:
            pc = -1
main()
