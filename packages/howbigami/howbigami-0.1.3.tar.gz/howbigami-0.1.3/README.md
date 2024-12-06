# How big am I?

<h1>Treemap visualization of component sizes</h1>
It processes the data from stdin and visualizes them in form of a treemap of components.
The visualization happens via local Flask server and can be then accessed via browser
<br>The input data must be in a format of:

```text 
SIZE1 LABEL1
SIZE2 LABEL2
...
```
<h2>Example 1</h2>

```console
echo -e '10 Ten\n20 Twenty\n50 Fifty' | python3 howbigami.py
```
![](docs/example-1.png?raw=true)


<h2>Example 2</h2>
How big are different installed RPM packages on my Linux system?

```console
rpm -qa --queryformat='%{SIZE} %{NAME} %{VERSION}\n' | python3 howbigami.py
```
<h2>Example 3</h2>
How big are differents part of my Linux file system?

```console
df | tail -n +2 | awk '{bytes = $2*1024; printf "%d %s %s\n",bytes, $1, $6}' | python3 howbigami.py
```
<h2>Example 4</h2>
How big are different part of the Linux kernel?

```console
du -sb /lib/modules/$(uname -r)/kernel/* | sed -E 's/\/lib.*kernel\///g' | python3 howbigami/howbigami.py --no-other --fontsize=40
```

<h2>Help</h2>

```text
Usage: python3 howbigami.py [-h] [--no-others] [--fontsize [FONT_SIZE]] [--ref] [--no-flask]

Optional arguments:
  -h, --help            show this help message and exit
  --no-others           Do not show label for other category
  --fontsize [FONT_SIZE]
                        Font size for labels
  --ref                 Show also reference etalon size of 10Mb
  --no-flask            Do not start flask server. Just show the figure.

The input must be coming from stdin pipe.
```