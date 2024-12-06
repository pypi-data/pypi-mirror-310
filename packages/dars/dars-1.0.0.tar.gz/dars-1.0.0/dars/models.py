from datetime import date
import pydantic

from dars import datastructs as ds
from dars import (
        config,
        defaults,
        errors,
        )


class AppModel(pydantic.BaseModel):
    settings: config.Settings | None = None
    base: ds.Base = ds.Base.FZ44

    @property
    def base_settings(self) -> pydantic.BaseModel:
        '''Получить текущую конфигурацию для base'''
        if not self.settings:
            raise errors.SettingsUndefinedError
        if self.base == ds.Base.FZ44:
            return self.settings.fz44
        if self.base == ds.Base.FZ223:
            return self.settings.fz223
        raise NotImplementedError


class GetNsiRequestModel(AppModel):
    '''Параметры запроса справочника'''
    nsiCode: str
    nsiKind: ds.NsiKind = ds.NsiKind.ALL
    isHidden: bool | None = False
    prefix: str = ''


class OrganizationModel(pydantic.BaseModel):
    '''Параметры организации'''
    inn: str
    kpp: str
    ogrn: str | None = None


class GetPublicDocsRequestModel(AppModel):
    '''Параметры запроса публичных документов'''
    subsystemtype: str
    regnums: list[str] = []
    organizations: list[OrganizationModel] = []
    monthinfo: date | None = None
    exactdate: date | None = None
    todayinfo: str | None = pydantic.Field(default=None, pattern=r'^\d+-\d+$')
    offsettimezone: str = defaults.TZ
    prefix: str = ''
    jobs: int = 1

    @pydantic.computed_field
    def fromhour(self) -> int:
        if self.todayinfo:
            return int(self.todayinfo.split('-')[0])

    @pydantic.computed_field
    def tohour(self) -> int:
        if self.todayinfo:
            return int(self.todayinfo.split('-')[1])
