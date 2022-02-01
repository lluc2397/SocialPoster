import moviepy.editor as mymovie
import random
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import cv2
import os




def resize_image(image_full_path, final_path, top =0, bottom=0, delete_old = False):
    imagen_original = cv2.imread(image_full_path)

    imagen_recortada = imagen_original[top:-bottom]

    final_image_path = f'{final_path}resized-image.jpg'

    cv2.imwrite(final_image_path, imagen_recortada)

    if delete_old is True:
        os.remove(image_full_path)
        print('Image deleted')

    return final_image_path


def convert_pictures_to_video(new_dir,image, fps, duration, is_vertical=True):
    ''' this function converts images to videos'''

    frame_array=[]

    '''reading images'''
    img=cv2.imread(image)

    image = image.split('/')[-1]
    
    if is_vertical is True:
        img=cv2.resize(img,(1080,1920))
        video = f'{new_dir}/{image[:-4]}-vertical.mp4'
    else:
        video = f'{new_dir}/{image[:-4]}-horizontal.mp4'

    height, width, layers = img.shape
    size=(width,height)

    for k in range (duration):
        frame_array.append(img)

    out=cv2.VideoWriter(video,cv2.VideoWriter_fourcc(*'mp4v'), fps,size)
    
    for i in range(len(frame_array)):
        out.write(frame_array[i])
    out.release()

    return video



def joint_video_audio(audio_directory, videofile, final_directory, is_vertical=True):
    #generate audio file cut
    audiofile = random.choice(os.listdir(audio_directory))

    start_time = random.randint(0, 130)
    end_time = start_time + 20

    #get cut audio file
    final_audio = f'{final_directory}/cutmusic.mp3'
    if is_vertical is True:

        final_video = f'{final_directory}/vertical-final.mp4'
    else:
        final_video = f'{final_directory}/horizontal-final.mp4'
    #get original audio and cut it
    ffmpeg_extract_subclip(audio_directory+audiofile, start_time, end_time, targetname=final_audio)

    clip_video = mymovie.VideoFileClip(videofile)

    clip_audio_cortado = mymovie.AudioFileClip(final_audio)
    
    video_final_con_audio = clip_video.set_audio(clip_audio_cortado)
    #create the final video with the audio
    video_final_con_audio.write_videofile(final_video, codec="libx264", audio_codec="aac")

    return final_video


# def concat_videos(video):
#     vid = mymovie.VideoFileClip(video)
#     final_clip = vid.set_fps(23)
#     final_video = (video.replace("".join(video.split('/')[-1:]), 'morefps.mp4'))
#     final_clip.write_videofile(final_video)

#     return final_video


def create_img_from_frame(video):
    vidcap = cv2.VideoCapture(video)
    success,image = vidcap.read()
    final_image = (video.replace("".join(video.split('/')[-1:]), 'image.jpg'))
    count = 0
    while success:
        cv2.imwrite(final_image, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1
        if count == 1:
            break
    return final_image