##!/usr/bin/env python3
"""
How big am I?
Treemap visualization of component sizes
It processes the data from stdin and visualizes them in form of a treemap of components.
The visualization happens via local Flask server and can be then accessed via browser.

The input data must be in a format of: 
SIZE1 LABEL1
SIZE2 LABEL2
...

For example:
10 Ten
20 Twenty
50 Fifty

Example usage:
    echo -e '10 Ten\n20 Twenty\n50 Fifty' | python3 howbigami.py
    rpm -qa --queryformat='%{SIZE} %{NAME} %{VERSION}\n' | sort -n -r | python3 howbigami.py
    df | tail -n +2 | awk '{bytes = $2*1024; printf "%d %s %s\n",bytes, $1, $6}' | python3 howbigami.py

For help:
    python3 howbigami.py --help
"""

import sys, os
import re

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import squarify
import seaborn as sb 
import base64
from io import BytesIO

from flask import Flask, render_template
app = Flask(__name__)

import argparse

def error(exitcode, msg):
    print(f'Error: {msg}')
    sys.exit(os.EX_NOINPUT)


def process_stdin():
    volumes=[]
    labels=[]
    if not sys.stdin.isatty():
        ptrn = re.compile(r"""		    
            (?P<size>\d+)\s+
            (?P<name>.+)
            """, re.VERBOSE)
        for line in sys.stdin:
            match = ptrn.match(line)
            if match is not None:
                volume = int(match.group("size"))
                print(volume)
                volumes.append(volume)
                label = match.group("name")
                label = label.replace(' ', '\n')
                print(label)
                labels.append(label)
        volumes, labels = zip(*sorted(zip(volumes, labels)))
        volumes = list(volumes)
        volumes.reverse()
        labels = list(labels)
        labels.reverse()
    else:
        error(os.EX_NOINPUT, "Please provide the input data via pipe!" )
    return volumes, labels

def plot(volumes, labels, n, file_format, options):
    # Remove zero items
    new_volumes = []
    new_labels = []
    for idx, x in enumerate(volumes):
        if x > 0:
            new_volumes.append(volumes[idx])
            new_labels.append(labels[idx])
    volumes = new_volumes
    labels = new_labels
    # Filter first N items
    if len(volumes) > n:
        othern = len(volumes[n:])
        othersum = int(sum(volumes[n:]))
        volumes = volumes[0:n]
        labels = labels[0:n]
        volumes.append(othersum)
        if options.b_others:
            labels.append(f'other\n({othern} items)')
        else:
            labels.append('')
    
    if options.b_ref:
        # Add 10Mb reference
        volumes.append(int(10485760))
        labels.append('10Mb')
    # Plot
    [fig, ax] = plt.subplots(figsize=(16.00, 9.00))
    color_list = sb.color_palette("Spectral_r" , len(volumes)-1)
    color_list.append('darkgray')
    squarify.plot(sizes=volumes, label=labels, color=color_list, pad=0,
                  text_kwargs={'color': 'black','fontweight': 'normal', 'fontsize': options.font_size})
    plt.axis("off")
    if file_format is None: 
        plt.show()
        plt.close('all')
        return None
    else:
        buffer = BytesIO();
        fig.savefig(buffer, format=file_format, bbox_inches='tight', pad_inches=0)
        data = base64.b64encode(buffer.getbuffer()).decode("ascii")
        plt.close('all')
        return f"<img src='data:image/png;base64,{data}'/>"
        
# ----- RESTFUL API FUNCTIONS -----
@app.route('/')
@app.route('/index.html')
def index():
    app.volumes, app.labels = zip(*sorted(zip(app.volumes, app.labels)))  
    app.volumes = list(app.volumes)
    app.volumes.reverse()
    app.labels = list(app.labels)
    app.labels.reverse()
    return index_filtered(40)

@app.route('/byname/<item_name>')
def index_filtered_by_name(item_name):
    tmp_volumes_1 = []
    tmp_volumes_2 = []
    tmp_labels_1 = []
    tmp_labels_2 = []
    n = 0
    for volume, label in zip(app.volumes, app.labels):
        if item_name in label:
            tmp_volumes_1.append(volume)
            tmp_labels_1.append(label)
            n += 1
        else:
            tmp_volumes_2.append(volume)
            tmp_labels_2.append(label)
    app.volumes = tmp_volumes_1 + tmp_volumes_2
    app.labels = tmp_labels_1 + tmp_labels_2
    if n == 0: n = 40
    return index_filtered(n)

@app.route('/filter/<n_items>')
def index_filtered(n_items):
    n_items = min(len(app.volumes),int(n_items))
    app.squarify_image = plot(app.volumes, app.labels, n_items, 'png', app.args)
    r_classes = ['black']*(n_items)
    for i in range(0, len(app.volumes)-n_items):
        r_classes.append('darkgray')
    items_list = zip(app.labels, app.volumes, r_classes)
    filtered_size = [
        sum(app.volumes[0:n_items]), 
        round(sum(app.volumes[0:n_items])*100 / app.total_size)
    ]

    return render_template("index.html", 
                squarify_image=app.squarify_image, 
                items_list=items_list,
                total_size=app.total_size,
                n_items = n_items,
                filtered_size = filtered_size
                )


def start_flask(volumes, labels):
    app.volumes = volumes
    app.labels = labels
    app.total_size = sum(volumes)
    app.run(debug=False, host='0.0.0.0', port=8080)

# ----- MAIN -----
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-others', dest='b_others', action='store_false', help='Do not show label for other category')
    parser.add_argument('--fontsize', dest='font_size', nargs='?', type=int, help='Font size for labels')
    parser.add_argument('--ref', dest='b_ref', action='store_true', help='Show also reference etalon size of 10Mb')
    parser.add_argument('--no-flask', dest='b_flask', action='store_false', help='Do not start flask server. Just show the figure.')
    parser.set_defaults(
            b_others = True, 
            b_ref = False, 
            font_size = 8,
            b_flask = True)
    app.args = parser.parse_args()
    volumes, labels = process_stdin()
    if app.args.b_flask:
        start_flask(volumes, labels) 
    else:
        plot(volumes, labels, 40, None, app.args)
    sys.exit(os.EX_OK)
