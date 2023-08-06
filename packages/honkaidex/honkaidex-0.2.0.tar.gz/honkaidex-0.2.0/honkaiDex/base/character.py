
from dataclasses import dataclass
import dataclasses
import typing


class BaseCharacterMeta(type):
    instances = {}
    nicknames : dict = {}
    def __call__(cls, *args, **kwargs):
        nicknames = kwargs.get("_nicknames", None)
        name = kwargs.get("_name", None)
        
        if name is None:
            raise ValueError("_name is required")
        name : str = name.lower().strip()
        
        if nicknames is None:
            nicknames = []

        if cls not in cls.instances:
            kwargs.pop("_nicknames", None)
            kwargs.pop("_name", None)
            cls.instances[name] = super().__call__(_nicknames=nicknames, _name=name, _else=kwargs)
            for nickname in nicknames:
                cls.nicknames[nickname] = cls.instances[name]
        
        return cls.instances[name]

@dataclass
class BaseCharacter(metaclass=BaseCharacterMeta):
    _name : str
    _nicknames : typing.List[str] = dataclasses.field(default_factory=lambda : [])
    _else : dict = dataclasses.field(default_factory=lambda : {})
    @property
    def name(self):
        return self._name

    @property
    def nicknames(self):
        return self._nicknames

    @staticmethod
    def get(name: str, nickname_allowed : bool = False, partial_search : bool = False) -> typing.Union['BaseCharacter', None]:
        name = name.strip().lower()

        item = BaseCharacter.instances.get(name, None)
        if item is not None:
            return item

        if nickname_allowed:
            item = BaseCharacter.nicknames.get(name, None)
            if item is not None:
                return item

        if partial_search:
            for val in BaseCharacter.instances.values():
                if name in val.name:
                    return val
        
        if nickname_allowed and partial_search:
            for key, val in BaseCharacter.nicknames.items():
                if name in key:
                    return val

                

    def __del__(self):
        self.__class__.instances.pop(self.name, None)
        for nickname in self.nicknames:
            self.__class__.nicknames.pop(nickname, None)

    @staticmethod
    def create(name: str, nicknames: typing.List[str] = None, **kwargs):
        if nicknames is None:
            nicknames = []
        return BaseCharacter(name=name, _nicknames=nicknames, **kwargs)


from enum import Enum
class BattlesuitType(Enum):
    MECH = "Mech"
    PSY = "Psy"
    BIO = "Bio"
    QUA = "Qua"
    IMG = "Img"

class BattlesuitMeta(type):
    abbrevs = {}
    instances = {}
    def __call__(cls, *args, **kwargs):
        name = kwargs.get("_name", None)

        if name is None:
            raise ValueError("name is required")
        
        name : str = name.lower().strip()

        abbrevs = kwargs.get("_battlesuit_abbrevs", [])
        if abbrevs is None:
            abbrevs = []
        

        if name not in cls.instances:
            cls.instances[name] = super().__call__(*args, **kwargs)
            for abbrev in abbrevs:
                abbrev = abbrev.lower().strip()
                cls.abbrevs[abbrev] = name


        return cls.instances[name]

@dataclass
class Battlesuit(metaclass=BattlesuitMeta):
    _base_character : BaseCharacter
    _name : str
    _version_released : str
    _rairty : str
    _tags : typing.List[str] = dataclasses.field(default_factory=lambda : [])
    _img_link : str = None
    _else : dict = dataclasses.field(default_factory=lambda : {})
    _type : BattlesuitType = None
    _battlesuit_abbrevs : typing.List[str] = dataclasses.field(default_factory=lambda : [])

    @property
    def bs_type(self):
        return self._type

    @property
    def character(self):
        return self._base_character

    @property
    def shards_needed(self):
        return self._unlock_shards

    @property
    def name(self):
        return self._name
    
    @property
    def version_released(self):
        return self._version_released

    @property
    def rarity(self):
        return self._rairty

    @property
    def tags(self):
        return self._tags

    @property
    def img_link(self):
        return self._img_link
    
    @property
    def meta(self):
        return self._else

    def __str__(self):
        return f"{self.name} ({self.bs_type})"

    @staticmethod
    def all():
        return list(Battlesuit.instances.values())
    
    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def get(name: str , allow_nickname : bool = False, partial_search : bool = False):
        name = name.strip().lower()
        item = Battlesuit.instances.get(name, None)
        if item is not None:
            return item

        if allow_nickname:
            name = Battlesuit.abbrevs.get(name, None)
            if name is not None:
                return Battlesuit.instances[name]

        if partial_search:
            for item in Battlesuit.instances.values():
                item : Battlesuit
                if name in item.name.lower():
                    return item
        
        if allow_nickname and partial_search:
            for val in Battlesuit.abbrevs.keys():
                if name in val:
                    return Battlesuit.instances[Battlesuit.abbrevs[name]]

    @staticmethod
    def get_all(**kwargs):
        ret = []
        for item in Battlesuit.instances.values():
            item : Battlesuit
            if all(kwargs[key] == getattr(item, "_"+key) for key in kwargs.keys()):
                ret.append(item)
        return ret

    @staticmethod
    def create(
        name: str, 
        base_character: BaseCharacter, 
        type_   : str,
        version_released: str, 
        rarity: str,
        tags: typing.List[str] = None, 
        img_link: str = None, 
        abbrevs: typing.List[str] = None,
        **kwargs
    ):
        if tags is None:
            tags = []
        # get battlesuit_type
        for bs_type in BattlesuitType:
            if bs_type.value == type_:
                type_ = bs_type
                break
        

        return Battlesuit(
            name=name, 
            _base_character=base_character, 
            _version_released=version_released, 
            _rairty=rarity, 
            _type=type_,
            _tags=tags, 
            _img_link=img_link, 
            _battlesuit_abbrevs=abbrevs,
            _else=kwargs
        )