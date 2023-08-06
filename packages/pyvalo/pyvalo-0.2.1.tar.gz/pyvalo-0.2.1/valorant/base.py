from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Any


class ValorantBase(metaclass=ABCMeta):

    def __init__(self, **kwargs):
        self._tesseract = kwargs['tesseract']
        self._check_money_pos = kwargs['check_money_pos']
        self._check_buy_phase = kwargs['check_buy_phase']
        self._enemy_score_info = kwargs['enemy_score_info']
        self._own_score_info = kwargs['own_score_info']
        self._time_left_pos = kwargs['time_left_pos']
        self._failsafe = kwargs['failsafe']
    #
    # def __repr__(self):
    #     return 'Tesseract Path: {self._tesseract} \n check_money_pos: {self._check_money_pos} \n'\
    #         'check_buy_phase Path: {self._check_buy_phase} \n enemy_score_info: {self._enemy_score_info} \n' \
    #         'own_score_info Path: {self._own_score_info} \n time_left_pos: {self._time_left_pos} \n' \
    #         'failsafe Path: {self._failsafe}\n' \
    #         .format(self=self)

    @property
    def tesseract(self):
        return self._tesseract

    @property
    def check_money_pos(self):
        return self._check_money_pos

    @property
    def buy_phase_coor(self):
        return self._check_buy_phase

    @property
    def enemy_info_coor(self):
        return self._enemy_score_info

    @property
    def own_info_coor(self):
        return self._own_score_info

    @property
    def time_left_coor(self):
        return self._time_left_pos


    def _read_config_file(self, config):
        """
        Read config file for setup
        :return:
        """
        pass

    def config(self, **kwargs):
        config = kwargs.copy()
        self._read_config_file(config)


