import logging
from typing import Optional, Iterable

from atap_corpus._types import TCorpus
from atap_corpus.corpus.base import BaseCorpora, BaseCorpus
from atap_corpus.utils import format_dunder_str


class UniqueNameCorpora(BaseCorpora):
    """
    UniqueNameCorpora is a container for BaseCorpus objects that ensures all corpus objects have unique names within the Corpora.
    Additionally, while stored within the Corpora, the rename method of the BaseCorpus objects is replaced with a rename method
    that ensures the new name is unique.
    """

    def __init__(self, logger_name: str, corpus: Optional[BaseCorpus | Iterable[BaseCorpus]] = None):
        super().__init__(corpus)
        logger = logging.getLogger(logger_name)
        self._collection = dict()
        if corpus is None:
            return
        elif isinstance(corpus, Iterable):
            for c in corpus:
                if c.name in self._collection.keys():
                    logger.warning(f"Corpus name: {c.name} is duplicated. Only one is kept for uniqueness.")
                else:
                    self.add(c)
        elif isinstance(corpus, BaseCorpus):
            self.add(corpus)
        else:
            raise TypeError(f"Corpora can only store Corpus objects. Got {corpus.__class__.__name__}.")

    def _verify_unique_name(self, name: str):
        if name in self._collection:
            raise ValueError(f"Corpus with name '{name}' already exists. Select a different name")

    def _unique_rename(self, corpus: TCorpus, name: str):
        self._verify_unique_name(name)
        old_name = corpus.name
        corpus._name = name
        self._collection[name] = self._collection.pop(old_name)

    def add(self, corpus: TCorpus):
        """ Adds a Corpus into the Corpora. Corpus name is used as the name for get(), remove().
        If a corpus with the same name is added again, a ValueError is raised.
        If a corpus is added with a name that is empty or None, it is renamed to a generated name based on the current time.
        BaseCorpus objects added have their rename method replaced to include a check for name uniqueness.
        """
        if not isinstance(corpus, BaseCorpus):
            raise TypeError(f"Corpora can only store Corpus objects. Got {corpus.__class__.__name__}.")

        self._verify_unique_name(corpus.name)

        corpus.__ORIG_RENAME = corpus.rename
        corpus.rename = lambda new_name, corpus_obj=corpus: self._unique_rename(corpus_obj, new_name)
        self._collection[corpus.name] = corpus

    def remove(self, name: str):
        """ Remove a Corpus from the Corpora.
        The rename method of the Corpus object has the unique name constraint removed before it is removed from the Corpora.
        If Corpus does not exist, it'll have no effect.
        """
        try:
            self._collection[name].rename = self._collection[name].__ORIG_RENAME
            del self._collection[name]
        except KeyError:
            return

    def items(self) -> list[TCorpus]:
        """
        Returns a shallow copy list of the corpus objects in the Corpora, in order of addition.
        :return: A list of corpus objects found in the Corpora
        :rtype: list[TCorpus]
        """
        return list(self._collection.values())

    def get(self, name: str) -> Optional[TCorpus]:
        """
        Returns the corpus object corresponding with the provided name.
        If no corpus exists with the name, returns None.
        :param name: name of the corpus to be retrieved
        :type name: str
        :return: The corresponding corpus, or None if not found
        :rtype: Optional[TCorpus]
        """
        return self._collection.get(name)

    def clear(self):
        """
        Clears the Corpora of all corpus objects.
        """
        self._collection = dict()

    def __len__(self) -> int:
        """
        :return: the number of Corpus in the Corpora.
        :rtype: int
        """
        return len(self._collection)

    def __str__(self) -> str:
        return format_dunder_str(self.__class__, **{"size": len(self)})
