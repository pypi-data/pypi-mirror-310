from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Dict

if TYPE_CHECKING:
  from ..models.plot_data_stats import PlotDataStats





T = TypeVar("T", bound="PlotInfoObjectStatsType0")


@_attrs_define
class PlotInfoObjectStatsType0:
    """ 
     """

    additional_properties: Dict[str, 'PlotDataStats'] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.plot_data_stats import PlotDataStats
        
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.plot_data_stats import PlotDataStats
        d = src_dict.copy()
        plot_info_object_stats_type_0 = cls(
        )


        from ..models.plot_data_stats_percentiles import PlotDataStatsPercentiles
        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = PlotDataStats.from_dict(prop_dict)



            additional_properties[prop_name] = additional_property

        plot_info_object_stats_type_0.additional_properties = additional_properties
        return plot_info_object_stats_type_0

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> 'PlotDataStats':
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: 'PlotDataStats') -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
