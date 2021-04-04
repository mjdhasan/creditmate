from init import DIR_VIDEOS
import pytube
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

if __name__ == '__main__':
    # download video
    url = 'https://www.youtube.com/watch?v=ayKGV_Lcbm0&ab_channel=Andr%C3%A9sVettori'
    youtube = pytube.YouTube(url)
    video = youtube.streams.get_highest_resolution()
    video.download('video')
    print(f'video title: {video.title}')

    # subset relevant part of the video
    files = os.listdir('./video')
    start_time = 38
    end_time = 154
    input_file = f"./video/{files[0]}"
    output_file = f"./video/{files[0]}_edited.mp4"
    video_example = VideoFileClip(input_file).subclip(start_time, end_time)
    video_example.write_videofile(output_file)
    video_example.audio

    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
    ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)

    # to remove audio from file, run the following shell script
    # for file in * .mp4; do ffmpeg -i "$file" -c copy -an "noaudio_$file"; done

    # schroders demo
    dir_vidoes_raw = os.path.join(DIR_VIDEOS, 'raw')
    dir_vidoes_edited = os.path.join(DIR_VIDEOS, 'edited')
    if not os.path.exists(dir_vidoes_edited):
        os.makedirs(dir_vidoes_edited)
    l_files = os.listdir(dir_vidoes_raw)
    l_files = [file for file in l_files if '.mov' in file]
    l_files.sort()
    i = 0
    for file in l_files:
        i = 8
        file = l_files[i]
        input_file = os.path.join(dir_vidoes_raw, file)
        output_file = os.path.join(dir_vidoes_edited, f"{file.replace('.mov', '')}_edited.mp4")
        if i == i:
            start_time = 1
            end_time = 100
        ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)

    # stitch videos together
    l_files = os.listdir(dir_vidoes_edited)
    l_files = [file for file in l_files if '.mp4' in file]
    l_files.sort()
    l_input_files = [os.path.join(dir_vidoes_edited, file) for file in l_files]
    # len(l_files)
    l_vidoes = []
    for file in l_files:
        input_file = os.path.join(dir_vidoes_edited, file)
        l_vidoes = l_vidoes + [VideoFileClip(input_file)]

    # concat list of videos into one
    final_video = concatenate_videoclips(l_vidoes, method='compose')
    # overwrite schroder's demo
    output_file = os.path.join(DIR_VIDEOS, f"demo_creditmate.mp4")
    final_video.write_videofile(output_file,
                                fps=l_vidoes[0].fps,
                                audio=True,
                                temp_audiofile='temp-audio.m4a',
                                remove_temp=True, codec="libx264", audio_codec="aac")
    # overwrite blackrock demo
    output_file = os.path.join(f"/Users/majid/Dropbox/startup/content/demo/docParser/blackrock/demo_blackrock.mp4")
    final_video.write_videofile(output_file,
                                fps=l_vidoes[0].fps,
                                audio=True,
                                temp_audiofile='temp-audio.m4a',
                                remove_temp=True,
                                codec="libx264",
                                audio_codec="aac")
    # overwrite schroders demo
    output_file = os.path.join(DIR_VIDEOS, f"/Users/majid/Dropbox/startup/content/demo/docParser/schroders/demo_schroders.mp4")
    final_video.write_videofile(output_file,
                                fps=l_vidoes[0].fps,
                                audio=True,
                                temp_audiofile='temp-audio.m4a',
                                remove_temp=True,
                                codec="libx264",
                                audio_codec="aac")


#     'ffmpeg -f concat -safe 0 -i video_concat.txt.txt -c copy mergedfile.mp4'
#
#     ffmpeg -i /Users/majid/Dropbox/startup/content/demo/docParser/edited/1_schroders_demo_01_edited.mp4 \
#            -i /Users/majid/Dropbox/startup/content/demo/docParser/edited/3_schroders_upload_0_edited.mp4 \
#            -i /Users/majid/Dropbox/startup/content/demo/docParser/edited/7_schriders_demo_03_edited.mp4 \
# -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]" \
# -map "[v]" -map "[a]" output.mp4
