from typing import List, Union

import pytest
from pydantic import BaseModel, Field
from pydantic.fields import Annotated

from raspcuterie.config.schema import AM2302Schema, RelaySwitchSchema, SinusSchema


class UnionField(BaseModel):
    field: Union[SinusSchema, AM2302Schema] = Field(..., discriminator="type")


DevicesUnion = Annotated[
    Union[SinusSchema, AM2302Schema, RelaySwitchSchema], Field(discriminator="type")
]


class UnionList(BaseModel):
    union_list: List[DevicesUnion]


@pytest.fixture
def am2302():
    return dict(type="AM2302", gpio=4, name="Better")


@pytest.fixture
def sinus():
    return dict(type="sinus", name="Some sinus")


@pytest.fixture
def relay():
    return dict(type="relay", name="refrigerator", gpio=4)


def test_am2302_schema(am2302):

    obj = AM2302Schema.parse_obj(am2302)

    assert isinstance(obj, AM2302Schema)


def test_sinus_schema(sinus):
    obj = SinusSchema.parse_obj(sinus)

    assert isinstance(obj, SinusSchema)


def test_relay_schema(relay):
    obj = RelaySwitchSchema.parse_obj(relay)

    assert isinstance(obj, RelaySwitchSchema)
    assert obj.timeout == 10


def test_union(sinus, am2302):

    x = UnionField.parse_obj(dict(field=sinus))

    assert isinstance(x.field, SinusSchema)


def test_union_list(sinus, am2302, relay):

    x = UnionList.parse_obj(dict(union_list=[sinus, am2302, relay]))

    assert isinstance(x.union_list[0], SinusSchema)
    assert isinstance(x.union_list[1], AM2302Schema)
    assert isinstance(x.union_list[2], RelaySwitchSchema)
