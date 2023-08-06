from dataclasses import dataclass
import dataclasses
import typing

class StigPieceMetaClass(type):
    t_piece = {}
    m_piece = {}
    b_piece = {}

    def __call__(cls, *args, **kwargs):
        if "__stig_pos__" not in kwargs:
            raise ValueError("__stig_pos__ is required")
        if "__stig_set__" not in kwargs:
            raise ValueError("__stig_set__ is required")
        stig_pos = kwargs.get("__stig_pos__", None)
        if stig_pos is None:
            raise ValueError("__stig_pos__ cannot be None")
        if stig_pos < 0 or stig_pos > 3:
            raise ValueError("__stig_pos__ must be between 0 and 3")
        
        stig_set = kwargs.get("__stig_set__", None)
        if stig_set is None or not isinstance(stig_set, StigamataSet):
            raise ValueError("__stig_set__ cannot be None")
        stig_name = stig_set.name
        stig_pos = int(stig_pos)
        
        if stig_pos == 0:
            interested_dict = cls.t_piece
        elif stig_pos == 1:
            interested_dict = cls.m_piece
        else:
            interested_dict = cls.b_piece

        if stig_name not in interested_dict:
            interested_dict[stig_name] = super().__call__(*args, **kwargs)
        
        return interested_dict[stig_name]


@dataclass
class StigamataPiece(metaclass=StigPieceMetaClass):
    __stig_pos__ : int
    __stig_set__ : 'StigamataSet'

    def __post_init__(self):
        if not (0 <= self.__stig_pos__ <=2):
            raise ValueError("__stig_pos__ must be between 0 and 2")

    @property
    def pos(self) -> int:
        return self.__stig_pos__

    @property
    def is_top(self):
        return self.__stig_pos__ == 0

    @property
    def is_middle(self):
        return self.__stig_pos__ == 1

    @property
    def is_bottom(self):
        return self.__stig_pos__ == 2

    @staticmethod
    def get_top(stig_name : str):
        return StigamataPiece.t_piece.get(stig_name, None)
    
    @staticmethod
    def get_middle(stig_name : str):
        return StigamataPiece.m_piece.get(stig_name, None)

    @staticmethod
    def get_bottom(stig_name : str):
        return StigamataPiece.b_piece.get(stig_name, None)
    
    @property
    def effect(self):
        return self.__stig_set__.effect(self.__stig_pos__)

    @property
    def hoyo_id(self):
        return self.__stig_set__._lab_ids[self.__stig_pos__]

    @property
    def stigset(self) -> 'StigamataSet':
        """
        returns the stig set object of this piece
        """
        return self.__stig_set__

    def __str__(self) -> str:
        if self.is_top:
            return f"{self.__stig_set__._set_name} (T)"
        elif self.is_middle:
            return f"{self.__stig_set__._set_name} (M)"
        else:
            return f"{self.__stig_set__._set_name} (B)"


class StigmataSetMetaClass(type):
    instances = {}
    alt_name_instances = {}

    def __call__(cls, *args, **kwargs):
        if "_set_name" not in kwargs:
            raise ValueError("_set_name is required")
        set_name = kwargs.get("_set_name", None)
        if set_name is None:
            raise ValueError("_set_name cannot be None")

        alt_names = kwargs.pop("alt_names", None)


        if set_name not in cls.instances:
            make_item = super().__call__(*args, **kwargs)
            set_name = set_name.lower()

            if alt_names and isinstance(alt_names, typing.List[str]):
                    for name in alt_names:
                        name = name.lower()
                        cls.alt_name_instances[name] = cls.instances[set_name]
            
            cls.instances[set_name] = make_item

        return cls.instances[set_name]

@dataclass
class StigamataSet(metaclass=StigmataSetMetaClass):
    _set_name : str
    _top_e : str = None
    _mid_e : str = None
    _bot_e : str = None
    _two_piece : str = None
    _three_piece : str = None
    _lab_id : int = None
    # default factory
    _lab_ids : list = dataclasses.field(default_factory=lambda : [None, None, None])
    _else : dict = dataclasses.field(default_factory=lambda : {})

    def __post_init__(self):
        top = self.top
        mid = self.middle
        bot = self.bottom

    @property
    def name(self):
        return self._set_name

    def effect(self, pos: int):
        if pos == 0:
            return self._top_e
        elif pos == 1:
            return self._mid_e
        elif pos == 2:
            return self._bot_e
        else:
            raise ValueError("pos must be between 0 and 2")

    def has_effect(self, pos: int):
        return self.effect(pos) is not None

    @property
    def has_top(self):
        return self._top_e is not None

    @property
    def has_middle(self):
        return self._mid_e is not None
    
    @property
    def has_bottom(self):
        return self._bot_e is not None

    @property
    def top(self):
        if not self.has_top:
            return None

        return StigamataPiece(
            __stig_pos__=0,
            __stig_set__=self
        )

    @property
    def middle(self):
        if not self.has_middle:
            return None

        return StigamataPiece(
            __stig_pos__=1,
            __stig_set__=self
        )
    
    @property
    def bottom(self):
        if not self.has_bottom:
            return None
    
        return StigamataPiece(
            __stig_pos__=2,
            __stig_set__=self
        )

    @property
    def two_piece(self) -> str:
        return self._two_piece
    
    @property
    def three_piece(self) -> str:
        return self._three_piece

    @staticmethod
    def create(
        name : str, 
        top : str = None, 
        mid : str = None, 
        bot : str = None, 
        two_piece : str = None, 
        three_piece : str = None,
        top_id : int = None,
        mid_id : int = None,
        bot_id : int = None,
        id : int = None,
        alternative_names : typing.List[str] = None,
        **kwargs
    ):
        return StigamataSet(
            _set_name=name,
            _top_e=top,
            _mid_e=mid,
            _bot_e=bot,
            _two_piece=two_piece,
            _three_piece=three_piece,
            _lab_id=id,
            _lab_ids=[top_id, mid_id, bot_id],
            alt_names = alternative_names,
            _else=kwargs
        )

    @staticmethod
    def iterate() -> typing.Generator['StigamataSet', None, None]:
        for val in StigmataSetMetaClass.instances.values():
            yield val

    @staticmethod
    def get(name : str, alt : bool = False, partial_search : bool = False) -> typing.Union['StigamataSet', None]:
        name = name.lower()
        if alt and name in StigmataSetMetaClass.alt_name_instances:
            return StigmataSetMetaClass.alt_name_instances[name]

        getfull = StigmataSetMetaClass.instances.get(name, None)
        if getfull is not None:
            return getfull
        
        if partial_search:
            for val in StigamataSet.iterate():
                val : StigamataSet
                if val.name.lower().startswith(name):
                    return val