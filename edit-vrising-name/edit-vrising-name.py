#!/bin/env python3

import os, sys, glob, argparse
from bitstring import ConstBitStream
from colorama import Fore
from colorama import Style

def pair(arg):
    return [str(s) for s in arg.split(':')]

def pad(text, block_size):  
    pad_size = block_size - len(text) % block_size
    padded = text + chr(0)*pad_size
    return bytes(bytearray(padded, 'utf-8'))

def editCharacterName(bin_file, old, new):
  
  old_byte_data = pad(old, 20)
  new_byte_data = pad(new, 20)

  new_len = len(new)
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
    
    if old_len != len(old):
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
    parser.add_argument('rename_pairs', type=pair, nargs='+')
    args = parser.parse_args()

    if not os.path.exists(args.save_path):
      sys.exit(f'{Fore.RED}{args.save_path} does not exist!{Style.RESET_ALL}')

    filelist = glob.glob(args.save_path + '/SerializationJob_*.save')

    if not filelist:
      sys.exit(f'{Fore.RED}{args.save_path} does not contain any SerializationJob_*.save files to edit!{Style.RESET_ALL}')

    for old,new in args.rename_pairs:

      if (len(new) < 2 or len(old) < 2):
        print(f'  {Fore.YELLOW}{old}{Fore.GREEN} is {Fore.LIGHTCYAN_EX}{len(old)}{Fore.GREEN} characters{Style.RESET_ALL}')
        print(f'  {Fore.YELLOW}{new}{Fore.GREEN} is {Fore.LIGHTCYAN_EX}{len(new)}{Fore.GREEN} characters{Style.RESET_ALL}')
        print(f'{Fore.RED}Character names must be at least 2 characters. Skipping pair.{Style.RESET_ALL}')
        continue

      if (len(new) > 20 or len(old) > 20):
        print(f'  {Fore.YELLOW}{old}{Fore.GREEN} is {Fore.LIGHTCYAN_EX}{len(old)}{Fore.GREEN} characters{Style.RESET_ALL}')
        print(f'  {Fore.YELLOW}{new}{Fore.GREEN} is {Fore.LIGHTCYAN_EX}{len(new)}{Fore.GREEN} characters{Style.RESET_ALL}')
        print(f'{Fore.RED}Character names cannot exceed 20 characters. Skipping pair.{Style.RESET_ALL}')
        continue

      print(f'{Fore.GREEN}Changing name from {Fore.LIGHTCYAN_EX}{old} {Fore.GREEN}to {Fore.LIGHTCYAN_EX}{new}{Fore.GREEN} in save files.{Style.RESET_ALL}')
    
      for f in filelist:
        editCharacterName(f, old, new)
      
      print(f'{Fore.BLUE}======{Style.RESET_ALL}')