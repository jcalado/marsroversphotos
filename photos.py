from datetime import date
import api
import argparse
import multiprocessing
import os
import requests


parser = argparse.ArgumentParser(
    description='Download NASAs Mars rovers photos')

parser.add_argument('-r', '--rover', help="Rover", default='perseverance')
parser.add_argument('-c', '--camera', help="Camera")
parser.add_argument('-cs', '--cameras', action='store_true',
                    help="Print Possible cameras for use with --camera")
parser.add_argument('-s', '--sol', help="Mars Sol")
parser.add_argument('-d', '--date', help="Earth date (yyyy-m-d)")
parser.add_argument(
    '-p', '--page', help="Page number (splits every 25 photos)")
parser.add_argument('-o', '--output', default='photos', help="Output location")
args = parser.parse_args()

# CAMERAS
# NAVCAM_LEFT           Navigation Camera - Left
# NAVCAM_RIGHT          Navigation Camera - Right
# MCZ_LEFT              Mast Camera Zoom - Left
# MCZ_RIGHT             Mast Camera Zoom - Right
# FRONT_HAZCAM_LEFT_A   Front Hazard Avoidance Camera - Left
# FRONT_HAZCAM_RIGHT_A  Front Hazard Avoidance Camera - Right
# REAR_HAZCAM_LEFT      Rear Hazard Avoidance Camera - Left
# REAR_HAZCAM_RIGHT     Rear Hazard Avoidance Camera - Right
# EDL_RDCAM             Rover Down-Look Camera
# EDL_PUCAM1            Parachute Up-Look Camera A
# EDL_PUCAM2            Parachute Up-Look Camera B


photos_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos'.format(
    rover=args.rover)


if args.sol:
    sols = args.sol.split("-")


def solrange(start, end):
    if start > end:
        return range(end, start + 1)
    else:
        return range(start, end + 1)


def get_mars_photos_for_sol(sol, api_key=api.KEY):
    params = {'sol': sol, 'api_key': api_key}
    if "camera" in args:
        params["camera"] = args.camera

    download_photos_from_url(photos_url, params, sol)


def get_mars_photos_for_date(date, api_key=api.KEY):
    print("Getting photos for Earth date {date}".format(date=date))
    params = {'earth_date': args.date, 'api_key': api_key}

    download_photos_from_url(photos_url, params, args.date)


def download_photos_from_url(photos_url, params, query):
    response = requests.get(photos_url, params, stream=True)

    if response.status_code == 429:
        print("You have exceeded your rate limit. Try again later.")
        quit()

    response_dictionary = response.json()
    try:
        photos = response_dictionary['photos']
    except Exception as e:
        print(response.json())
        quit()

    dpath = r'%s/%s' % (args.output, query)

    if not os.path.exists(dpath):
        os.makedirs(dpath)

    urls = []
    for photo in photos:
        urls.append(photo['img_src'])
    if len(photos) == 0:
        print("No photos could be found. Check your arguments.")
        quit()

    for url in urls:
        p1 = multiprocessing.Process(target=fetch_url, args=(url, dpath,))
        p1.start()


def fetch_url(url, dpath):
    image = url.rsplit('/', 1)[1]
    path = os.path.join(dpath, image)

    if not os.path.exists(path):
        r = requests.get(url)
        print("Downloading photo: {path}".format(path=path))
        with open(path, 'wb') as f:
            f.write(r.content)
    else:
        print("Skipping {path} - file already exists".format(path=path))


def main():
    global sols

    if args.cameras:
        print(( "# This is a list of strings that you can feed to the --camera argument, followed by a short description.\n\n"
                "NAVCAM_LEFT           Navigation Camera - Left \n"
                "NAVCAM_RIGHT          Navigation Camera - Right \n"
                "MCZ_LEFT              Mast Camera Zoom - Left \n"
                "MCZ_RIGHT             Mast Camera Zoom - Right \n"
                "FRONT_HAZCAM_LEFT_A   Front Hazard Avoidance Camera - Left \n"
                "FRONT_HAZCAM_RIGHT_A  Front Hazard Avoidance Camera - Right \n"
                "REAR_HAZCAM_LEFT      Rear Hazard Avoidance Camera - Left \n"
                "REAR_HAZCAM_RIGHT     Rear Hazard Avoidance Camera - Right \n"
                "EDL_RDCAM             Rover Down-Look Camera \n"
                "EDL_PUCAM1            Parachute Up-Look Camera A \n"
                "EDL_PUCAM2            Parachute Up-Look Camera B \n"
                ))
        quit()

    if args.sol == None and args.date == None:
        print("No --date or --sol provided. Will fetch photos from today and output to photos/")
        args.output = './photos'
        today = date.today().strftime("%Y-%m-%d")
        print(today)
        get_mars_photos_for_date(today)

    if args.sol != None:
        if len(sols) == 1:
            print("Getting rover photo for SOL {sol}".format(sol=sols[0]))
            get_mars_photos_for_sol(sol=sols[0])
        else:
            sols = [int(i) for i in sols]
            for i in solrange(sols[0], sols[1]):
                print("Getting rover photos for SOL {sol}".format(sol=i+1))
                get_mars_photos_for_sol(sol=i)

    if args.date != None:
        get_mars_photos_for_date(args.date)


if __name__ == '__main__':
    main()
