class Annotator(object):

  diver_name = None
  dive_profile = None
  i = 0
  max_depth = 0

  def __init__(self, profile, diver_name=None):
    if profile is None:
      raise "Dive profile must exist"
    self.dive_profile = profile
    self.i = 1
    self.diver_name = diver_name

  def __iter__(self):
      return self


  def __get_time_str(self):
    secs = self.i % 60
    mins = self.i / 60
    return '%02d:%02d' % (mins, secs)

  def __build_string(self):
    depth = self.dive_profile[self.i - 1]
    time_str = self.__get_time_str()
    string = ''
    if self.diver_name:
      string = 'Diver: {}\n'.format(self.diver_name)
    if depth > self.max_depth:
      self.max_depth = depth
    string = string + 'Time: {}\nDepth: {:.1f}meters\nMax Depth: {:.1f}'.format(time_str, depth,  self.max_depth)
    return string

  def next(self):
    if self.i > len(self.dive_profile):
      raise StopIteration()
    else:
      string = self.__build_string()
      self.i += 1
      return string
