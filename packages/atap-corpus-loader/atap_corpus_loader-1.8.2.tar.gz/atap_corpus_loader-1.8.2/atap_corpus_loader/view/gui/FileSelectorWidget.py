import sys
from fnmatch import fnmatch
from typing import Callable

import panel
from panel import Row, Column
from panel.pane import Markdown
from panel.widgets import Button, MultiSelect, TextInput, Select, Checkbox

from atap_corpus_loader.controller import Controller
from atap_corpus_loader.controller.data_objects import FileReference
from atap_corpus_loader.view import ViewWrapperWidget
from atap_corpus_loader.view.gui import AbstractWidget


class StdErrWrapper:
    def __init__(self):
        self.panel = Markdown(object="")
        self.last_msg = ""
        self.orig_stderr = sys.stderr

    def __enter__(self):
        sys.stderr = self

    def __exit__(self, exc_type, exc_value, traceback):
        self.clear()
        sys.stderr = self.orig_stderr

    def __panel__(self):
        return self.panel

    def write(self, std_msg):
        if '\r' in std_msg:
            self.panel.object = self.last_msg + str(std_msg) + '\n'
        else:
            self.last_msg = self.panel.object
            self.panel.object = self.panel.object + str(std_msg) + '\n'

    def clear(self):
        self.panel.object = ""
        self.last_msg = ""


class FileSelectorWidget(AbstractWidget):
    MAX_WIDTH: int = 1000

    @staticmethod
    def _get_short_path(long_path: str, threshold_len: int = 70):
        buffer_len: int = threshold_len // 2
        if len(long_path) < threshold_len:
            return long_path
        else:
            return f"{long_path[:buffer_len]}...{long_path[-buffer_len:]}"

    def __init__(self, view_handler: ViewWrapperWidget, controller: Controller):
        super().__init__()
        self.view_handler: ViewWrapperWidget = view_handler
        self.controller: Controller = controller
        # The function will be set by an instance method, but must be callable until then
        self._set_button_status_on_operation: Callable = lambda curr_loading: None

        self.select_all_button = Button(name="Select all", width=95,
                                        button_style="solid", button_type="primary")
        self.select_all_button.on_click(self.select_all)

        self.filter_input = TextInput(placeholder="Filter displayed files\t\t\t\N{DOWNWARDS ARROW WITH CORNER LEFTWARDS}",
                                      sizing_mode='stretch_width')
        self.filter_input.param.watch(self._on_filter_change, ['value'])
        filter_input_tooltip = self.view_handler.get_tooltip('file_filter_input')
        self.filter_row: Row = Row(self.filter_input, filter_input_tooltip)

        self.show_hidden_files_checkbox = Checkbox(name="Show hidden", value=False, align="start")
        self.show_hidden_files_checkbox.param.watch(self._on_filter_change, ['value'])

        self.expand_archive_checkbox = Checkbox(name="Expand archives", value=False, align="start")
        self.expand_archive_checkbox.param.watch(self._on_filter_change, ['value'])

        self.file_type_filter = Select(name='Filter by filetype', width=150)
        self.file_type_filter.options = ['All valid filetypes'] + self.controller.get_valid_filetypes()
        self.file_type_filter.value = self.file_type_filter.options[0]
        self.file_type_filter.param.watch(self._on_filter_change, ['value'])

        self.selector_widget = MultiSelect(size=10, sizing_mode='stretch_width')

        self.stderr_wrapper = StdErrWrapper()

        self.panel = Column(
            Row(Column(
                self.filter_row,
                self.select_all_button
            ),
                self.file_type_filter,
                Column(
                    self.show_hidden_files_checkbox,
                    self.expand_archive_checkbox
                )
            ),
            Row(self.selector_widget),
            self.stderr_wrapper,
            max_width=self.MAX_WIDTH
        )

        panel.state.add_periodic_callback(self.update_display, period=2000)
        self.update_display()

    def set_button_operation_fn(self, _set_button_status_on_operation: Callable):
        self._set_button_status_on_operation = _set_button_status_on_operation

    def update_display(self):
        loaded_corpus_files: set[FileReference] = self.controller.get_loaded_corpus_files()
        loaded_meta_files: set[FileReference] = self.controller.get_loaded_meta_files()

        filtered_refs: list[FileReference] = self._get_filtered_file_refs()

        filtered_files_dict: dict[str, str] = {}
        checkmark_symbol = "\U00002714"
        for ref in filtered_refs:
            file_repr = self._get_short_path(ref.get_path())
            if ref in loaded_corpus_files:
                file_repr += f" {checkmark_symbol} [corpus]"
            if ref in loaded_meta_files:
                file_repr += f" {checkmark_symbol} [meta]"
            filtered_files_dict[file_repr] = ref.get_path()

        self.selector_widget.options = filtered_files_dict

    def _get_filtered_file_refs(self) -> list[FileReference]:
        valid_file_types: list[str] = self.controller.get_valid_filetypes()
        selected_file_types: set[str]
        if self.file_type_filter.value in valid_file_types:
            selected_file_types = {self.file_type_filter.value.upper()}
        else:
            selected_file_types = {ft.upper() for ft in valid_file_types}

        expand_archived: bool = self.expand_archive_checkbox.value
        file_refs: list[FileReference] = self.controller.retrieve_all_files(expand_archived)

        filtered_refs: list[FileReference] = []
        filter_str = f"*{self.filter_input.value}*"
        skip_hidden: bool = not self.show_hidden_files_checkbox.value
        for ref in file_refs:
            if ref.get_extension().upper() not in selected_file_types:
                continue
            if not fnmatch(ref.get_path(), filter_str):
                continue
            if skip_hidden and ref.is_hidden():
                continue

            filtered_refs.append(ref)

        return filtered_refs

    def _on_filter_change(self, *_):
        self._set_button_status_on_operation(curr_loading=True)
        self.update_display()
        self._set_button_status_on_operation(curr_loading=False)
        self._check_for_download()

    def _check_for_download(self):
        filter_input: str = self.filter_input.value
        with self.stderr_wrapper:
            success = self.controller.check_for_download(filter_input)
        if success:
            self.filter_input.value = ""

    def select_all(self, *_):
        self._set_button_status_on_operation(curr_loading=True)
        self.selector_widget.value = list(self.selector_widget.options.values())
        self._set_button_status_on_operation(curr_loading=False)

    def get_selector_value(self) -> list[str]:
        return self.selector_widget.value

    def get_show_hidden_value(self) -> bool:
        return self.show_hidden_files_checkbox.value
