#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from models import storage_t

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
        else:
            if not kwargs.get('id'):
                kwargs['id'] = str(uuid.uuid4())
            if kwargs.get('created_at'):
                kwargs['updated_at'] = kwargs[
                    'created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                kwargs['created_at'] = kwargs['updated_at'] = datetime.now()
            if kwargs.get("__class__"):
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        if storage_t == "db":
            if "password" in new_dict:
                del new_dict['password']
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
