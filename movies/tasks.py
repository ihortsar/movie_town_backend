import subprocess

def convert_480p(source):
    target = f"{source}_480p.mp4"
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd480',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        target
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while converting video: {e}")
