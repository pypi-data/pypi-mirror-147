from pathlib import Path
from typing import List

import pandas as pd
from PySide2.QtWidgets import QFileDialog, QAction
from bg_atlasapi import BrainGlobeAtlas
from traitlets import HasTraits, Unicode, directional_link, Instance, Bool

from regexport.model import AppState
from regexport.utils.load_data import read_detection_files


class LoadCellsActionModel(HasTraits):
    text = Unicode("2. Load TSV Files")
    atlas = Instance(BrainGlobeAtlas, allow_none=True)
    cells = Instance(pd.DataFrame, allow_none=True)
    enabled = Bool(default_value=False)

    def register(self, model: AppState):
        directional_link((model, 'atlas'), (self, 'atlas'))
        directional_link((self, 'cells'), (model, 'cells'))
        directional_link((model, 'atlas'), (self, 'enabled'), lambda atlas: atlas is not None)

    def submit(self, filenames: List[Path]):
        if not filenames:
            return
        if self.atlas is None:
            raise ValueError("No atlas detected, cannot register brain regions")
        df = read_detection_files(filenames, atlas=self.atlas)
        self.cells = df


class LoadCellsAction(QAction):

    def __init__(self, model: LoadCellsActionModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText(self.model.text)

        self.triggered.connect(self.run)
        self.model.observe(self.set_enabled, 'enabled')
        self.set_enabled(None)
        
    def set_enabled(self, changed):
        print("setting enabled")
        self.setEnabled(self.model.enabled)

    def run(self):
        filenames, filetype = QFileDialog.getOpenFileNames(
            caption="Load Cell Points from File",
            filter="TSV Files (*.tsv)"
        )

        filenames = [Path(f) for f in filenames]
        self.model.submit(filenames=filenames)

