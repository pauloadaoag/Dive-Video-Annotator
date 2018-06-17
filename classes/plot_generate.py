import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

COLOR = 'xkcd:bright green'
FPS = 5


def generate_plot_overlay(dive_profile):
  fig1 = plt.figure()

  line = None
  annotation = None

  # Create the init function that returns the objects
  # that will change during the animation process
  def initialize():
      annotation.set_animated(True)
      return line, annotation

  def update_line(num, data, line, fig):
      if num > 0:
        annotation.set_text('-{:.1f}m'.format((data[..., :num][1][num-1])))
        annotation.set_position((data[..., :num][0][num-1], data[..., :num][1][num-1]  - 2))

      line.set_data(data[..., :num])
      line.set_color('white')
      return line, annotation



  # Expand dive profile to fill in the intermediate frames
  d2 = []
  init = 0.0
  for i in dive_profile:
    new_max = i
    diff = new_max - init
    diff = float(diff)
    for j in range(1,FPS+1):
      fig2 = ((float(j)/FPS) * diff) + float(init)
      d2.append(fig2)
    init = new_max

  data = np.random.rand(2, len(d2))
  data[1] = [-1 * e for e in d2]
  data[0] = xrange(0, len(d2))
  line, = plt.plot([], [], 'r-')
  plt.xlim(0, len(d2))
  plt.ylim((-1 * max(dive_profile)) - 5, 1)
  plt.setp(line, linewidth=4, color='r')
  # print len(d)


  ax = plt.gca()
  title = ax.set_title('Dive Profile', loc='left')
  plt.setp(title, color='#FFFFFF')
  ax.spines['bottom'].set_color('#FFFFFF')
  # ax.spines['top'].set_color('#dddddd')
  # ax.spines['right'].set_color('#FFFFFF')
  ax.spines['left'].set_color('#FFFFFF')
  ax.yaxis.label.set_color('#FFFFFF')
  ax.xaxis.label.set_color('#FFFFFF')
  ax.set_ylabel('Depth (m)')
  ax.tick_params(axis='y', colors='#FFFFFF')
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)


  plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off

  annotation = ax.annotate('Start', xy=(0,0))
  annotation.set_color('white')
  # print annotation
  # annotation.set_animated(True)

  # # ax.set_facecolor(COLOR)
  # ax.get_xaxis().set_visible(True)
  # ax.get_yaxis().set_visible(True)
  # ax.set_frame_on(True)
  # fig1.patch.set_alpha(0.0)

  # for child in ax.get_children():
  #     if isinstance(child, matplotlib.spines.Spine):
  #        child.set_color(COLOR)

  line_ani = animation.FuncAnimation(fig1, update_line, frames=len(d2), fargs=(data, line, fig1), interval=(1000/FPS), blit=True)
  line_ani.save('lines.mov',  codec='png', savefig_kwargs={'transparent': True, 'facecolor': 'none'})

