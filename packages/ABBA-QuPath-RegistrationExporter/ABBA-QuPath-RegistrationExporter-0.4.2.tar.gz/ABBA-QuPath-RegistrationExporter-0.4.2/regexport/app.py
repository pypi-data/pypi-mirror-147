from PySide2.QtWidgets import QMainWindow

from regexport.actions.download_biop_extensions import SaveBiopExtensionsAction, SaveBiopExtensionsActionModel
from regexport.actions.load_atlas import LoadAtlasActionModel, LoadAtlasAction
from regexport.actions.load_cells import LoadCellsActionModel, LoadCellsAction
from regexport.actions.save_cells import SaveCellsActionModel, SaveCellsAction
from regexport.actions.save_script import SaveGroovyScriptActionModel, SaveGroovyScriptAction
from regexport.model import AppState
from regexport.utils.exceptions import show_dialog_box_on_uncaught_exception
from regexport.views.channel_filter import ChannelFilterView, ChannelFilterModel
from regexport.views.histogram import HistogramModel, HistogramView
from regexport.views.histogram2 import PlotView, PlotModel
from regexport.views.main_window import MainWindow
from regexport.views.plot_3d import PlotterModel, PlotterView
from regexport.views.region_tree import BrainRegionTreeModel, BrainRegionTree
from regexport.views.checkbox import CheckboxModel, CheckboxView
from regexport.views.sidebar import Layout
from regexport.views.text_selector import TextSelectorModel, DropdownTextSelectorView


class App:
    def __init__(self, debug=False):
        self.debug = debug
        self.model = AppState()

        self.plot_window = PlotterModel()
        self.plot_window.register(model=self.model)

        self.brain_region_tree = BrainRegionTreeModel()
        self.brain_region_tree.register(model=self.model)

        self.load_atlas_button = LoadAtlasActionModel()
        self.load_atlas_button.register(model=self.model)

        self.load_cells_button = LoadCellsActionModel()
        self.load_cells_button.register(model=self.model)

        self.export_data_button = SaveCellsActionModel()
        self.export_data_button.register(model=self.model)

        self.colormap_selector_model = TextSelectorModel()
        self.colormap_selector_model.register(model=self.model, options_attr='colormap_options',
                                              selected_attr='selected_colormap')

        self.colordata_selector_dropdown = TextSelectorModel()
        self.colordata_selector_dropdown.register(model=self.model, options_attr='column_to_plot_options',
                                                  selected_attr='column_to_plot')

        self.download_biop_extensions_button = SaveBiopExtensionsActionModel()
        self.save_groovy_script_button = SaveGroovyScriptActionModel()

        self.channel_filter_model = ChannelFilterModel()
        self.channel_filter_model.register(model=self.model)

        self.hist_plots = PlotModel()
        self.hist_plots.register(model=self.model)

        self.show_plots_checkbox = CheckboxModel(label='Auto-Update Histograms')
        self.show_plots_checkbox.register(model=self.model, model_property='show_plots')


    def create_gui(self) -> QMainWindow:
        if not self.debug:
            show_dialog_box_on_uncaught_exception()
        return MainWindow(
            main_widgets=(
                BrainRegionTree(model=self.brain_region_tree),
                PlotterView(model=self.plot_window),
                Layout(
                    widgets=(
                        DropdownTextSelectorView(model=self.colordata_selector_dropdown),
                        DropdownTextSelectorView(model=self.colormap_selector_model),
                        PlotView(model=self.hist_plots),
                        CheckboxView(model=self.show_plots_checkbox),
                        ChannelFilterView(model=self.channel_filter_model),
                    ),
                    horizontal=False,
                ),
            ),
            menu_actions=(
                SaveBiopExtensionsAction(model=self.download_biop_extensions_button),
                SaveGroovyScriptAction(model=self.save_groovy_script_button),
                LoadAtlasAction(model=self.load_atlas_button),
                LoadCellsAction(model=self.load_cells_button),
                SaveCellsAction(model=self.export_data_button),
            )
        )

    def set_max(self, channel_name, max_spots):
        ...
