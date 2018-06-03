import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import matplotlib.patheffects as path_effects
import csv

FPS = 5
COLOR = 'xkcd:bright green'
DIVE_PROFILE = []


def format_time(seconds):
    secs = seconds % 60
    mins = seconds / 60
    return '%02d:%02d' % (mins, secs)

def initialize_plot():
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    # fig = plt.figure(figsize=(5, 5), dpi=50)

    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    return fig


def build_dive_string(FPS, i, dive_profile):
    d = i / FPS
    depth = dive_profile[d]
    seconds = i / FPS
    time_str = format_time(seconds)
    return 'Dive Time: %s seconds\nDepth: %sm' % (time_str, depth)


def update_plot(figure, plot,i):
    plot.clf()
    ax = plt.gca()
    ax.spines['bottom'].set_color(COLOR)
    ax.spines['top'].set_color(COLOR)
    ax.spines['right'].set_color(COLOR)
    ax.spines['left'].set_color(COLOR)
    ax.set_facecolor(COLOR)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    text = fig.text(0.1, 0.1, build_dive_string(FPS, i, DIVE_PROFILE), color='white', ha='left', va='bottom', size=15)
    text.set_path_effects([path_effects.PathPatchEffect(edgecolor='white', linewidth=1.1, facecolor='white')])


def build_movie(fig):
    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Movie Test', artist='Matplotlib', comment='Movie support!')
    writer = FFMpegWriter(fps=FPS, metadata=metadata)
    frame_count =  FPS * len(DIVE_PROFILE)

    # plt.savefig('myfig_1.png', facecolor='xkcd:sky blue', bbox_inches='tight', pad_inches=0)
    with writer.saving(fig, "/Users/paoloadaoag/Desktop/dive2/haze_clean.mp4", 100):
        for i in range(frame_count):
            update_plot(fig, plt, i)
            writer.grab_frame(savefig_kwargs={'facecolor':'xkcd:sky blue', 'bbox_inches':'tight', 'pad_inches':0})


def import_dive_profile(filename, header):
    dive_profile = []
    with open(filename, 'rb') as csvfile:
        divereader = csv.DictReader(csvfile, delimiter=',')
        for row in divereader:
            dive_profile.append(row[header])
    return dive_profile

if __name__ == "__main__":
    # filename = 'dive.csv'
    filename = '/Users/paoloadaoag/Desktop/dive2/haze_clean.csv'
    DIVE_PROFILE = import_dive_profile(filename, 'sample depth (m)')
    # DIVE_PROFILE = [0,0] + DIVE_PROFILE
    # print DIVE_PROFILE
    # DIVE_PROFILE = [1,2,3]
    fig = initialize_plot()
    build_movie(fig)
