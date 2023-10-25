'''
Wattbot 2.0
Written by Elena D
25/10/2023
'''
## imports
from argparse import ArgumentParser


args = ArgumentParser('The commands to run the script')
args.add_argument(
  '-u', '--username', type=str, required=True,
  help='The username of the profile to scan'
)
args.add_argument(
  '-p', '--mongo_password', type=str, required=True,
  help='the password for the mongo database'
)

