#!/usr/bin/env python

import sys, os
from yaml import load, dump
import argparse
import re
import string
import pudb

class PageGen(object):
  def __init__(self, template):
    if os.path.exists(template):
      with open(template, 'r') as file:
        self.terms = load(file.read())
    self.re_token = re.compile('\$\{([a-zA-Z0-9_]*)\}')

  def __call__(self, format_file, file):
    # update terms with format_file dict
    self.terms.update(format_file)
    # find terms within the html file
    matches = self.re_token.finditer(file)
    for match in matches:
      token = match.group(1)
      variable = match.group(0)
      if token in self.terms:
        # process token to recover full string replacement
        replace_str = self.ProcessString(self.terms[token])
        file = string.replace(file, variable, replace_str)
    return file
  def ProcessString(self, raw_string, parent_scope=None):
    scope = None
    # Construct full raw string defined terms
    if not raw_string:
      return ""
    # check if string is dictionary
    if type(raw_string) == dict:
      scope = raw_string
      raw_string = raw_string['OUTPUT']

    matches = self.re_token.finditer(raw_string)
    if matches:
      for match in matches:
        token = match.group(1)
        variable = match.group(0)
        if scope and token in scope:
          replace_str = self.ProcessString(scope[token], scope)
        elif parent_scope and token in parent_scope:
          replace_str = self.ProcessString(parent_scope[token], scope)
        elif token in self.terms:
          replace_str = self.ProcessString(self.terms[token], scope)
        else:
          raise ValueError('No term matched token!')
        # pudb.set_trace()
        raw_string = string.replace(raw_string, variable, replace_str)
    return raw_string

def main():
  parser = argparse.ArgumentParser(prog='HTML Page Generation Program')
  parser.add_argument('-f', '--format', type=str, help='Input format file')
  parser.add_argument('-t', '--html', type=str, help='Input html   file')

  args = parser.parse_args()
  html_format = None
  format_file = None

  if args.html and os.path.exists(args.html):
    with open(args.html, 'r') as file:
      html_format = file.read()
  if args.format and os.path.exists(args.format):
    with open(args.format, 'r') as file:
      format_file = load(file.read())

  if html_format and format_file:
    # Call PageGen to replace tokens with html strings
    page_gen = PageGen('template.yaml')
    with open(args.html[1:], 'w') as output:
      generated_file = page_gen(format_file, html_format)
      output.write(generated_file)
    print 'File Generated'

if __name__ == '__main__':
  main()
