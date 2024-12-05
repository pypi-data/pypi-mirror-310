from enum import Enum, auto

from atap_corpus_loader.controller.data_objects import FileReference
from atap_corpus_loader.controller.loader_service.FileLoadError import FileLoadError
from atap_corpus_loader.controller.loader_service.file_loader_strategy.concrete_strategies import *
from atap_corpus_loader.controller.loader_service.file_loader_strategy.FileLoaderStrategy import FileLoaderStrategy


class ValidFileType(Enum):
    """
    An enum of valid file extensions that are supported with a loader
    """
    TXT = auto()
    DOCX = auto()
    ODT = auto()
    CSV = auto()
    TSV = auto()
    XLSX = auto()
    ODS = auto()
    XML = auto()
    ZIP = auto()


class FileLoaderFactory:
    """
    Provides a single public method to map a FileReference object to concrete FileLoaderStrategy object

    FILETYPE_LOADER_MAP maps file extensions to concrete FileLoaderStrategy types.
    The file extensions are treated as case-insensitive
    """
    FILETYPE_LOADER_MAP: dict = {
        ValidFileType.TXT: TXTLoaderStrategy,
        ValidFileType.DOCX: DOCXLoaderStrategy,
        ValidFileType.ODT: ODTLoaderStrategy,
        ValidFileType.CSV: CSVLoaderStrategy,
        ValidFileType.TSV: TSVLoaderStrategy,
        ValidFileType.XLSX: XLSXLoaderStrategy,
        ValidFileType.ODS: ODSLoaderStrategy,
        ValidFileType.XML: XMLLoaderStrategy
    }

    @staticmethod
    def get_file_loader(file_ref: FileReference) -> FileLoaderStrategy:
        """
        Maps the provided FileReference object to a concrete FileLoaderStrategy object based on the extension.
        If the file extension is missing (the filename is not of the format <name>.<extension> or is not
        valid, i.e. is not a member of the ValidFileType enum) a FileLoadError will be raised.
        :param file_ref: the FileReference object corresponding to the file to assign a loader to
        :return: a concrete FileLoaderStrategy object that has been passed the provided FileReference object.
        :raises FileLoadError: if there is no '.' in the file name or the extension after the '.' is not a valid file type
        """
        file_name: str = file_ref.get_filename()
        file_extension: str = file_ref.get_extension().upper()
        if file_extension == '':
            raise FileLoadError(f"No file extension found in file name: {file_name}. "
                                f"File name must be in format <filename>.<extension>")

        try:
            file_type: ValidFileType = ValidFileType[file_extension]
            file_loader: FileLoaderStrategy = FileLoaderFactory.FILETYPE_LOADER_MAP[file_type](file_ref)
        except KeyError:
            accepted_types: str = ', '.join([ft.name for ft in ValidFileType])
            raise FileLoadError(f"Invalid file type loaded: {file_extension}. Valid file types: {accepted_types}")

        return file_loader
