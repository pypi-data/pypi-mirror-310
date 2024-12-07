import os
from pathlib import Path

from pydantic import BaseModel

from datamax.env import DATAMAX_HOME


class Config(BaseModel):
    datamax_home: Path


CONFIG = Config(
    datamax_home=Path(os.environ.get(DATAMAX_HOME, Path.home() / ".datamax")).resolve()
)
