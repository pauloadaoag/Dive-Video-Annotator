import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

COLOR = 'xkcd:bright green'
FPS = 5
def update_line(num, data, line, fig):
    # print (data[..., :num])
    # print num
    line.set_data(data[..., :num])
    line.set_color('white')
    annotation = plt.annotate('A0', xy=(5,1))
    annotation.set_animated(True)
    return line,annotation

def generate_plot_overlay(dive_profile):
  fig1 = plt.figure()
  fig1.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
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
  l, = plt.plot([], [], 'r-')
  plt.xlim(0, len(d2))
  plt.ylim((-1 * max(dive_profile)) - 5, 1)
  plt.setp(l, linewidth=4)
  # print len(d)


  ax = plt.gca()
  # ax.set_facecolor(COLOR)
  ax.get_xaxis().set_visible(True)
  ax.get_yaxis().set_visible(True)
  ax.set_frame_on(False)
  fig1.patch.set_alpha(0.0)

  for child in ax.get_children():
      if isinstance(child, matplotlib.spines.Spine):
         child.set_color(COLOR)

  line_ani = animation.FuncAnimation(fig1, update_line, frames=len(d2), fargs=(data, l, fig1), interval=(1000/FPS), blit=True)
  line_ani.save('lines.mov',  codec='png', savefig_kwargs={'transparent': True, 'facecolor': 'none'})

