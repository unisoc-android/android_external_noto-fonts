#!/usr/bin/env python

# Copyright (C) 2018 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
import os
import sys

from fontTools import ttLib

def read_cbdt(ttf):
  cbdt = ttf['CBDT']
  glyph_to_image = {}
  for strike_data in cbdt.strikeData:
    for key, data in strike_data.iteritems():
      data.decompile
      glyph_to_image[key] = data.imageData
  return glyph_to_image

def main(argv):
  with contextlib.closing(ttLib.TTFont(argv[1])) as ttf:
    font1_cbdt = read_cbdt(ttf)
  with contextlib.closing(ttLib.TTFont(argv[2])) as ttf:
    font2_cbdt = read_cbdt(ttf)

  glyphs1 = set(font1_cbdt.keys())
  glyphs2 = set(font2_cbdt.keys())
  if glyphs1 != glyphs2:
    print "Glyph set has changed: : %s" % (glyphs1 ^ glyphs2)

  for key in font1_cbdt.keys():
    image1 = font1_cbdt[key]
    image2 = font2_cbdt[key]

    if image1 != image2:
      print 'Glyph %s has different image' % key
      with open(os.path.join(argv[3], '%s_old.png' % key), 'w') as f:
        f.write(image1)
      with open(os.path.join(argv[3], '%s_new.png' % key), 'w') as f:
        f.write(image2)

if __name__ == '__main__':
  main(sys.argv)
