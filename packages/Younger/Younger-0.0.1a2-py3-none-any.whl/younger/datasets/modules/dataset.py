#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2023-09-11 08:16
#
# This source code is licensed under the Apache-2.0 license found in the
# LICENSE file in the root directory of this source tree.


import tqdm
import pathlib

from typing import Generator

from younger.commons.io import load_json, save_json
from younger.commons.hash import hash_strings
from younger.commons.logging import logger
from younger.commons.version import semantic_release, str_to_sem

from younger.datasets.modules.stamp import Stamp
from younger.datasets.modules.instance import Instance


class Dataset(object):
    def __init__(
            self,
            instances: list[Instance] | None = None,
            version: semantic_release.Version | None = None
    ) -> None:
        instances = instances or list()
        version = version or str_to_sem('0.0.0')

        self._stamps_filename = 'stamps.json'
        self._stamps: set[Stamp] = set()

        self._uniques_filename = 'uniques.json'
        self._uniques: list[str] = list()

        self._instances_dirname = 'instances'
        self._instances: dict[str, Instance] = dict()

        self.insert_instances(instances)
        self.release(version)

    @property
    def uniques(self) -> list[str]:
        return self._uniques

    @property
    def instances(self) -> dict[str, Instance]:
        return self._instances

    @property
    def latest_version(self) -> semantic_release.Version:
        latest_version = str_to_sem('0.0.0')
        for stamp in self._stamps:
            latest_version = max(latest_version, stamp.version)
        return latest_version

    @property
    def checksum(self) -> str:
        exact_uniques = list()
        for unique in self._uniques:
            instance = self._instances[unique]
            if instance.meta.is_release:
                exact_uniques.append(instance.unique)
        return hash_strings(exact_uniques)

    def load(self, dataset_dirpath: pathlib.Path) -> None:
        assert dataset_dirpath.is_dir(), f'There is no \"Dataset\" can be loaded from the specified directory \"{dataset_dirpath.absolute()}\".'
        logger.info(f' = [YBD] = Loading Dataset @ {dataset_dirpath}...')
        stamps_filepath = dataset_dirpath.joinpath(self._stamps_filename)
        self._load_stamps(stamps_filepath)
        uniques_filepath = dataset_dirpath.joinpath(self._uniques_filename)
        self._load_uniques(uniques_filepath)
        instances_dirpath = dataset_dirpath.joinpath(self._instances_dirname)
        self._load_instances(instances_dirpath)
        return

    def save(self, dataset_dirpath: pathlib.Path) -> None:
        assert not dataset_dirpath.is_dir(), f'\"Dataset\" can not be saved into the specified directory \"{dataset_dirpath.absolute()}\".'
        logger.info(f' = [YBD] = Saving Dataset @ {dataset_dirpath}...')
        stamps_filepath = dataset_dirpath.joinpath(self._stamps_filename)
        self._save_stamps(stamps_filepath)
        uniques_filepath = dataset_dirpath.joinpath(self._uniques_filename)
        self._save_uniques(uniques_filepath)
        instances_dirpath = dataset_dirpath.joinpath(self._instances_dirname)
        self._save_instances(instances_dirpath)
        return

    def _load_stamps(self, stamps_filepath: pathlib.Path) -> None:
        assert stamps_filepath.is_file(), f'There is no \"Stamp\"s can be loaded from the specified path \"{stamps_filepath.absolute()}\".'
        stamps = load_json(stamps_filepath)
        self._stamps = set()
        for stamp in stamps:
            self._stamps.add(Stamp(**stamp))
        return

    def _save_stamps(self, stamps_filepath: pathlib.Path) -> None:
        assert not stamps_filepath.is_file(), f'\"Stamp\"s can not be saved into the specified path \"{stamps_filepath.absolute()}\".'
        stamps = list()
        for stamp in self._stamps:
            stamps.append(stamp.dict)
        save_json(stamps, stamps_filepath)
        return

    def _load_uniques(self, uniques_filepath: pathlib.Path) -> None:
        assert uniques_filepath.is_file(), f'There is no \"Unique\"s can be loaded from the specified path \"{uniques_filepath.absolute()}\".'
        self._uniques = load_json(uniques_filepath)
        assert isinstance(self._uniques, list), f'Wrong type of the \"Unique\"s, should be \"{type(list())}\" instead \"{type(self._uniques)}\"'
        return

    def _save_uniques(self, uniques_filepath: pathlib.Path) -> None:
        assert not uniques_filepath.is_file(), f'\"Unique\"s can not be saved into the specified path \"{uniques_filepath.absolute()}\".'
        assert isinstance(self._uniques, list), f'Wrong type of the \"Unique\"s, should be \"{type(list())}\" instead \"{type(self._uniques)}\"'
        save_json(self._uniques, uniques_filepath)
        return

    def _load_instances(self, instances_dirpath: pathlib.Path) -> None:
        assert instances_dirpath.is_dir(), f'There is no \"Instance\"s can be loaded from the specified directory \"{instances_dirpath.absolute()}\".'
        logger.info(f' = [YBD] = Loading Instances ...')
        for index, unique in enumerate(self._uniques):
            logger.info(f' = [YBD] = No.{index} Instance: {unique}')
            instance_dirpath = instances_dirpath.joinpath(f'{index}-{unique}')
            self._instances[unique] = Instance()
            self._instances[unique].load(instance_dirpath)
        return

    def _save_instances(self, instances_dirpath: pathlib.Path) -> None:
        assert not instances_dirpath.is_dir(), f'\"Instance\"s can not be saved into the specified directory \"{instances_dirpath.absolute()}\".'
        logger.info(f' = [YBD] = Saving Instances ...')
        for index, unique in enumerate(self._uniques):
            logger.info(f' = [YBD] = No.{index+1} Instance: {unique}')
            instance_dirpath = instances_dirpath.joinpath(f'{index}-{unique}')
            instance = self._instances[unique]
            instance.save(instance_dirpath)
        return

    def acquire(self, version: semantic_release.Version) -> 'Dataset':
        logger.info(f' = [YBD] = Acquiring Dataset: version = {version}...')
        dataset = Dataset()
        for index, unique in enumerate(self._uniques):
            instance = self._instances[unique]
            if (instance.meta.release and instance.meta.release_version <= version) and (not instance.meta.retired or version < instance.meta.retired_version):
                logger.info(f' = [YBD] = Acquired No.{index+1} Instance: {unique}')
                dataset.insert(instance)
        dataset.release(version=version)
        return dataset

    def check(self) -> None:
        assert len(self._uniques) == len(self._instances), f'The number of \"Instance\"s does not match the number of \"Unique\"s.'
        for unique in self._uniques:
            instance = self._instances[unique]
            assert unique == instance.unique, f'The \"Unique={instance.unique}\" of \"Instance\" does not match \"Unique={unique}\" '
        return

    def insert(self, instance: Instance) -> bool:
        # Insert only instances that do not belong to any dataset.
        assert isinstance(instance, Instance), f'Argument \"instance\"must be an \"Instance\" instead \"{type(instance)}\"!'
        if instance.unique is None:
            return False
        else:
            if instance.unique in self._instances:
                return False
            else:
                self._instances[instance.unique] = instance
                return self._instances[instance.unique].insert()

    def delete(self, instance: Instance) -> bool:
        # Delete only the instances within the dataset.
        assert isinstance(instance, Instance), f'Argument \"instance\"must be an \"Instance\" instead \"{type(instance)}\"!'
        if instance.unique is None:
            return False
        else:
            if instance.unique in self._instances:
                instance = self._instances[instance.unique]
                return instance.delete()
            else:
                return False

    def insert_instances(self, instances: list[Instance]) -> int:
        flags = list()
        for instance in instances:
            flags.append(self.insert(instance))
        return sum(flags)

    def delete_instances(self, instances: list[Instance]) -> int:
        flags = list()
        for instance in instances:
            flags.append(self.delete(instance))
        return sum(flags)

    def release(self, version: semantic_release.Version) -> None:
        if version == str_to_sem('0.0.0'):
            return
        assert self.latest_version < version, (
            f'Version provided less than or equal to the latest version:\n'
            f'Provided: {version}\n'
            f'Latest: {self.latest_version}'
        )

        for unique, instance in self._instances.items():
            if instance.meta.is_external:
                if instance.meta.is_new:
                    self._uniques.append(unique)
                if instance.meta.is_old:
                    self._instances.pop(unique)
            instance.release(version)

        stamp = Stamp(
            str(version),
            self.checksum,
        )
        if stamp in self._stamps:
            return
        else:
            self._stamps.add(stamp)
        return

    @classmethod
    def load_instances(cls, dataset_dirpath: pathlib.Path | str) -> Generator[Instance, None, None]:
        dataset_dirpath = pathlib.Path(dataset_dirpath) if isinstance(dataset_dirpath, str) else dataset_dirpath

        instance_dirpaths = list(dataset_dirpath.iterdir())
        with tqdm.tqdm(total=len(instance_dirpaths), desc='Processing Instance') as progress_bar:
            for instance_dirpath in instance_dirpaths:
                instance = Instance()
                try:
                    instance.load(instance_dirpath)
                    yield instance
                except:
                    continue
                progress_bar.update(1)