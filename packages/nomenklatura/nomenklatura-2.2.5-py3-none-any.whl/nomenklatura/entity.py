from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, TypeVar, cast
from followthemoney.model import Model
from followthemoney.proxy import EntityProxy

from nomenklatura.dataset import Dataset, DatasetIndex

if TYPE_CHECKING:
    from nomenklatura.loader import Loader


class CompositeEntity(EntityProxy):
    """An entity object that can link to a set of datasets that it is sourced from."""

    def __init__(
        self,
        model: Model,
        data: Dict[str, Any],
        key_prefix: Optional[str] = None,
        cleaned: bool = True,
    ) -> None:
        super().__init__(model, data, key_prefix=key_prefix, cleaned=cleaned)
        self.datasets: Set[Dataset] = set()
        """The set of datasets from which information in this entity is derived."""

        self.referents: Set[str] = set()
        """The IDs of all entities which are included in this canonical entity."""

    def merge(self, other: "EntityProxy") -> "CompositeEntity":
        """Merge another entity proxy into this one. For composite entities, this
        will update the datasets and referents data accordingly."""
        merged = cast(CompositeEntity, super().merge(other))
        if isinstance(other, CompositeEntity):
            merged.referents.update(other.referents)
            merged.datasets.update(other.datasets)
        return merged

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["referents"] = list(self.referents)
        data["datasets"] = [d.name for d in self.datasets]
        return data

    def _to_nested_dict(
        self, loader: "Loader[DS, CompositeEntity]", depth: int, path: List[str]
    ) -> Dict[str, Any]:
        next_depth = depth if self.schema.edge else depth - 1
        next_path = path + [self.id]
        data = self.to_dict()
        if next_depth < 0:
            return data
        nested: Dict[str, Any] = {}
        for prop, adjacent in loader.get_adjacent(self):
            if adjacent.id in next_path:
                continue
            value = adjacent._to_nested_dict(loader, next_depth, next_path)
            if prop.name not in nested:
                nested[prop.name] = []
            nested[prop.name].append(value)
        data["properties"].update(nested)
        return data

    def to_nested_dict(
        self, loader: "Loader[DS, CompositeEntity]", depth: int = 1
    ) -> Dict[str, Any]:
        return self._to_nested_dict(loader, depth=depth, path=[])

    @classmethod
    def from_data(
        cls,
        model: Model,
        data: Dict[str, Any],
        datasets: DatasetIndex,
        cleaned: bool = True,
    ) -> "CompositeEntity":
        obj = cls(model, data, cleaned=cleaned)
        obj.id = data["id"]
        for dataset_name in data.get("datasets", []):
            dataset = datasets.get(dataset_name)
            if dataset is not None:
                obj.datasets.add(dataset)
        obj.referents.update(data.get("referents", []))
        return obj


E = TypeVar("E", bound=CompositeEntity)
DS = TypeVar("DS", bound=Dataset)
