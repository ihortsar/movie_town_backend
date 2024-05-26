import subprocess

'''converts loaded videos'''
def convert_480p(source): 
    target=source + '_480p.mp4'
    cmd = f'ffmpeg -i "{source}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    subprocess.run(cmd)