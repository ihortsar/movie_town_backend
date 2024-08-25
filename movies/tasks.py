import subprocess
from django.conf import settings
import os

FFMPEG_PATH = "/usr/bin/ffmpeg"


def create_thumbnail(source_path, time="00:00:01", width=640, height=360):
    """
    Creates a thumbnail for a given video file.

    This function generates a thumbnail image from the specified video file at a given time,
    with specified width and height.

    Args:
    - source_path (str): The path to the source video file.
    - time (str, optional): The timestamp in the video from which to capture the thumbnail. Defaults to "00:00:05".
    - width (int, optional): The width of the thumbnail image. Defaults to 640.
    - height (int, optional): The height of the thumbnail image. Defaults to 360.

    Returns:
    - str: The path to the generated thumbnail image.
    """

    file_name = os.path.splitext(os.path.basename(source_path))[0]
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, "thumbnails")
    os.makedirs(thumbnail_dir, exist_ok=True)
    thumbnail_path = os.path.join(thumbnail_dir, f"{file_name}.jpg")

    cmd = '{} -y -i "{}" -ss {} -vframes 1 -vf "scale={}:{}" "{}"'.format(
        FFMPEG_PATH, source_path, time, width, height, thumbnail_path
    )
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg command failed with error: {result.stderr}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg error: {e.stderr}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e

    return thumbnail_path


def convert_720p(source_path):
    """
    Converts a video file to 720p resolution.

    This function converts the given video file to 720p resolution using FFmpeg.

    Args:
    - source_path (str): The path to the source video file.
    """
    print("converted 720")

    new_file_name = convert_path(source_path, "720p")
    cmd = '{} -y -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
        FFMPEG_PATH, source_path, new_file_name
    )
    subprocess.run(cmd, shell=True)


def convert_1080p(source_path):
    print("converted 1080")

    new_file_name = convert_path(source_path, "1080p")
    cmd = (
        '{} -y -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
            FFMPEG_PATH, source_path, new_file_name
        )
    )
    subprocess.run(cmd, shell=True)


def convert_480p(source_path):
    """
    Converts a video file to 480p resolution.

    This function converts the given video file to 480p resolution using FFmpeg.

    Args:
    - source_path (str): The path to the source video file.
    """

    new_file_name = convert_path(source_path, "480p")
    cmd = '{} -y -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
        FFMPEG_PATH, source_path, new_file_name
    )
    print("converted480")
    subprocess.run(cmd, shell=True)


def convert_path(source_path, resolution):
    """
    Generates a new file path with a resolution suffix.

    Args:
    - source_file (FieldFile or str): The path to the source file or a FieldFile object.
    - resolution (str): The resolution suffix to add to the new file name.

    Returns:
    - str: The new file path with the resolution suffix.
    """
    dot_index = source_path.rfind(".")
    base_name = source_path[:dot_index]
    ext = source_path[dot_index:]
    return f"{base_name}_{resolution}{ext}"
