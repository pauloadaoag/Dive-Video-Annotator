"""Overlay dive profile on a video

This script overlays a dive profile from a xml file onto a dive video

Usage:
    run.py [options]

Options:
    --xml-path=<arg>            Path to the xml file
    --video-source=<arg>        Path to the video file
    --output=<arg>              Destination file
    --timezone=<arg>            Timezone in diff from GMT
    --sec-offset=<arg>          Time in seconds that video is ahead of dive computer. Defaults to zero
    --diver-name=<arg>          Name of the diver
"""

from docopt import docopt
import xml.etree.ElementTree as ET
import os
from datetime import datetime, timedelta
import ffmpeg
from classes.annotator import Annotator
from classes.plot_generate import generate_plot_overlay
import dateutil.parser

tree = ET.parse('dive.xml')
root = tree.getroot()
dives = root.find('dives')
dive = dives.find('dive')
notes = dive.find('notes')

notes_text = notes.text

CHROMAKEY = '0x01ff07'

def format_time(seconds):
    secs = seconds % 60
    mins = seconds / 60
    return '%02d:%02d' % (mins, secs)

def parse_xml(xml_path, dive_date):
  tree = ET.parse(xml_path)
  root = tree.getroot()
  dives = root.find('dives')
  dive = dives.find('dive')
  dive_profile = []
  for sample in dive.iter('sample'):
    depth_sample = sample.get('depth')
    depth = float(depth_sample.split(' ')[0])
    dive_profile.append(depth)

  notes = dive.find('notes')
  dive_end = datetime.strptime(notes.text, "%H:%M:%S")
  dive_end = dive_end.replace(year=dive_date.year, month=dive_date.month, day=dive_date.day)
  dive_start = dive_end - timedelta(seconds=len(dive_profile))
  return {'dive_profile': dive_profile,
          'dive_start': dive_start}

def build_dive_string(depth, time):
    return 'Depth: {:.2f} meters\nTime: {}'.format(depth, format_time(time))


if __name__ == '__main__':
  arguments = docopt(__doc__)
  xml_path = arguments['--xml-path']
  video_source = arguments['--video-source']
  output = arguments['--output']
  sec_offset = arguments['--sec-offset']
  timezone = arguments['--timezone']
  diver_name = arguments['--diver-name']

  if not (xml_path and video_source and output and timezone):
    print(__doc__)
    exit()

  timezone = int(timezone)

  if not sec_offset:
    sec_offset = 0
  else:
    sec_offset = int(sec_offset)

  statbuf = os.stat(video_source)
  video_mod_time = datetime.utcfromtimestamp(statbuf.st_mtime)
  dive_date = video_mod_time.date()


  fontfile = '/Users/paoloadaoag/Documents/Personal/DiveVideoAnnotate/Play-Bold.ttf'
  probe = ffmpeg.probe(video_source)

  video_start = dateutil.parser.parse(probe['streams'][0]['tags']['creation_time'])

  dive_data = parse_xml(xml_path, video_start)
  dive_start = dive_data['dive_start']
  dive_start = dive_start.replace(tzinfo=None)
  video_start = video_start.replace(tzinfo=None)
  dive_start_adjusted = dive_start + timedelta(seconds=sec_offset)

  # dive_start = dive_start.replace(year=video_start.year, month=video_start.month, day=video_start.day)
  print "Dive_Start:%s"%(dive_start)
  print "Dive_Start Adsjusted:%s"%(dive_start_adjusted)

  print "Video Duration:%s"%(probe['streams'][0]['duration'])
  print "Video_Start:%s"%(video_start)

  difference = video_start - dive_start_adjusted


  start_offset = -1 * (difference.total_seconds())

  print "Start Offset: %s " %(start_offset)
  dive_profile = dive_data['dive_profile']

  annotator = Annotator(dive_profile, diver_name=diver_name)

  generate_plot_overlay(dive_profile)

  stream = ffmpeg.input(video_source, acodec='aac')
  audio = stream["a"].filter_("aecho", 0.8, 0.9, 1000, 0.3)
  stream2 = ffmpeg.input('lines.mov')

  stream2 = ffmpeg.setpts(stream2, 'PTS+%s/TB'%(start_offset-1))
  for i in xrange(0, len(dive_profile)):
    string = annotator.next()
    if (i+1) < len(dive_profile):
      enable_str = 'between(t,%s,%s)'%(i+start_offset, i+1+start_offset)
    else:
      enable_str = 'gte(t,%s)'%(i+start_offset)
    stream = ffmpeg.drawtext(stream,
      string,
      x=50, y=50,
      fontfile=fontfile, fontsize=70,
      escape_text=False,
      shadowcolor='Black',shadowx=3, shadowy=3,
      start_number=100,
      enable=enable_str, fontcolor='WhiteSmoke')
  stream = ffmpeg.overlay(stream, stream2, x=50, y=500, enable='gte(t,%s)'%(start_offset-1))
  stream = ffmpeg.output(stream, audio, output)
  stream = ffmpeg.overwrite_output(stream)
  ffmpeg.run(stream)
