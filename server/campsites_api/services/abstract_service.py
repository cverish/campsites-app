from typing import Generic, List, Optional, Tuple, Type, TypeVar

from fastapi import HTTPException
from pydantic import UUID4, BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Query, Session
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from campsites_db.models import Base

ModelType = TypeVar("ModelType", bound=Base)
ModelTypeDTO = TypeVar("ModelTypeDTO", bound=BaseModel)
FilterTypeDTO = TypeVar("FilterTypeDTO", bound=BaseModel)
DistanceTypeDTO = TypeVar("DistanceTypeDTO", bound=BaseModel)


class AbstractService(Generic[ModelType, ModelTypeDTO, FilterTypeDTO, DistanceTypeDTO]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    """
    Function to filter by distance.

    Parameters:
        distance_filters: DistanceTypeDTO (value, units, lat, lon)

    Returns:
        query (Query): sqlalchemy query object with distance filter applied
    """

    def __distance(self, query: Query, distance_filters: DistanceTypeDTO):
        # convert distance to meters
        dis = distance_filters.value
        dis = dis * 1609.344 if distance_filters.units == "mi" else dis * 1000
        # build point
        lat, lon = distance_filters.lat, distance_filters.lon
        point = from_shape(Point(lon, lat), srid=4326)

        query = query.filter(
            func.ST_DistanceSphere(getattr(self.model, "geo"), point) < dis
        )
        return query

    """
    Takes in a sqlalchemy Query object and a filter object. Removes filters with
    a None value and applies filters depending on type.

    The name of the filters may contain a modifier at the end, preceded with two
    underscores. Allowed modifiers:
        __lt: filter by values less than or equal to a given value
        __gt: filter by values greater than or equal to a given value
        __ct: filter by string values containing given substring

    Filter names (not including modifier with underscores) must exactly match the column name.
    The only exception to this is the `distance` filter, of type DistanceDTO, containing the
    values (value, units, lat, lon), used by the __distance function to filter by distance
    from a given point.

    Parameters:
        query (Query): sqlalchemy query object
        filters (FilterTypeDTO): filter object

    Returns:
        query (Query): sqlalchemy query object with filters applied
    """

    def __filter(self, query: Query, filters: FilterTypeDTO) -> Query:
        # keys to exclude (sorting and pagination)
        excluded_keys = ["offset", "limit", "sort_by", "sort_dir"]
        for name in filters:
            if filters[name] is not None:
                if name in excluded_keys:
                    continue
                if name[-4:] == "__lt":
                    # greater than query
                    query = query.filter(
                        getattr(self.model, name[:-4]) <= filters[name]
                    )
                elif name[-4:] == "__gt":
                    # less than query
                    query = query.filter(
                        getattr(self.model, name[:-4]) >= filters[name]
                    )
                elif name[-4:] == "__ct":
                    query = query.filter(
                        func.lower(getattr(self.model, name[:-4])).contains(
                            filters[name].lower()
                        )
                    )
                elif name == "distance":
                    query = self.__distance(query, filters[name])
                elif isinstance(filters[name], list):
                    query = query.filter(getattr(self.model, name).in_(filters[name]))
                else:
                    query = query.filter(getattr(self.model, name) == filters[name])
        return query

    """
    Function to get a single item by UUID. Raises a 404 HTTP exception
    if item was not found.

    Parameters:
        id (UUID4): UUID of item

    Returns:
        item (ModelType): item with given UUID4
    """

    def get(self, id: UUID4) -> ModelType:
        item: Optional[ModelType] = (
            self.session.query(self.model).filter_by(id=id).first()
        )
        if item is None:
            self.session.rollback()
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        return item

    """
    Function to list items based on applied filters. Returns a tuple containing the list
    of items, limited by the page size and page, and the number of total items based on
    applied filters.

    Parameters:
        filters (FilterTypeDTO): object with filters to apply.
            These filters have a specific format, highlighted in the function
            description for `__filter()`

    Returns:
        result (List[ModelType]), num_total_results (int): a tuple containing the
            list of items and the number of total items
    """

    def list(self, filters: FilterTypeDTO) -> Tuple[List[ModelType], int]:
        try:
            query = self.session.query(self.model)
            query = self.__filter(query, filters)
            query = query.order_by(
                getattr(getattr(self.model, filters["sort_by"]), filters["sort_dir"])()
            )
            num_total_results = query.count()
            query = query.limit(filters["limit"])
            query = query.offset(filters["offset"])
            result: List[ModelTypeDTO] = query.all()
            return result, num_total_results
        except Exception as e:
            self.session.rollback()
            raise e

    """
    Function to add an instance of the item to the database. Takes in the
    item, adds it to the database, and returns the item with its assigned UUID.
    If the item cannot be created, a 422 HTTP exception is thrown.

    Parameters:
        item (ModelTypeDTO): object to be added to the database, in DTO format.

    Returns:
        item (ModelType): object that has been added to the database
    """

    def create(self, item: ModelTypeDTO) -> ModelType:
        item: ModelType = self.model(**item.model_dump())
        self.session.add(item)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise HTTPException(status_code=422, detail="Item could not be created.")
        return item

    """
    Function to add multiple items to the database. Takes in a list of
    items and adds them to the database. Does not return the items, as the list could be
    large.

    If an issue is encountered while adding items, a 422 HTTP exception is thrown.

    Parameters:
        items (List[ModelTypeDTO]): objects to be added to the database, in DTO format.
    """

    def bulk_create(self, items: List[ModelTypeDTO]) -> None:
        items: List[ModelType] = [self.model(**item.model_dump()) for item in items]
        self.session.add_all(items)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise HTTPException(status_code=422, detail="Items could not be created.")

    """
    Function to update the values for an item. Takes in the UUID of the item as well
    as the full item object in DTO format, containing new values. Returns the edited item.
    Raises a 404 HTTP exception if an item with the given UUID does not exist.

    Parameters:
        id (UUID4): the UUID of the item
        item (ModelTypeDTO): new object to overwrite in the database

    Returns:
        db_item (ModelType): the edited item
    """

    def update(self, id: UUID4, item: ModelTypeDTO) -> ModelType:
        db_item = self.get(id)
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        for key, value in item.model_dump().items():
            # we want to ensure we are not overwriting the ID
            if key != "id":
                setattr(db_item, key, value)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        return db_item

    """
    Function to delete an item by UUID. Takes in the UUID of the item and removes it from
    the database.

    Parameters:
        id (UUID4): the UUID of the item
    """

    def delete(self, id: UUID4) -> None:
        item = self.session.query(self.model).filter_by(id=id).first()
        if item is None:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        try:
            self.session.delete(item)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
