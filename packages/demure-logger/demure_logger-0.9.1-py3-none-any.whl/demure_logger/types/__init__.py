from typing  import Optional, get_origin, get_args, Generic, TypeVar


T = TypeVar('T')

NO_ARG = object()


class Parent(Generic[T]):
    arg = NO_ARG  # using `arg` to store the current type argument

    def __class_getitem__(cls, key):
        if cls.arg is NO_ARG or cls.arg is T:
            cls.arg = key 
        else:
            try:
                cls.arg = cls.arg[key]
            except TypeError:
                cls.arg = key
        return super().__class_getitem__(key)

    def __init_subclass__(cls):
        if Parent.arg is not NO_ARG:
            cls.arg, Parent.arg = Parent.arg, NO_ARG



def get_parent_type_parameter( child: type, parent: type ) -> Optional[str]:
    for base in child.mro( ):
        for generic_base in getattr( base, "__orig_bases__", () ):
            if get_origin( generic_base ) is parent:
                [ type_argument ] = get_args( generic_base )

                return type_argument

    return None