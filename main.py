import os
import datetime
import shutil
import time
import pyautogui
import cv2
from plyer import notification

from param import SECRET_SCREENSHOTS_DIR_PATH, VIDEO_FPS, RESULTS_DIR_PATH


def CreerDossierSauvegarde(where, doss=None):
    nomEmplacementSauvegarde = f"{where}/{doss}" if doss else where
    if not os.path.exists(nomEmplacementSauvegarde):
        os.mkdir(nomEmplacementSauvegarde)
    return nomEmplacementSauvegarde


# **** EMPLACEMENT SAUVEGARDE
SECRET_SCREENSHOTS_DIR_PATH = CreerDossierSauvegarde(SECRET_SCREENSHOTS_DIR_PATH)
# **** NOM SAUVEGARDE
CACHE_DIR = CreerDossierSauvegarde(SECRET_SCREENSHOTS_DIR_PATH, "cache_timelapse")
username = os.getlogin()

def convert_sec_to_hour(s):
    return s / 3600

def run_screen(delay_sec, limit_time_hour=24, compt_sec=0):

    if convert_sec_to_hour(compt_sec) < limit_time_hour:
        # print("convert_sec_to_hour(compt_sec) ", convert_sec_to_hour(compt_sec))
        screen()
        time.sleep(delay_sec)
        run_screen(delay_sec, limit_time_hour, compt_sec + 1)
    else:
        print("... run_screen() stop, time is over !")
        return convert_sec_to_hour(compt_sec)


def screen():
    nomFichier = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S') + " " + username
    photo = f"{CACHE_DIR}/{nomFichier}.png"
    pyautogui.screenshot(photo)
    print(f"~ {photo}")


def remove(path):
    # removing the folder
    if os.path.isdir(path):
        if not shutil.rmtree(path):
            # success message
            print(f" * {path} is removed successfully !")
        else:
            # failure message
            print(f" * Unable to delete the {path}")

def notify(title="...", message="...."):
    image = f"{os.getcwd()}/img/time-lapse.ico"
    print(image)
    notification.notify(title=title, message=message, timeout=10, app_icon=image)

def create_timelapse(image_folder_path, params="",nb_test_rest = 3):
    images = sorted([img for img in os.listdir(image_folder_path) if img.endswith(".png")])

    if nb_test_rest > 0:
        if len(images) > 3:
            video_name = f'timelapse - {images[0].split(" ")[0]} [{params}].mp4'
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
            except:
                print("error in video creation...")
                print("let's try again ...")
                time.sleep(5)
                create_timelapse(image_folder_path, params, nb_test_rest-1)
            else:
                print("~ video saved at", video_name)
                notify("Timelapse video saved at", f"-> {video_name}")
                remove(CACHE_DIR)
        else:
            print("not enough images...")
    else:
        print("not enough nb try...")

def main():
    TIME_MAX_HOUR = int(input(" * TIME MAX (HOUR) > "))
    #TIME_MAX_HOUR = 0.01
    SCREENSHOT_DELAY_SEC = int(input(" * SCREENSHOT DELAY (SEC) [10, 15, 30] > "))
    #SCREENSHOT_DELAY_SEC = 1
    notify("Timelapse #screenshots in progress", f"{TIME_MAX_HOUR} hour remaining")
    start_time = time.time()
    try:
        print(" * run_screen()")
        run_screen(SCREENSHOT_DELAY_SEC, TIME_MAX_HOUR)
    except:
        print(" * error * go screens")
    finally:
        end_time_hour = convert_sec_to_hour((time.time() - start_time))
        notify("Timelapse #screenshots finish", f"{round(end_time_hour,1)}h time ...")
        create_timelapse(CACHE_DIR, params=f"duration={round(end_time_hour,1)}, max_hour={TIME_MAX_HOUR}, screens_delay={SCREENSHOT_DELAY_SEC}")
        print("\n bye bye :) ")
        time.sleep(10)


if __name__ == "__main__":
    main()
