#!/bin/env python3

import gzip
import shutil
import os, sys, glob, argparse
from bitstring import ConstBitStream
from colorama import Fore
from colorama import Style

def pair(arg):
  return [str(s) for s in arg.split(':')]

def pad(text, block_size):  
  pad_size = block_size - len(text.encode('utf-8')) % block_size
  padded = text + chr(0)*pad_size
  return bytes(bytearray(padded, 'utf-8'))

def m_gunzip(file):
  with gzip.open(file, 'rb') as f_in:
    with open(file[:-3], 'wb') as f_out:
      shutil.copyfileobj(f_in, f_out)
  os.remove(file)

def m_gzip(file):
  with open(file, 'rb') as f_in:
    with gzip.open(file + '.gz', 'wb') as f_out:
      shutil.copyfileobj(f_in, f_out)
  os.remove(file)

def is_gzip(file):
  with open(file, 'rb') as f:
    return f.read(2) == b'\x1f\x8b'

def m_unzip(file):
  if is_gzip(file):
    print(f'{Fore.GREEN}Unzipping {Fore.LIGHTCYAN_EX}{file}{Fore.GREEN}...{Style.RESET_ALL}')
    m_gunzip(file)
    return file[:-3]
  else:
    return file

def editCharacterName(bin_file, old, new):
  
  old_byte_data = pad(old, 20)
  new_byte_data = pad(new, 20)

  old_n = old.encode('utf-8')
  new_n = new.encode('utf-8')

  new_len = len(new_n)  
  s_file = m_unzip(bin_file)

  fileSizeBytes = os.path.getsize(s_file)

  print(f'{Fore.GREEN}Searching{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{s_file} {Fore.LIGHTBLUE_EX}{fileSizeBytes/float(1<<20):,.2f} MB{Fore.GREEN} ...{Style.RESET_ALL}')

  savefile = open(s_file, 'r+b')
  s = ConstBitStream(savefile)
  occurrences = s.findall(old_byte_data, bytealigned=True)
  occurrences = list(occurrences)
  totaloccurrences = len(occurrences)

  print(f'{Fore.YELLOW}Found{Style.RESET_ALL} {Fore.GREEN}{totaloccurrences} {Fore.YELLOW}occurrence(s){Style.RESET_ALL}')
  
  if totaloccurrences == 0:
    print(f'{Fore.RED}No occurrences found for {Fore.LIGHTCYAN_EX}{old}{Fore.RED}. Skipping.{Style.RESET_ALL}')
    return

  for i in range(0, len(occurrences)):

    occurrenceOffset = (hex(int(occurrences[i]/8)))

    s.bitpos = occurrences[i]
    s.bytepos -= 2
    data = s.read('int:8')
    old_len = int(data)
    s.bitpos = occurrences[i]
    data = s.read('bytes:20')

    if data != old_byte_data:
      if args.verbose:
        print(f'\t{Fore.RED}Skipping old name mismatch{Style.RESET_ALL}')
        print(f'\t- {Fore.RED}Entered: {Fore.LIGHTCYAN_EX}{old_byte_data}{Style.RESET_ALL}')
        print(f'\t- {Fore.RED}Found: {Fore.LIGHTCYAN_EX}{data}{Style.RESET_ALL}')
      continue
    
    if old_len != len(old_n):
      if args.verbose:
        print(f'\t{Fore.RED}Skipipng old name length mismatch | Entered: {Fore.LIGHTCYAN_EX}{len(old_n)} {Fore.RED}Found: {Fore.LIGHTCYAN_EX}{old_len}{Style.RESET_ALL}')
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

  print(f'{Fore.GREEN}Gzipping new save file{Style.RESET_ALL}')
  m_gzip(s_file)
  print(f'{Fore.GREEN}Wrote new save file to {Fore.LIGHTCYAN_EX}{s_file}.gz{Fore.GREEN}.{Style.RESET_ALL}')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Edit character names within V Rising save files')
    parser.add_argument("save_path", help='Path to directory containing save files to edit')
    parser.add_argument("-f", dest='save_file', nargs='?', action='store', help='Path to specific file to edit')
    parser.add_argument('rename_pair', type=pair, nargs='+', help='Pair of old and new name in the form of old_name:new_name')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='More verbose output with debug information')
    args = parser.parse_args()

    if not os.path.exists(args.save_path):
      sys.exit(f'{Fore.RED}{args.save_path} does not exist!{Style.RESET_ALL}')

    if args.save_file:
      if not os.path.isfile(args.save_file):
          sys.exit(f'{Fore.RED}{args.save_file} does not exist in {args.save_path}!{Style.RESET_ALL}')
      filelist = glob.glob(args.save_path + '/' + args.save_file)
    else: 
      filelist = glob.glob(args.save_path + '/AutoSave_*.save.gz')
      if not filelist:
        filelist = glob.glob(args.save_path + '/AutoSave_*.save')

    if not filelist:
      sys.exit(f'{Fore.RED}{args.save_path} does not contain any AutoSave_*.save.gz or AutoSave_*.save files to edit!{Style.RESET_ALL}')

    for old,new in args.rename_pair:

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
