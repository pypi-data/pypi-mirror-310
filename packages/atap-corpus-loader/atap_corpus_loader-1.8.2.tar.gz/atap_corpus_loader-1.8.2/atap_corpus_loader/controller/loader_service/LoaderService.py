from abc import abstractmethod, ABC
from datetime import datetime
from keyword import iskeyword
from typing import Optional, Union

from atap_corpus.corpus.corpus import DataFrameCorpus
from pandas import DataFrame, merge, concat
from panel.widgets import Tqdm

from atap_corpus_loader.controller.data_objects import FileReference, CorpusHeader, FileReferenceFactory, HeaderStrategy
from atap_corpus_loader.controller.loader_service.FileLoadError import FileLoadError
from atap_corpus_loader.controller.loader_service.file_loader_strategy import FileLoaderStrategy, FileLoaderFactory

"""
Some methods in this module utilise Tqdm from the panel library, which breaks the Model-View separation.
This has been done out of necessity for a progress bar for particular operations.
The panel Tqdm is a wrapper for the standard tqdm module and can be replaced if needed.
"""


class LoaderService(ABC):
    def __init__(self):
        self.loaded_corpus_files: set[FileReference] = set()
        self.loaded_meta_files: set[FileReference] = set()
        # Utilise FileReferenceFactory.clear_cache() if memory overhead is raised as an issue.
        self.file_ref_factory: FileReferenceFactory = FileReferenceFactory()
        self.header_strategy: HeaderStrategy = HeaderStrategy.HEADERS

    @abstractmethod
    def get_all_files(self, expand_archived: bool) -> list[FileReference]:
        raise NotImplementedError()

    @abstractmethod
    def add_corpus_files(self, corpus_filepaths: list[str], include_hidden: bool, tqdm_obj: Tqdm):
        raise NotImplementedError()

    @abstractmethod
    def add_meta_files(self, meta_filepaths: list[str], include_hidden: bool, tqdm_obj: Tqdm):
        raise NotImplementedError()

    def get_header_strategy(self) -> HeaderStrategy:
        return self.header_strategy

    def set_header_strategy(self, strategy: Union[HeaderStrategy, str]):
        if isinstance(strategy, HeaderStrategy):
            self.header_strategy = strategy
        elif isinstance(strategy, str):
            try:
                self.header_strategy = HeaderStrategy(strategy)
            except ValueError:
                raise ValueError(f'strategy argument should be a value in the HeaderStrategy enum, instead got {strategy}')
        else:
            TypeError(f"strategy argument should be either str or HeaderStrategy, instead got {type(strategy)}")

    def is_corpus_loaded(self) -> bool:
        return len(self.loaded_corpus_files) > 0

    def is_meta_loaded(self) -> bool:
        return len(self.loaded_meta_files) > 0

    def get_loaded_corpus_files(self) -> set[FileReference]:
        return set([f for f in self.loaded_corpus_files if not f.is_archive()])

    def get_loaded_meta_files(self) -> set[FileReference]:
        return set(f for f in self.loaded_meta_files if not f.is_archive())

    def remove_corpus_filepath(self, corpus_filepath: str):
        file_ref: FileReference = self.file_ref_factory.get_file_ref(corpus_filepath)
        if file_ref in self.loaded_corpus_files:
            self.loaded_corpus_files.remove(file_ref)

    def remove_meta_filepath(self, meta_filepath: str):
        file_ref: FileReference = self.file_ref_factory.get_file_ref(meta_filepath)
        if file_ref in self.loaded_meta_files:
            self.loaded_meta_files.remove(file_ref)

    def remove_loaded_corpus_files(self):
        self.loaded_corpus_files.clear()

    def remove_loaded_meta_files(self):
        self.loaded_meta_files.clear()

    def remove_all_files(self):
        self.remove_loaded_corpus_files()
        self.remove_loaded_meta_files()

    def get_inferred_corpus_headers(self) -> list[CorpusHeader]:
        return self._get_file_headers(self.get_loaded_corpus_files())

    def get_inferred_meta_headers(self) -> list[CorpusHeader]:
        return self._get_file_headers(self.get_loaded_meta_files())

    def _get_file_headers(self, file_refs: set[FileReference]) -> list[CorpusHeader]:
        headers: Optional[list[CorpusHeader]] = None
        for ref in file_refs:
            file_loader: FileLoaderStrategy = FileLoaderFactory.get_file_loader(ref)
            try:
                path_headers: list[CorpusHeader] = file_loader.get_inferred_headers(self.header_strategy)
            except UnicodeDecodeError:
                self.remove_corpus_filepath(ref.get_path())
                self.remove_meta_filepath(ref.get_path())
                raise FileLoadError(f"Error loading file at {ref.get_path()}: file is not UTF-8 encoded")
            except Exception as e:
                self.remove_corpus_filepath(ref.get_path())
                self.remove_meta_filepath(ref.get_path())
                raise FileLoadError(f"Error loading file at {ref.get_path()}: {e}")

            if headers is None:
                headers = path_headers
            elif set(headers) != set(path_headers):
                self.remove_corpus_filepath(ref.get_path())
                self.remove_meta_filepath(ref.get_path())
                raise FileLoadError(f"Incompatible data labels in file: {ref.get_path()}")

        if headers is None:
            headers = []

        return headers

    @staticmethod
    def _is_valid_header_name(header_name: str) -> bool:
        if len(header_name) == 0:
            return False
        start_char = header_name[0]
        if start_char.isdigit() or (start_char == '_'):
            return False
        if iskeyword(header_name):
            return False
        return True

    @staticmethod
    def _get_valid_header_name(header_name: str, existing_headers: list[str]) -> str:
        existing_headers.remove(header_name)
        # Replace all spaces in the meta name with underscores
        header_name = header_name.strip().replace(' ', '_')
        # Remove all special characters from the meta name.
        header_name = ''.join([c for c in header_name if c.isalnum() or c == '_'])
        while not LoaderService._is_valid_header_name(header_name):
            header_name = 'M_' + header_name
        i = 1
        orig_name = header_name
        while header_name in existing_headers:
            header_name = f'{orig_name}_{i}'
            i += 1

        return header_name

    def build_corpus(self, corpus_name: str,
                     corpus_headers: list[CorpusHeader],
                     meta_headers: list[CorpusHeader],
                     text_header: CorpusHeader,
                     corpus_link_header: Optional[CorpusHeader],
                     meta_link_header: Optional[CorpusHeader],
                     tqdm_obj: Tqdm) -> DataFrameCorpus:
        corpus_files: list[FileReference] = sorted(self.get_loaded_corpus_files(), key=lambda f: f.get_path())
        meta_files: list[FileReference] = sorted(self.get_loaded_meta_files(), key=lambda f: f.get_path())

        corpus_df: DataFrame = self._get_concatenated_dataframe(corpus_files, corpus_headers, self.header_strategy,
                                                                tqdm_obj, "Reading corpus files")
        meta_df: DataFrame = self._get_concatenated_dataframe(meta_files, meta_headers, self.header_strategy,
                                                              tqdm_obj, "Reading metadata files")

        if (corpus_df.shape[0] == 0) and (meta_df.shape[0] == 0):
            raise FileLoadError("No corpus documents loaded. Corpus cannot be empty")

        load_corpus: bool = len(corpus_headers) > 0
        load_meta: bool = len(meta_headers) > 0

        final_df: DataFrame
        if load_corpus and load_meta:
            final_df = merge(left=corpus_df, right=meta_df,
                             left_on=corpus_link_header.name, right_on=meta_link_header.name,
                             how='inner', suffixes=(None, '_meta'))
        elif load_corpus:
            final_df = corpus_df
        elif load_meta:
            final_df = meta_df
        else:
            raise FileLoadError("No corpus headers or metadata headers provided")

        col_doc: str = text_header.name
        for header_name in final_df.columns:
            curr_headers = [str(c) for c in final_df.columns]
            renamed = LoaderService._get_valid_header_name(header_name, curr_headers)
            if header_name != renamed:
                if header_name == col_doc:
                    col_doc = renamed
                final_df = final_df.rename({header_name: renamed}, axis=1)

        if (corpus_name == '') or (corpus_name is None):
            corpus_name = f"Corpus-{datetime.now()}"

        return DataFrameCorpus.from_dataframe(final_df, col_doc, corpus_name)

    @staticmethod
    def _dataframe_generator(file_refs: list[FileReference],
                             headers: list[CorpusHeader],
                             header_strategy: HeaderStrategy,
                             tqdm_obj: Tqdm, loading_msg: str):
        for ref in tqdm_obj(file_refs, desc=loading_msg, unit="files", leave=False):
            file_loader: FileLoaderStrategy = FileLoaderFactory.get_file_loader(ref)
            try:
                yield file_loader.get_dataframe(headers, header_strategy, tqdm_obj)
            except UnicodeDecodeError:
                raise FileLoadError(f"Error loading file at {ref.get_path()}: file is not UTF-8 encoded")
            except Exception as e:
                raise FileLoadError(f"Error loading file at {ref.get_path()}: {e}")

    @staticmethod
    def _get_concatenated_dataframe(file_refs: list[FileReference],
                                    headers: list[CorpusHeader],
                                    header_strategy: HeaderStrategy,
                                    tqdm_obj: Tqdm,
                                    loading_msg: str) -> DataFrame:
        if len(file_refs) == 0:
            return DataFrame()

        df_generator = LoaderService._dataframe_generator(file_refs, headers, header_strategy, tqdm_obj, loading_msg)
        return concat(df_generator, ignore_index=True)
