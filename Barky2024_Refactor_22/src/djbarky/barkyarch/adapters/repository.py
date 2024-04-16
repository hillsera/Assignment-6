from typing import Set
import abc
from barkyarch.domain.model import DomainBookmark
from barkyapi.models import Bookmark


class AbstractRepository(abc.ABC):
    """
    Because it is based on an ABC, this abstract class repository can be used with
    any data storage strategy.
    """

    def __init__(self):
        self.bookmarks_set = set()  # type: Set[DomainBookmark]

    def add(self, bookmark: DomainBookmark):
        self.bookmarks_set.add(bookmark)

    def get(self, id) -> DomainBookmark:
        bookmark = self._get(id)
        if bookmark:
            self.bookmarks_set.add(bookmark)
        return bookmark

    @abc.abstractmethod
    def _get(self, id):
        raise NotImplementedError
    
    # delete
    @abc.abstractmethod
    def delete(self, bookmark_id):
        raise NotImplementedError
    
    # edit bookmark
    @abc.abstractmethod
    def edit(self, bookmark_id, new_data):
        raise NotImplementedError


class DjangoRepository(AbstractRepository):
    """
    This concrete instance of the repository uses the Django ORM as the data storage strategy.
    """

    def add(self, bookmark):
        super().add(bookmark)
        self.update(bookmark)

    def update(self, bookmark):
        Bookmark.update_from_domain(bookmark)

    def _get(self, id):
        return Bookmark.objects.filter(id=id).first().to_domain()

    def list(self):
        return [bookmark.to_domain() for bookmark in Bookmark.objects.all()]
    
    # delete
    def delete(self, bookmark_id):
        try:
            bookmark = Bookmark.objects.get(id=bookmark_id)
            bookmark.delete()
        except Bookmark.DoesNotExist:
            pass

    
    # edit bookmark
    def edit(self, bookmark_id, new_data):
        try:
            bookmark = Bookmark.objects.get(id=bookmark_id)
            for field, value in new_data.items():
                setattr(bookmark, field, value)
            bookmark.save()
        except Bookmark.DoesNotExist:
            pass

class DjangoApiRepository(AbstractRepository):
    """
    This concrete instance of the repository uses the DRF, which abstracts its own data storage
    strategy.
    """

    def add(self, bookmark):
        # super().add(bookmark)
        # self.update(bookmark)
        pass

    def update(self, bookmark):
        # django_models.Bookmark.update_from_domain(bookmark)
        pass

    def _get(self, id):
        # return (
        #     django_models.Bookmark.objects.filter(id=id)
        #     .first()
        #     .to_domain()
        # )
        pass

    def list(self):
        # return [bookmark.to_domain() for bookmark in django_models.Bookmark.objects.all()]
        pass
