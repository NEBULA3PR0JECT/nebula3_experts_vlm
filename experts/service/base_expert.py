from abc import ABC, abstractmethod
from asyncio import constants
from typing import Optional
from fastapi import FastAPI
from threading import Lock
import logging
from experts.common.defines import *
import sys
sys.path.insert(0, 'experts/')
sys.path.insert(0, 'nebula3_experts/nebula3_pipeline/nebula3_database/')
sys.path.insert(0, 'nebula3_experts/nebula3_pipeline/')
from common.defines import *
from experts.common.constants import OUTPUT

import sys
sys.path.insert(0, 'experts/')
sys.path.insert(0, 'nebula3_pipeline/nebula3_database/')
sys.path.insert(0, 'nebula3_pipeline/')
from nebula3_pipeline.nebula3_database.movie_db import MOVIE_DB
from nebula3_pipeline.nebula3_database.movie_s3 import MOVIE_S3
# from nebula3_pipeline.nebula3_database.movie_tokens import MovieTokens


class BaseExpert(ABC):
    def __init__(self):
        self.movie_db = MOVIE_DB()
        self.db = self.movie_db.db
        self.movie_s3 = MOVIE_S3()
        # self.movie_tokens = MovieTokens(self.db)
        self.status = ExpertStatus.STARTING
        self.tasks_lock = Lock()
        self.tasks = dict()


    def set_logger(self, logger: logging.Logger):
        self.logger = logger

    def log_debug(self, msg):
        if self.logger:
            self.logger.debug(msg)
        else:
            print(msg)

    def log_info(self, msg):
        if self.logger:
            self.logger.info(msg)
        else:
            print(msg)

    def log_error(self, msg):
        if self.logger:
            self.logger.error(msg)
        else:
            print(msg)

    def set_active(self):
        """ setting the expert status to active"""
        self.status = ExpertStatus.ACTIVE

    def add_task(self, task_id: str,  taks_params = dict()):
        with self.tasks_lock:
            self.tasks[task_id] = taks_params

    def remove_task(self, task_id: str):
        with self.tasks_lock:
            self.tasks.pop(task_id)

    @abstractmethod
    def add_expert_apis(self, app: FastAPI):
        """add expert's specific apis (REST)

        Args:
            app (FastAPI): _description_
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """return expert's name
        """
        pass

    # @abstractmethod
    def get_status(self) -> str:
        """return expert's status
        """
        return self.status.name

    @abstractmethod
    def get_cfg(self) -> str:
        """return expert's config params
        """
        pass

    # @abstractmethod
    def get_tasks(self) -> list:
        """ return the taks currently running """
        current_tasks = list()
        with self.tasks_lock:
            for id, info in self.tasks.items:
                current_tasks.append({ 'id': id, 'info': info })
        return current_tasks

    @abstractmethod
    def get_dependency(self) -> str:
        """return the expert's dependency in the pipeline:
        which pipeline step is this expert depends on
        pass

        Returns:
            str: _description_
        """
        pass

    # @abstractmethod
    def handle_msg(self, msg_params):
        """handling msg: going over the movies and calling predict on each one
        Args:
            msg_params (_type_): _description_
        """
        output = OutputStyle.DB if not msg_params[constants.OUTPUT] else msg_params[constants.OUTPUT]
        movies = msg_params[constants.MOVIES]
        if isinstance(movies, list):
            for movie_id in movies:
                self.predict(movie_id, output)

    @abstractmethod
    def predict(self, movie_id, output: OutputStyle):
        """ handle new movie """
        pass


    @abstractmethod
    def handle_exit(self):
        """handle things before exit process
        """
        pass