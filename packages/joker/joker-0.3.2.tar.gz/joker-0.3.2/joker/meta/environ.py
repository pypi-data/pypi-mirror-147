#!/usr/bin/env python3
# coding: utf-8

import os
from functools import cached_property

import volkanic.environ
from volkanic.utils import (
    under_home_dir,
    abs_path_join,
    abs_path_join_and_mkdirs,
)


packages = [
    'joker.aligner',
    'joker.broker',
    'joker.cast',
    'joker.meta',
    'joker.flasky',
    'joker.geometry',
    'joker.masquerade',
    'joker.minions',
    'joker.pyoneliner',
    'joker.relational',
    'joker.scraper',
    'joker.stream',
    'joker.studio',
    'joker.textmanip',
    'joker.xopen'
]

projects = [
    'joker-aligner',
    'joker-broker',
    'joker-cast',
    'joker',
    'joker-flasky',
    'joker-geometry',
    'joker-masquerade',
    'joker-minions',
    'joker-pyoneliner',
    'joker-relational',
    'joker-scraper',
    'joker-stream',
    'joker-studio',
    'joker-textmanip',
    'joker-xopen'
]


def _get_joker_packages():
    import pkg_resources
    _packages = []
    for pkg in pkg_resources.working_set:
        pn = pkg.project_name
        if pn.startswith('joker-') or pn == 'joker':
            _packages.append(pkg)
    return _packages


def _get_joker_packages_with_pkgutil():
    import pkgutil
    import joker
    # https://stackoverflow.com/a/57873844/2925169
    return list(pkgutil.iter_modules(
        joker.__path__,
        joker.__name__ + "."
    ))


# this is deprecated
class GlobalInterface(volkanic.environ.GlobalInterfaceTrial):
    package_name = 'joker.meta'


class JokerInterface(GlobalInterface):
    package_name = 'joker.meta'
    default_config = {}

    def under_temp_dir(self, ext=''):
        name = os.urandom(17).hex() + ext
        return self.under_data_dir('tmp', name, mkdirs=True)

    @cached_property
    def jinja2_env(self):
        # noinspection PyPackageRequirements
        from jinja2 import Environment, PackageLoader, select_autoescape
        return Environment(
            loader=PackageLoader(self.package_name, 'templates'),
            autoescape=select_autoescape(['html', 'xml']),
        )

    @classmethod
    def under_joker_dir(cls, *paths, mkdirs=False):
        base_dir = os.environ.get('JOKER_HOME') or under_home_dir('.joker')
        if not mkdirs:
            return abs_path_join(base_dir, *paths)
        return abs_path_join_and_mkdirs(base_dir, *paths)

    @classmethod
    def under_joker_subdir(cls, *paths, mkdirs=False):
        _paths = cls.namespaces[1:]
        _paths.extend(paths)
        return cls.under_joker_dir(*_paths, mkdirs=mkdirs)

    @classmethod
    def _get_conf_path_names(cls):
        names = cls.namespaces.copy()
        names.append(cls._get_option('confpath_filename'))
        return names


def get_joker_packages(use_pkgutil=False):
    if use_pkgutil:
        return _get_joker_packages_with_pkgutil()
    else:
        return _get_joker_packages()


def under_joker_dir(*paths):
    ji = JokerInterface()
    return ji.under_joker_dir(*paths)
