#!/bin/env python3

import os, sys, glob, argparse
from bitstring import ConstBitStream
from colorama import Fore
from colorama import Style

def pad(text, block_size):  
    pad_size = block_size - len(text) % block_size
    padded = text + chr(0)*pad_size
    return bytes(bytearray(padded, 'utf-8'))

def editCharacterName(bin_file, old_byte_data, new_byte_data):
  new_len = len(new_name)
  fileSizeBytes = os.path.getsize(bin_file)

  print(f'{Fore.GREEN}Searching{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{bin_file} {Fore.LIGHTBLUE_EX}{fileSizeBytes/float(1<<20):,.2f} MB{Fore.GREEN} ...{Style.RESET_ALL}')

  savefile = open(bin_file, 'r+b')
  s = ConstBitStream(savefile)
  occurrences = s.findall(old_byte_data, bytealigned=True)
  occurrences = list(occurrences)
  totaloccurrences = len(occurrences)

  print(f'{Fore.YELLOW}Found{Style.RESET_ALL} {Fore.GREEN}{totaloccurrences} {Fore.YELLOW}occurrence(s){Style.RESET_ALL}')

  for i in range(0, len(occurrences)):

    occurrenceOffset = (hex(int(occurrences[i]/8)))

    s.bitpos = occurrences[i]
    s.bytepos -= 2
    data = s.read('int:8')
    old_len = int(data)
    s.bitpos = occurrences[i]
    data = s.read('bytes:20')

    if data != old_byte_data:
      continue

    print(f'\t{Fore.BLUE}---{Style.RESET_ALL}') 
    print(f'\t{Fore.GREEN}Found {Fore.LIGHTCYAN_EX}{data} {Fore.GREEN}at {Fore.YELLOW}{occurrenceOffset} {Fore.WHITE}({Fore.LIGHTCYAN_EX}{int(old_len)}{Style.RESET_ALL})')
    print(f'\t{Fore.GREEN}Writing {Fore.LIGHTCYAN_EX}{new_byte_data} {Fore.GREEN}to {Fore.YELLOW}{occurrenceOffset} {Fore.WHITE}({Fore.LIGHTCYAN_EX}{int(new_len)}{Style.RESET_ALL})')

    savefile.seek(int(occurrences[i]/8), 0)
    print(f'\t{Fore.LIGHTCYAN_EX}** wrote new name at {Fore.YELLOW}{hex(int(savefile.tell()))}{Style.RESET_ALL}')
    savefile.write(new_byte_data)
    savefile.seek(int(occurrences[i]/8)-2, 0)
    print(f'\t{Fore.LIGHTCYAN_EX}** wrote new length at {Fore.YELLOW}{hex(int(savefile.tell()))}{Style.RESET_ALL}')
    savefile.write(bytes(chr(new_len), 'utf-8'))

  savefile.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("save_path", help='Path to AutoSave_? directory containing save files to edit')
    parser.add_argument('old_name', help='old name to replace')
    parser.add_argument('new_name', help='new name')
    args = parser.parse_args()

    old_name = args.old_name
    new_name = args.new_name

    old_byte_data = pad(old_name, 20)
    new_byte_data = pad(new_name, 20)

    if not os.path.exists(args.save_path):
      sys.exit(f'{Fore.RED}{args.save_path} does not exist!{Style.RESET_ALL}')
    if (len(new_name) > 20):
      sys.exit(f'{Fore.RED}Character names cannot exceed 20 characters{Style.RESET_ALL}')

    filelist = glob.glob(args.save_path + '/SerializationJob_*.save')

    if not filelist:
      sys.exit(f'{Fore.RED}{args.save_path} does not contain any SerializationJob_*.save files to edit!{Style.RESET_ALL}')

    print(f'{Fore.GREEN}Changing name from {Fore.LIGHTCYAN_EX}{old_name} {Fore.GREEN}to {Fore.LIGHTCYAN_EX}{new_name}{Fore.GREEN} in save files.{Style.RESET_ALL}')
    
    for f in filelist:
      editCharacterName(f, old_byte_data, new_byte_data)