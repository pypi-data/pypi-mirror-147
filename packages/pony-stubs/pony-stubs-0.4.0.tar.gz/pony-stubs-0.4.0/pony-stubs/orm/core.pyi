from collections.abc import Generator
from typing import Any, Callable, Generic, Iterable, Type, TypeVar, Union, overload

import pony as pony
from pony.orm.asttranslation import TranslationError as TranslationError
from pony.orm.dbapiprovider import DatabaseError as DatabaseError
from pony.orm.dbapiprovider import DataError as DataError
from pony.orm.dbapiprovider import DBException as DBException
from pony.orm.dbapiprovider import Error as Error
from pony.orm.dbapiprovider import IntegrityError as IntegrityError
from pony.orm.dbapiprovider import InterfaceError as InterfaceError
from pony.orm.dbapiprovider import InternalError as InternalError
from pony.orm.dbapiprovider import NotSupportedError as NotSupportedError
from pony.orm.dbapiprovider import OperationalError as OperationalError
from pony.orm.dbapiprovider import ProgrammingError as ProgrammingError
from pony.orm.dbapiprovider import Warning as Warning
from pony.orm.ormtypes import FloatArray as FloatArray
from pony.orm.ormtypes import IntArray as IntArray
from pony.orm.ormtypes import Json as Json
from pony.orm.ormtypes import LongStr as LongStr
from pony.orm.ormtypes import LongUnicode as LongUnicode
from pony.orm.ormtypes import StrArray as StrArray
from pony.orm.ormtypes import raw_sql as raw_sql
from pony.py23compat import buffer as buffer
from pony.py23compat import unicode as unicode
from pony.utils import between as between
from pony.utils import coalesce as coalesce
from pony.utils import concat as concat
from pony.utils import localbase

log_sql: Any
log_orm: Any
const_functions: Any
extract_vars: Any
special_functions: Any

def sql_debug(value: Any) -> None: ...
def set_sql_debug(debug: bool = ..., show_values: Any | None = ...) -> None: ...

class OrmError(Exception): ...
class ERDiagramError(OrmError): ...
class DBSchemaError(OrmError): ...
class MappingError(OrmError): ...
class BindingError(OrmError): ...
class TableDoesNotExist(OrmError): ...
class TableIsNotEmpty(OrmError): ...
class ConstraintError(OrmError): ...
class CacheIndexError(OrmError): ...
class RowNotFound(OrmError): ...
class MultipleRowsFound(OrmError): ...
class TooManyRowsFound(OrmError): ...
class PermissionError(OrmError): ...

class ObjectNotFound(OrmError):
    def __init__(exc, entity: Any, pkval: Any | None = ...) -> None: ...

class MultipleObjectsFoundError(OrmError): ...
class TooManyObjectsFoundError(OrmError): ...
class OperationWithDeletedObjectError(OrmError): ...
class TransactionError(OrmError): ...
class ConnectionClosedError(TransactionError): ...

class TransactionIntegrityError(TransactionError):
    def __init__(exc, msg: Any, original_exc: Any | None = ...) -> None: ...

class CommitException(TransactionError):
    def __init__(exc, msg: Any, exceptions: Any) -> None: ...

class PartialCommitException(TransactionError):
    def __init__(exc, msg: Any, exceptions: Any) -> None: ...

class RollbackException(TransactionError):
    def __init__(exc, msg: Any, exceptions: Any) -> None: ...

class DatabaseSessionIsOver(TransactionError): ...

TransactionRolledBack = DatabaseSessionIsOver

class IsolationError(TransactionError): ...
class UnrepeatableReadError(IsolationError): ...
class OptimisticCheckError(IsolationError): ...
class UnresolvableCyclicDependency(TransactionError): ...

class UnexpectedError(TransactionError):
    def __init__(exc, msg: Any, original_exc: Any) -> None: ...

class ExprEvalError(TranslationError):
    def __init__(exc, src: Any, cause: Any) -> None: ...

class PonyInternalException(Exception): ...
class OptimizationFailed(PonyInternalException): ...

class UseAnotherTranslator(PonyInternalException):
    translator: Any
    def __init__(self, translator: Any) -> None: ...

class PonyRuntimeWarning(RuntimeWarning): ...
class DatabaseContainsIncorrectValue(PonyRuntimeWarning): ...
class DatabaseContainsIncorrectEmptyValue(DatabaseContainsIncorrectValue): ...

class PrefetchContext:
    database: Any
    attrs_to_prefetch_dict: Any
    entities_to_prefetch: Any
    relations_to_prefetch_cache: Any
    def __init__(self, database: Any | None = ...) -> None: ...
    def copy(self) -> Any: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
    def get_frozen_attrs_to_prefetch(self, entity: Any) -> Any: ...
    def get_relations_to_prefetch(self, entity: Any) -> Any: ...

class Local(localbase):
    def __init__(local) -> None: ...
    @property
    def prefetch_context(local) -> Any: ...
    def push_debug_state(local, debug: Any, show_values: Any) -> None: ...
    def pop_debug_state(local) -> None: ...

def flush() -> None: ...
def commit() -> None: ...
def rollback() -> None: ...

class DBSessionContextManager:
    def __init__(
        db_session,
        retry: int = ...,
        immediate: bool = ...,
        ddl: bool = ...,
        serializable: bool = ...,
        strict: bool = ...,
        optimistic: bool = ...,
        retry_exceptions: Any = ...,
        allowed_exceptions: Any = ...,
        sql_debug: Any | None = ...,
        show_values: Any | None = ...,
    ) -> None: ...
    def __call__(db_session, *args: Any, **kwargs: Any) -> Any: ...
    def __enter__(db_session) -> None: ...
    def __exit__(
        db_session,
        exc_type: Any | None = ...,
        exc: Any | None = ...,
        tb: Any | None = ...,
    ) -> None: ...

db_session: Any

class SQLDebuggingContextManager:
    debug: Any
    show_values: Any
    def __init__(self, debug: bool = ..., show_values: Any | None = ...) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self, exc_type: Any | None = ..., exc: Any | None = ..., tb: Any | None = ...
    ) -> None: ...

sql_debugging: Any

def with_transaction(*args: Any, **kwargs: Any) -> Any: ...

class OnConnectDecorator:
    @staticmethod
    def check_provider(provider: Any) -> None: ...
    provider: Any
    database: Any
    def __init__(self, database: Any, provider: Any) -> None: ...
    def __call__(self, func: Any | None = ..., provider: Any | None = ...) -> Any: ...

class Database:
    def __deepcopy__(self, memo: Any) -> Any: ...
    id: Any
    priority: int
    entities: Any
    schema: Any
    Entity: Entity
    on_connect: Any
    provider: Any
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def call_on_connect(database, con: Any) -> None: ...
    def bind(self, *args: Any, **kwargs: Any) -> None: ...
    @property
    def last_sql(database) -> Any: ...
    @property
    def local_stats(database) -> Any: ...
    def merge_local_stats(database) -> None: ...
    @property
    def global_stats(database) -> Any: ...
    @property
    def global_stats_lock(database) -> Any: ...
    def get_connection(database) -> Any: ...
    def disconnect(database) -> None: ...
    def flush(database) -> None: ...
    def commit(database) -> None: ...
    def rollback(database) -> None: ...
    def execute(
        database, sql: Any, globals: Any | None = ..., locals: Any | None = ...
    ) -> Any: ...
    def select(
        database,
        sql: Any,
        globals: Any | None = ...,
        locals: Any | None = ...,
        frame_depth: int = ...,
    ) -> Any: ...
    def get(
        database, sql: Any, globals: Any | None = ..., locals: Any | None = ...
    ) -> Any: ...
    def exists(
        database, sql: Any, globals: Any | None = ..., locals: Any | None = ...
    ) -> Any: ...
    def insert(
        database, table_name: Any, returning: Any | None = ..., **kwargs: Any
    ) -> Any: ...
    def generate_mapping(
        database,
        filename: Any | None = ...,
        check_tables: bool = ...,
        create_tables: bool = ...,
    ) -> Any: ...
    def drop_table(
        database, table_name: Any, if_exists: bool = ..., with_all_data: bool = ...
    ) -> None: ...
    def drop_all_tables(database, with_all_data: bool = ...) -> None: ...
    def create_tables(database, check_tables: bool = ...) -> None: ...
    def check_tables(database) -> None: ...
    def set_perms_for(database, *entities: Any) -> Generator[None, None, None]: ...
    def to_json(
        database,
        data: Any,
        include: Any = ...,
        exclude: Any = ...,
        converter: Any | None = ...,
        with_schema: bool = ...,
        schema_hash: Any | None = ...,
    ) -> Any: ...
    def from_json(database, changes: Any, observer: Any | None = ...) -> Any: ...

def perm(*args: Any, **kwargs: Any) -> Any: ...

class AccessRule:
    def __init__(
        rule,
        database: Any,
        entities: Any,
        permissions: Any,
        groups: Any,
        roles: Any,
        labels: Any,
    ) -> None: ...
    def exclude(rule, *args: Any) -> None: ...

def has_perm(user: Any, perm: Any, x: Any) -> Any: ...
def get_current_user() -> Any: ...
def set_current_user(user: Any) -> None: ...
def get_user_groups(user: Any) -> Any: ...
def get_user_roles(user: Any, obj: Any) -> Any: ...
def get_object_labels(obj: Any) -> Any: ...
def user_groups_getter(cls: Any | None = ...) -> Any: ...
def user_roles_getter(user_cls: Any | None = ..., obj_cls: Any | None = ...) -> Any: ...
def obj_labels_getter(cls: Any | None = ...) -> Any: ...

class DbLocal(localbase):
    def __init__(dblocal) -> None: ...

class QueryStat:
    def __init__(stat, sql: Any, duration: Any | None = ...) -> None: ...
    def copy(stat) -> Any: ...
    def query_executed(stat, duration: Any) -> None: ...
    def merge(stat, stat2: Any) -> None: ...
    @property
    def avg_time(stat) -> Any: ...

class SessionCache:
    def __init__(cache, database: Any) -> None: ...
    def connect(cache) -> Any: ...
    def reconnect(cache, exc: Any) -> Any: ...
    def prepare_connection_for_query_execution(cache) -> Any: ...
    def flush_and_commit(cache) -> None: ...
    def commit(cache) -> None: ...
    def rollback(cache) -> None: ...
    def release(cache) -> None: ...
    def close(cache, rollback: bool = ...) -> None: ...
    def flush_disabled(cache) -> Generator[None, None, None]: ...
    def flush(cache) -> None: ...
    def call_after_save_hooks(cache) -> None: ...
    def update_simple_index(
        cache, obj: Any, attr: Any, old_val: Any, new_val: Any, undo: Any
    ) -> None: ...
    def db_update_simple_index(
        cache, obj: Any, attr: Any, old_dbval: Any, new_dbval: Any
    ) -> None: ...
    def update_composite_index(
        cache, obj: Any, attrs: Any, prev_vals: Any, new_vals: Any, undo: Any
    ) -> None: ...
    def db_update_composite_index(
        cache, obj: Any, attrs: Any, prev_vals: Any, new_vals: Any
    ) -> None: ...

class NotLoadedValueType: ...
class DefaultValueType: ...

class DescWrapper:
    attr: Any
    def __init__(self, attr: Any) -> None: ...
    def __call__(self) -> Any: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...

AttributeType = TypeVar("AttributeType")

class Attribute(Generic[AttributeType]):
    def __deepcopy__(attr, memo: Any) -> Any: ...
    def __init__(attr, py_type: AttributeType, *args: Any, **kwargs: Any) -> None: ...
    def linked(attr) -> None: ...
    def __lt__(attr, other: Any) -> Any: ...
    def validate(
        attr,
        val: Any,
        obj: Any | None = ...,
        entity: Any | None = ...,
        from_db: bool = ...,
    ) -> Any: ...
    def parse_value(
        attr, row: Any, offsets: Any, dbvals_deduplication_cache: Any
    ) -> Any: ...
    def load(attr, obj: Any) -> Any: ...
    def __get__(attr, obj: Any, cls: Any | None = ...) -> AttributeType: ...
    def get(attr, obj: Any) -> Any: ...
    def __set__(attr, obj: Any, new_val: Any, undo_funcs: Any | None = ...) -> None: ...
    def db_set(attr, obj: Any, new_dbval: Any, is_reverse_call: bool = ...) -> None: ...
    def update_reverse(
        attr, obj: Any, old_val: Any, new_val: Any, undo_funcs: Any
    ) -> None: ...
    def db_update_reverse(attr, obj: Any, old_dbval: Any, new_dbval: Any) -> None: ...
    def __delete__(attr, obj: Any) -> None: ...
    def get_raw_values(attr, val: Any) -> Any: ...
    def get_columns(attr) -> Any: ...
    @property
    def asc(attr) -> Any: ...
    @property
    def desc(attr) -> Any: ...
    def describe(attr) -> Any: ...

class Optional(Attribute[AttributeType]): ...

class Required(Attribute[AttributeType]):
    def validate(
        attr,
        val: Any,
        obj: Any | None = ...,
        entity: Any | None = ...,
        from_db: bool = ...,
    ) -> Any: ...

class Discriminator(Required[AttributeType]):
    def __init__(attr, py_type: AttributeType, *args: Any, **kwargs: Any) -> None: ...
    @staticmethod
    def create_default_attr(entity: Any) -> None: ...
    def process_entity_inheritance(attr, entity: Any) -> None: ...
    def validate(
        attr,
        val: Any,
        obj: Any | None = ...,
        entity: Any | None = ...,
        from_db: bool = ...,
    ) -> Any: ...
    def load(attr, obj: Any) -> None: ...
    def __get__(attr, obj: Any, cls: Any | None = ...) -> AttributeType: ...
    def __set__(attr, obj: Any, new_val: Any) -> None: ...  # type: ignore
    def db_set(attr, obj: Any, new_dbval: Any) -> None: ...  # type: ignore
    def update_reverse(
        attr, obj: Any, old_val: Any, new_val: Any, undo_funcs: Any
    ) -> None: ...

class Index:
    def __init__(index, *attrs: Any, **options: Any) -> None: ...

def composite_index(*attrs: Any) -> None: ...
def composite_key(*attrs: Any) -> None: ...

class PrimaryKey(Required[AttributeType]):
    def __new__(cls, *args: Any, **kwargs: Any) -> Any: ...

class Collection(Attribute[AttributeType]):
    def __init__(attr, py_type: AttributeType, *args: Any, **kwargs: Any) -> None: ...
    def load(attr, obj: Any) -> None: ...
    def __get__(attr, obj: Any, cls: Any | None = ...) -> Any: ...
    def __set__(attr, obj: Any, val: Any) -> None: ...  # type: ignore
    def __delete__(attr, obj: Any) -> None: ...
    def prepare(attr, obj: Any, val: Any, fromdb: bool = ...) -> None: ...
    def set(attr, obj: Any, val: Any, fromdb: bool = ...) -> None: ...

class SetData(set[Any]):
    def __init__(setdata) -> None: ...

class Set(Collection[AttributeType]):
    def validate(
        attr,
        val: Any,
        obj: Any | None = ...,
        entity: Any | None = ...,
        from_db: bool = ...,
    ) -> Any: ...
    def prefetch_load_all(attr, objects: Any) -> Any: ...
    def load(attr, obj: Any, items: Any | None = ...) -> Any: ...
    def construct_sql_m2m(
        attr, batch_size: int = ..., items_count: int = ...
    ) -> Any: ...
    def copy(attr, obj: Any) -> Any: ...
    def __get__(  # type: ignore
        attr, obj: Any, cls: Any | None = ...
    ) -> SetInstance[AttributeType]: ...
    def __set__(
        attr, obj: Any, new_items: Any, undo_funcs: Any | None = ...
    ) -> None: ...
    def __delete__(attr, obj: Any) -> None: ...
    def reverse_add(attr, objects: Any, item: Any, undo_funcs: Any) -> None: ...
    def db_reverse_add(attr, objects: Any, item: Any) -> None: ...
    def reverse_remove(attr, objects: Any, item: Any, undo_funcs: Any) -> None: ...
    def db_reverse_remove(attr, objects: Any, item: Any) -> None: ...
    def get_m2m_columns(attr, is_reverse: bool = ...) -> Any: ...
    def remove_m2m(attr, removed: Any) -> None: ...
    def add_m2m(attr, added: Any) -> None: ...
    def drop_table(attr, with_all_data: bool = ...) -> None: ...

class SetIterator(Generic[EntityType]):
    def __init__(self, wrapper: EntityType) -> None: ...
    def __iter__(self) -> Any: ...
    def next(self) -> Any: ...
    def __next__(self) -> EntityType: ...

class SetInstance(Generic[EntityType]):
    def __init__(wrapper, obj: Any, attr: Any) -> None: ...
    def __reduce__(wrapper) -> Any: ...
    def copy(wrapper) -> set[EntityType]: ...
    def __nonzero__(wrapper) -> Any: ...
    def is_empty(wrapper) -> bool: ...
    def __len__(wrapper) -> int: ...
    def count(wrapper, distinct: bool = ...) -> int: ...
    def __iter__(wrapper) -> SetIterator[EntityType]: ...
    def __eq__(wrapper, other: Any) -> bool: ...
    def __ne__(wrapper, other: Any) -> bool: ...
    def __add__(wrapper, new_items: Any) -> Any: ...
    def __sub__(wrapper, items: Any) -> Any: ...
    def __contains__(wrapper, item: EntityType) -> bool: ...
    def create(wrapper, **kwargs: Any) -> EntityType: ...
    @overload
    def add(wrapper, item: EntityType) -> None: ...
    @overload
    def add(wrapper, new_items: Iterable[EntityType]) -> None: ...
    def __iadd__(wrapper, items: Any) -> Any: ...
    def remove(wrapper, items: EntityType) -> None: ...
    def __isub__(wrapper, items: Any) -> Any: ...
    def clear(wrapper) -> None: ...
    def load(wrapper) -> None: ...
    @overload
    def select(
        wrapper, callback: Callable[[EntityType], bool]
    ) -> Query[EntityType, EntityType]: ...
    @overload
    def select(wrapper, **kwargs: Any) -> Query[EntityType, EntityType]: ...
    @overload
    def filter(
        wrapper, callback: Callable[[EntityType], bool]
    ) -> Query[EntityType, EntityType]: ...
    @overload
    def filter(wrapper, **kwargs: Any) -> Query[EntityType, EntityType]: ...
    def limit(
        wrapper, limit: Optional[int] = ..., offset: Optional[int] = ...
    ) -> Query[EntityType, EntityType]: ...
    def page(
        wrapper, pagenum: int, pagesize: int = ...
    ) -> Query[EntityType, EntityType]: ...
    @overload
    def order_by(
        wrapper, callback: Callable[[EntityType], Any]
    ) -> Query[EntityType, EntityType]: ...
    @overload
    def order_by(wrapper, *args: Any) -> Query[EntityType, EntityType]: ...
    @overload
    def sort_by(
        wrapper, callback: Callable[[EntityType], Any]
    ) -> Query[EntityType, EntityType]: ...
    @overload
    def sort_by(wrapper, *args: Any) -> Query[EntityType, EntityType]: ...
    def random(wrapper, limit: int) -> Query[EntityType, EntityType]: ...

    # TODO: Somehow figure out attr lifting
    def __getattr__(self, __name: str) -> Any: ...

class Multiset:
    def __init__(multiset, obj: Any, attrnames: Any, items: Any) -> None: ...
    def __reduce__(multiset) -> Any: ...
    def distinct(multiset) -> Any: ...
    def __nonzero__(multiset) -> Any: ...
    def __len__(multiset) -> Any: ...
    def __iter__(multiset) -> Any: ...
    def __eq__(multiset, other: Any) -> Any: ...
    def __ne__(multiset, other: Any) -> Any: ...
    def __contains__(multiset, item: Any) -> Any: ...

EntityType = TypeVar("EntityType")

class EntityIter(Generic[EntityType]):
    entity: EntityType
    def __init__(self, entity: EntityType) -> None: ...
    def next(self) -> None: ...
    def __next__(self) -> EntityType: ...

class EntityMeta(type):
    def __new__(meta, name: Any, bases: Any, cls_dict: Any) -> Any: ...
    def __init__(entity, name: Any, bases: Any, cls_dict: Any) -> None: ...
    def __iter__(entity: Type[EntityType]) -> EntityIter[EntityType]: ...
    def __getitem__(entity: Type[EntityType], key: Any) -> EntityType: ...
    @overload
    def exists(
        entity: Type[EntityType], callback: Callable[[EntityType], bool]
    ) -> bool: ...
    @overload
    def exists(entity, *args: Any, **kwargs: Any) -> bool: ...
    @overload
    def get(
        entity: Type[EntityType], callback: Callable[[EntityType], bool]
    ) -> EntityType: ...
    @overload
    def get(entity: Type[EntityType], **kwargs: Any) -> EntityType: ...
    def get_for_update(
        entity: Type[EntityType], *args: Any, **kwargs: Any
    ) -> EntityType: ...
    def get_by_sql(
        entity: Type[EntityType],
        sql: str,
        globals: Union[dict[str, Any], None] = ...,
        locals: Union[dict[str, Any], None] = ...,
    ) -> EntityType: ...
    @overload
    def select(
        entity: Type[EntityType], callback: Callable[[EntityType], bool]
    ) -> Query[EntityType, EntityType]: ...
    @overload
    def select(
        entity: Type[EntityType], **kwargs: Any
    ) -> Query[EntityType, EntityType]: ...
    def select_by_sql(
        entity: Type[EntityType],
        sql: str,
        globals: Optional[dict[str, Any]] = ...,
        locals: Optional[dict[str, Any]] = ...,
    ) -> list[EntityType]: ...
    def select_random(entity: Type[EntityType], limit: int) -> EntityType: ...
    def describe(entity) -> str: ...
    def drop_table(entity, with_all_data: bool = ...) -> None: ...

def make_proxy(obj: Any) -> Any: ...

class EntityProxy:
    def __init__(self, obj: Any) -> None: ...
    def __getattr__(self, name: Any) -> Any: ...
    def __setattr__(self, name: Any, value: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...

OtherEntity = TypeVar("OtherEntity", bound="Entity")

class Entity(metaclass=EntityMeta):
    def __reduce__(obj) -> Any: ...
    def __init__(obj, *args: Any, **kwargs: Any) -> None: ...
    def get_pk(obj) -> Any: ...
    def __lt__(entity: OtherEntity, other: OtherEntity) -> bool: ...
    def __le__(entity: OtherEntity, other: OtherEntity) -> bool: ...
    def __gt__(entity: OtherEntity, other: OtherEntity) -> bool: ...
    def __ge__(entity: OtherEntity, other: OtherEntity) -> bool: ...
    def load(obj, *attrs: Any) -> None: ...
    def delete(obj) -> None: ...
    def set(obj, **kwargs: Any) -> None: ...
    def find_updated_attributes(obj) -> Any: ...
    def flush(obj) -> None: ...
    def before_insert(obj) -> None: ...
    def before_update(obj) -> None: ...
    def before_delete(obj) -> None: ...
    def after_insert(obj) -> None: ...
    def after_update(obj) -> None: ...
    def after_delete(obj) -> None: ...
    def to_dict(
        obj,
        only: Optional[Union[list[str], str]] = ...,
        exclude: Optional[Union[list[str], str]] = ...,
        with_collections: bool = ...,
        with_lazy: bool = ...,
        related_objects: bool = ...,
    ) -> dict[str, Any]: ...
    def to_json(
        obj,
        include: Any = ...,
        exclude: Any = ...,
        converter: Any | None = ...,
        with_schema: bool = ...,
        schema_hash: Any | None = ...,
    ) -> str: ...

GeneratorReturn = TypeVar("GeneratorReturn")

def select(
    generator: Generator[EntityType, None, GeneratorReturn]
) -> Query[GeneratorReturn, EntityType]: ...
def left_join(*args: Any) -> Any: ...
def get(generator: Iterable[EntityType]) -> EntityType: ...
def exists(
    generator: Iterable[Any],
    globals: Optional[dict[str, Any]] = ...,
    locals: Optional[dict[str, Any]] = ...,
) -> bool: ...
def delete(*args: Any) -> Any: ...
def count(generator: Iterable[Any], distinct: bool = ...) -> int: ...
def sum(generator: Iterable[Any], distinct: bool = ...) -> float: ...
def min(generator: Iterable[Any]) -> Any: ...
def max(generator: Iterable[Any]) -> Any: ...
def avg(generator: Iterable[Any], distinct: bool = ...) -> float: ...

group_concat: Any
distinct: Any

def JOIN(expr: Any) -> Any: ...
def desc(expr: Any) -> Any: ...

QueryType = TypeVar("QueryType")
# We might need to access the Entity type that the query originated from, so
# we let it hang along: https://docs.ponyorm.org/api_reference.html#Query.filter
OriginalQueryType = TypeVar("OriginalQueryType")

class Query(Generic[QueryType, OriginalQueryType]):
    def __init__(
        query,
        code_key: Any,
        tree: Any,
        globals: Any,
        locals: Any,
        cells: Any | None = ...,
        left_join: bool = ...,
    ) -> None: ...
    def __reduce__(query) -> Any: ...
    def get_sql(query) -> str: ...
    def prefetch(query, *args: Any) -> Any: ...
    def show(query, width: Any | None = ..., stream: Any | None = ...) -> None: ...
    def get(query) -> Optional[QueryType]: ...
    def first(query) -> Optional[QueryType]: ...
    def without_distinct(query) -> "Query"[QueryType, OriginalQueryType]: ...
    def distinct(query) -> "Query"[QueryType, OriginalQueryType]: ...
    def exists(query) -> bool: ...
    def delete(query, bulk: Optional[bool] = ...) -> int: ...
    def __len__(query) -> int: ...
    def __iter__(query) -> QueryResultIterator[QueryType]: ...
    @overload
    def order_by(
        query, callback: Callable[[QueryType], bool]
    ) -> "Query"[QueryType, OriginalQueryType]: ...
    @overload
    def order_by(query, *args: Any) -> "Query"[QueryType, OriginalQueryType]: ...
    @overload
    def sort_by(
        query, callback: Callable[[QueryType], bool]
    ) -> "Query"[QueryType, OriginalQueryType]: ...
    @overload
    def sort_by(query, *args: Any) -> "Query"[QueryType, OriginalQueryType]: ...
    @overload
    def filter(
        query, callback: Callable[[QueryType], bool]
    ) -> "Query"[QueryType, OriginalQueryType]: ...
    @overload
    def filter(
        query, **kwargs: Any
    ) -> "Query"[OriginalQueryType, OriginalQueryType]: ...
    @overload
    def where(
        query, callback: Callable[[OriginalQueryType], bool]
    ) -> "Query"[QueryType, OriginalQueryType]: ...
    @overload
    def where(
        query, **kwargs: Any
    ) -> "Query"[OriginalQueryType, OriginalQueryType]: ...
    def __getitem__(query, key: Any) -> QueryResult[QueryType]: ...
    def fetch(
        query, limit: Any | None = ..., offset: Any | None = ...
    ) -> QueryResult[QueryType]: ...
    def limit(
        query, limit: Optional[int] = ..., offset: Optional[int] = ...
    ) -> QueryResult[QueryType]: ...
    def page(query, pagenum: int, pagesize: int = ...) -> QueryResult[QueryType]: ...
    def sum(query, distinct: Optional[bool] = ...) -> float: ...
    def avg(query, distinct: Optional[bool] = ...) -> float: ...
    def group_concat(
        query, sep: Optional[str] = ..., distinct: Optional[bool] = ...
    ) -> str: ...
    def min(query) -> QueryType: ...
    def max(query) -> QueryType: ...
    def count(query, distinct: Optional[bool] = ...) -> int: ...
    def for_update(
        query, nowait: bool = ..., skip_locked: bool = ...
    ) -> "Query"[QueryType, OriginalQueryType]: ...
    def random(query, limit: int) -> Query[QueryType, OriginalQueryType]: ...
    def to_json(
        query,
        include: Any = ...,
        exclude: Any = ...,
        converter: Any | None = ...,
        with_schema: bool = ...,
        schema_hash: Any | None = ...,
    ) -> str: ...

class QueryResultIterator(Generic[QueryType]):
    def __init__(self, query_result: Any) -> None: ...
    def next(self) -> Any: ...
    def __next__(self) -> QueryType: ...
    def __length_hint__(self) -> Any: ...

class QueryResult(Generic[QueryType]):
    def __init__(
        self, query: QueryType, limit: int, offset: int, lazy: bool
    ) -> None: ...
    def __iter__(self) -> QueryResultIterator[QueryType]: ...
    def __len__(self) -> Any: ...
    def __getitem__(self, key: Any) -> QueryType: ...
    def __contains__(self, item: QueryType) -> bool: ...
    def index(self, item: QueryType) -> int: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __lt__(self, other: Any) -> Any: ...
    def __le__(self, other: Any) -> Any: ...
    def __gt__(self, other: Any) -> Any: ...
    def __ge__(self, other: Any) -> Any: ...
    def __reversed__(self) -> Any: ...
    def reverse(self) -> None: ...
    def sort(self, *args: Any, **kwargs: Any) -> None: ...
    def shuffle(self) -> None: ...
    def show(self, width: Any | None = ..., stream: Any | None = ...) -> Any: ...
    def to_json(
        self,
        include: Any = ...,
        exclude: Any = ...,
        converter: Any | None = ...,
        with_schema: bool = ...,
        schema_hash: Any | None = ...,
    ) -> str: ...
    def __add__(self, other: Any) -> Any: ...
    def __radd__(self, other: Any) -> Any: ...
    def to_list(self) -> list[QueryType]: ...
    __setitem__: Any
    __delitem__: Any
    __iadd__: Any
    __imul__: Any
    __mul__: Any
    __rmul__: Any
    append: Any
    clear: Any
    extend: Any
    insert: Any
    pop: Any
    remove: Any

def show(entity: Any) -> None: ...
