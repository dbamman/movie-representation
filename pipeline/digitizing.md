# Digitizing

We use MakeMKV and Handbrake for extracting video files from DVDs from the command line.

## Install

Download and install [MakeMKV](https://www.makemkv.com) and [HandBrakeCLI](https://handbrake.fr/downloads2.php).


## Extract MKV files

* INPUTDISK is the input disk source (e.g., `dev:/dev/disk4`)
* OUTPUT_DIR is the folder you want extracted mkv files written to.

```
makemkvcon mkv $INPUTDISK all $OUTPUT_DIR --robot --progress=-stdout --messages=-stdout --debug --noscan --minlength=900 > $output_dir/out.log

```

## Convert MKV to MP4

* INPUTMKV is the mkv file to convert (e.g., `title00.mkv`)
* OUTPUTMP4 is the output file (e.g., `departed.mp4`)

```
/Applications/HandBrakeCLI -i "$INPUTMKV" -o $OUTPUTMP4 -e x264 -b 1200 --cfr --two-pass --turbo --subtitle none --audio-lang-list eng --first-audio
```