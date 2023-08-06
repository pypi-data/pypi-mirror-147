from __future__ import annotations
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import warnings

import cv2
from dataclasses_json import dataclass_json
from ruamel.yaml import YAML, round_trip_dump

try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata

__version__ = metadata.version("voltfpipe")


@dataclass_json
@dataclass
class RawVideo:
    path: str
    description: Optional[str] = None
    fps: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None


@dataclass_json
@dataclass
class RawVideoTransform:
    """ When converting a video to a images, what stats """
    description: Optional[str] = None
    nth_frame: int = 10  # extract every nth frame
    additional_frames: Optional[List[int]] = None   # extra frames to extract
    rotate: Optional[int] = None  # degrees
    resize: Optional[Tuple[int, int]] = None
    force_fps: Optional[float] = None  # re-render the video to the target fps before extracting
    start: Optional[float] = None  # in seconds
    end: Optional[float] = None  # in seconds


@dataclass_json
@dataclass
class VoltfPipe:
    name: str = "Untitled Project"
    slug: str = "untitled"
    version: Optional[str] = __version__
    raw_videos: Optional[Dict[str, RawVideo]] = field(default_factory=dict)
    video_transforms:  Optional[Dict[str, RawVideoTransform]] = field(default_factory=dict)
    num_of_raw_images: Optional[int] = 400  # when extracting, how many to allow
    num_of_align_images: Optional[int] = 200   # how many extract images to use in alignment

    @classmethod
    def load(cls, slug) -> VoltfPipe:
        """Load from yaml into class"""
        return load_project(slug)

    def save(self):
        """Save obj to yaml"""
        return save_project(
            self.slug,
            asdict(
                self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
            ),
        )

    def create(self):
        """Create a yaml for a project"""
        project_path = Path(self.slug)
        if not project_path.exists():
            project_path.mkdir()

        for i in ["images", "metashape"]:
            path = project_path / Path(i)
            if not path.exists():
                path.mkdir(exist_ok=True)

        if get_save_path(self.slug).exists():
            warnings.warn(f"Configuration file for {self.slug} already exists.")

        return self

    def parse_video(self, video_slug: str):
        """ Read the metadata from the file """
        video = self.raw_videos[video_slug]
        transform = self.video_transforms[video_slug]
        cap = cv2.VideoCapture(video.path)
        video.fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / video.fps
        transform.start = 0
        transform.end = duration % 60


def get_save_path(slug):
    return Path(Path(slug) / Path(slug)).with_suffix(".yaml")


def load_project(slug: str) -> VoltfPipe:
    """Load from yaml"""
    project_yaml_file = get_save_path(slug)
    with open(project_yaml_file) as file:
        yaml = YAML()
        project = yaml.load(file)
    return VoltfPipe.from_dict(project)


def save_project(slug: str, data: dict):
    """Save to yaml"""
    project_yaml_file = get_save_path(slug)
    with open(project_yaml_file, "w") as f:
        f.write(round_trip_dump(data, indent=2, block_seq_indent=2))
    return True
