import glob
from pathlib import Path
from typing import Optional
from simple_term_menu import TerminalMenu
import subprocess

from pypsxlib import Project
import pypsxlib.utils
import typer
from slug import slug as slugify

from .core import (RawVideo, RawVideoTransform, VoltfPipe)

app = typer.Typer(
    help="A pipeline manager for a voltf project (photogrammetry and videogrammetry)",
)
videos_app = typer.Typer()
app.add_typer(videos_app, name="videos")
video_app = typer.Typer()
app.add_typer(video_app, name="video")
images_app = typer.Typer()
app.add_typer(images_app, name="images")


def cli_selector(slug: Optional[str] = None, options=None, title="Select"):
    """Select a single item"""
    slug = slug.lower() if slug else ""
    options = [] if not options else options

    if not slug:
        terminal_menu = TerminalMenu(options, title=title)
        menu_entry_index = terminal_menu.show()
        slug = options[menu_entry_index]

    return slug


def cli_video_selector(obj: VoltfPipe, slug: Optional[str] = None):
    """Find a video"""
    return cli_selector(slug, list(obj.raw_videos.keys()), "Select video")


@app.command()
def init(slug: Optional[str] = typer.Argument(None)):
    """Create a new pipeline"""
    if not slug:
        slug = input("project slug >")
    if not slug:
        return
    title = "My Project"
    if not title:
        title = input("project title >")

    proj = VoltfPipe(name=title, slug=slug)
    proj.create()
    proj.save()
    typer.echo(f"Created project {slug}.")


@video_app.command("add")
def video_add(path: str, video: str = typer.Option(None), project: str = typer.Option(...)):
    """Add a tool used to generate data in the pipeline"""

    if not video:
        video = slugify(Path(path).stem)

    proj = VoltfPipe.load(project)
    proj.raw_videos[video] = RawVideo(path)
    proj.save()
    typer.echo(f"Added video {video} to project {project}.")


@videos_app.command("add")
def videos_add(path: str, project: str = typer.Option(...)):
    """Add all the videos in a path to the project """

    proj = VoltfPipe.load(project)
    path = Path(path) / "*.mp4"
    print(path)
    for video_path in glob.glob(path.as_posix()):
        video = slugify(Path(video_path).stem)
        proj.raw_videos[video] = RawVideo(video_path)
        typer.echo(f"Added video {video_path} to project {project} as {video}.")
    proj.save()


@video_app.command("configure")
def video_configure(video: str = typer.Option(None), project: str = typer.Option(...)):
    """Configure a video"""

    obj = VoltfPipe.load(project)
    if not video:
        video = cli_video_selector(obj, video)

    if video not in obj.video_transforms:
        obj.video_transforms[video] = RawVideoTransform()

    transform = obj.video_transforms[video]
    nth = input(f"nth frame {transform.nth_frame} >")
    transform.nth_frame = int(nth) if nth else transform.nth_frame

    obj.save()
    typer.echo(f"Configured video {video} for project {project}.")


@videos_app.command("configure")
def videos_configure(project: str = typer.Option(...)):
    """Configure all videos basic, try and smart guess the nth frames to extract for each video
       to generate a maximum of 160 frames for the project
    """

    obj = VoltfPipe.load(project)
    num_of_videos = len(obj.raw_videos)
    total_allowed_frames = obj.num_of_raw_images

    total_duration = 0
    for video in obj.raw_videos.keys():
        if video not in obj.video_transforms:
            obj.video_transforms[video] = RawVideoTransform()
        obj.parse_video(video)
        total_duration += obj.video_transforms[video].end

    # eg if we have 100 seconds of footage and 50 allowed frames, then 1 frame every 2 seconds
    allowed_frames_per_second = total_allowed_frames / total_duration

    for video, transform in obj.video_transforms.items():
        video_percent_of_total = transform.end / total_duration
        transform.nth_frame = int(obj.raw_videos[video].fps // allowed_frames_per_second)

    print("total duration", total_duration)
    obj.save()
    typer.echo(f"Batch configured videos for project {project}.")


@images_app.command("create")
def images_create(project: str = typer.Option(...)):
    """process all raw videos"""

    obj = VoltfPipe.load(project)
    for video_slug, transform in obj.video_transforms.items():
        typer.echo(f"Extract images from video {video_slug}.")
        video = obj.raw_videos[video_slug]
        # "ffmpeg -i input.mp4 -r <framespersecond> output_%05d.png"
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video.path,
                "-r",
                str(video.fps / transform.nth_frame),
                Path(Path(obj.slug) / f"images/{video_slug}_%05d.png").as_posix()
            ]
        )

    typer.echo(f"Extract images for project {project}.")


@images_app.command("metashape")
def images_metashape(project: str = typer.Option(...)):
    """process all raw videos"""
    obj = VoltfPipe.load(project)
    path = Path(project) / "metashape" / project
    psx = Project(project, path.with_suffix(".psx").as_posix())
    psx.defaults()  # create a new app and document and chunk
    images = []
    path = Path(project) / "images/*.png"
    print(path)
    for image in glob.glob(path.as_posix()):
        images.append(image)

    nth_image = int(len(images) / obj.num_of_align_images)
    nth_image = 1 if nth_image < 1 else nth_image

    images = images[::nth_image]

    pypsxlib.utils.add_photos_to_chunk(psx, 0, images)
    psx.save()  # project.name and project.path must be set


if __name__ == "__main__":
    app()
