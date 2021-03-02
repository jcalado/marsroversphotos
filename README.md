# Mars Rover's photo downloader

## Start here

* This will use the official NASA API, so you will need a key from here: https://api.nasa.gov/
* You will need to create an api.py file with

```python
KEY = 'Your nasa provided api key goes here'
```

## Ok, so how do I use this?

`python photos.py` should be enough to get you today's perseverance photos if there are any.
You can (and should!) also try some arguments:

* Download photos from an Earth Date: `--date 2021-02-28`
* Download photos from Mars Sol: `--sol 1` for Sol 1, `--sol 1-10` for Sol 1 through 10
* Download only photos from a specific camera on the rover. Use `--camera MCZ_LEFT`. Check https://api.nasa.gov/ for an extensive list of possible strings, or check the section below.
* Output to another place than photos/: `--output path/to/output/dir`
* Defaults to Perseverance but you can target other rovers: `--rover curiosity`
* More! Use `--help` for all options.

## Rovers (--rover)
spirit  
opportunity   
curiosity  
perseverance  

## Perseverance cameras (--camera)

| Camera               | Description                           |
| -------------------- | ------------------------------------- |
| NAVCAM_LEFT          | Navigation Camera - Left              |
| NAVCAM_RIGHT         | Navigation Camera - Right             |
| MCZ_LEFT             | Mast Camera Zoom - Left               |
| MCZ_RIGHT            | Mast Camera Zoom - Right              |
| FRONT_HAZCAM_LEFT_A  | Front Hazard Avoidance Camera - Left  |
| FRONT_HAZCAM_RIGHT_A | Front Hazard Avoidance Camera - Right |
| REAR_HAZCAM_LEFT     | Rear Hazard Avoidance Camera - Left   |
| REAR_HAZCAM_RIGHT    | Rear Hazard Avoidance Camera - Right  |
| EDL_RDCAM            | Rover Down-Look Camera                |
| EDL_PUCAM1           | Parachute Up-Look Camera A            |
| EDL_PUCAM2           | Parachute Up-Look Camera B            |
