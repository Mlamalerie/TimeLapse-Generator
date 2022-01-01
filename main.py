import os
import datetime
import shutil
import time
import pyautogui
import cv2
import win32api

from param import SECRET_SCREENSHOTS_DIR_PATH,VIDEO_FPS,RESULTS_DIR_PATH

def CreerDossierSauvegarde(where, doss=None):
    nomEmplacementSauvegarde = where + "/" + doss if doss else where
    if not os.path.exists(nomEmplacementSauvegarde):
        os.mkdir(nomEmplacementSauvegarde)
        return nomEmplacementSauvegarde
    else:
        return nomEmplacementSauvegarde

# **** EMPLACEMENT SAUVEGARDE
SECRET_SCREENSHOTS_DIR_PATH = CreerDossierSauvegarde(SECRET_SCREENSHOTS_DIR_PATH)
# **** NOM SAUVEGARDE
CACHE_DIR = CreerDossierSauvegarde(SECRET_SCREENSHOTS_DIR_PATH, "cache_timelapse")
username = os.getlogin()

def run_screen(delay_sec,limit_time_hour = 24,compt_sec = 0):
    convert_sec_to_hour = lambda s : s/3600
    if convert_sec_to_hour(compt_sec) < limit_time_hour :
        #print("convert_sec_to_hour(compt_sec) ", convert_sec_to_hour(compt_sec))
        screen()
        time.sleep(delay_sec)
        run_screen(delay_sec,limit_time_hour,compt_sec + 1)
    else:
        print(f"... run_screen() stop, time is over ! ({convert_sec_to_hour(compt_sec)}h")

def screen():
    nomFichier = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S') + " " + username
    photo = CACHE_DIR + "/" + nomFichier + ".png"
    pyautogui.screenshot(photo)
    print("~ " + photo)

def remove(path):
    # removing the folder
    if os.path.isdir(path):
        if not shutil.rmtree(path):
            # success message
            print(f" * {path} is removed successfully !")
        else:
            # failure message
            print(f" * Unable to delete the {path}")


def create_timelapse(image_folder_path,params =  ""):
    images = sorted([img for img in os.listdir(image_folder_path) if img.endswith(".png")])

    if len(images) > 3:
        video_name = f'timelapse - {images[0].split(" ")[0]} - {images[-1].split(" ")[0]} [{params}].mp4'
        video_name = f"{RESULTS_DIR_PATH}/{video_name}"

        try:
            frame = cv2.imread(os.path.join(image_folder_path, images[0]))
            height, width, layers = frame.shape
            size = (width, height)
            video = cv2.VideoWriter(video_name, 0x7634706d, VIDEO_FPS, size)

            for image in images:
                video.write(cv2.imread(os.path.join(image_folder_path, image)))

            cv2.destroyAllWindows()
            video.release()
            print("~ video saved at",video_name)
        except:
            print("error in video creation...",e)
    else:
        print("not enough images...")

def on_exit(signal_type):
    print('caught signal:', str(signal_type))
    remove(CACHE_DIR)

def main():
    win32api.SetConsoleCtrlHandler(on_exit, True)

    TIME_MAX_HOUR = int(input(" * TIME MAX (HOUR) > "))
    SCREENSHOT_DELAY_SEC = int(input(" * SCREENSHOT DELAY (SEC) [5, 15, 30] > "))
    print(" * go screens")
    try:
        run_screen(SCREENSHOT_DELAY_SEC,TIME_MAX_HOUR)
    except:
        print(" * error * go screens")

    try:
        print(" * go create timelapse")
        create_timelapse(CACHE_DIR, params=f"({TIME_MAX_HOUR},{SCREENSHOT_DELAY_SEC}),{VIDEO_FPS}")
    except:
        print(" * error * go create timelapse")
    finally:
        time.sleep(1)
        remove(CACHE_DIR)
    print("\n bye bye :) ")
    time.sleep(5)

if __name__ == "__main__":
    main()



