import enum

from typing import Any
from typing import Dict
from typing import Type

from typing import Annotated
from typing import get_args

from sqlalchemy import types
from sqlalchemy.types import TypeEngine

import datetime
import decimal
import uuid


class ServiceLogStatus(enum.Enum):
    START = "start"
    FINISH = "finish"


# QueryIdType = QueryIdMapType.PythonType
# MessageGroupIdType = MessageGroupIdMapType.PythonType
# ServiceIdType = ServiceIdMapType.PythonType
# ServiceErrorIdType = ServiceErrorIdMapType.PythonType
# RejectionIdType = ServiceRejectionIdMapType.PythonType
# LogIdType = LogIdMapType.PythonType
# BlackListType = BlackListMapType.PythonType


################################################################################

# Annotated types:
# https://django.fun/docs/sqlalchemy/2.0/orm/declarative_tables/#mapping
# -multiple-type-configurations-to-python-types

# Text = Annotated[
#     str,
#     types.Text(),
#     "text"
# ]
# QueryId = Annotated[int, types.Integer(), "query_id"]
# CustomerId = Annotated[str, types.Text(), "customer_id"]
# ClientId = Annotated[str, types.Text(), "client_id"]
# ChannelId = Annotated[str, types.Text(), "channel_id"]
# BlackList = Annotated[list[str], types.ARRAY(types.Text()), "black_list"]
# MessageGroupId = Annotated[int, types.Integer(), "message_group_id"]
# Attitude = Annotated[str, types.Text(), "attitude"]
# CorporateOfferFile = Annotated[str, types.Text(), "corporate_offer_file"]
# ServiceId = Annotated[int, types.Integer(), "service_id"]
# ServiceErrorId = Annotated[int, types.Integer(), "service_error_id"]
# ServiceRejectionId = Annotated[int, types.Integer(), "service_rejection_id"]
# LogId = Annotated[int, types.Integer(), "log_id"]
# MessageDatetime = Annotated[
#     datetime.datetime,
#     types.DateTime(),
#     "message_datetime"
# ]

Text = Annotated[
    str,
    types.Text(),
]
FilePath = Annotated[
    str,
    types.Text(),
]
QueryId = Annotated[
    int,
    types.Integer(),
]
CustomerId = Annotated[
    str,
    types.Text(),
]
ClientId = Annotated[
    str,
    types.Text(),
]
CsvId = Annotated[
    int,
    types.Integer(),
]
ChannelId = Annotated[
    str,
    types.Text(),
]
CustomerBlackList = Annotated[
    list[str],
    types.ARRAY(types.Text()),
]
CustomerTags = Annotated[
    list[str],
    types.ARRAY(types.Text()),
]
CustomerWhiteList = Annotated[
    list[str],
    types.ARRAY(types.Text()),
]
CustomerFeatures = Annotated[
    list[str],
    types.ARRAY(types.Text()),
]
MessageGroupId = Annotated[
    int,
    types.Integer(),
]
Attitude = Annotated[
    str,
    types.Text(),
]
ServiceId = Annotated[
    int,
    types.Integer(),
]
ServiceErrorId = Annotated[
    int,
    types.Integer(),
]
ServiceRejectionId = Annotated[
    int,
    types.Integer(),
]
LogId = Annotated[
    int,
    types.Integer(),
]
MessageDatetime = Annotated[
    datetime.datetime,
    types.DateTime(),
]


def get_db_type(annotated_type):
    return get_args(annotated_type)[1]


# default type mapping, deriving the type for mapped_column()
# from a Mapped[] annotation
type_map: Dict[Type[Any], TypeEngine[Any]] = {
    # Default
    bool: types.Boolean(),
    bytes: types.LargeBinary(),
    datetime.date: types.Date(),
    datetime.datetime: types.DateTime(),
    datetime.time: types.Time(),
    datetime.timedelta: types.Interval(),
    decimal.Decimal: types.Numeric(),
    float: types.Float(),
    int: types.Integer(),
    str: types.String(),
    uuid.UUID: types.Uuid(),

    # Custom
    Text: get_db_type(Text),
    FilePath: get_db_type(FilePath),
    QueryId: get_db_type(QueryId),
    CustomerId: get_db_type(CustomerId),
    ClientId: get_db_type(ClientId),
    CsvId: get_db_type(CsvId),
    ChannelId: get_db_type(ChannelId),
    CustomerBlackList: get_db_type(CustomerBlackList),
    CustomerTags: get_db_type(CustomerTags),
    CustomerWhiteList: get_db_type(CustomerWhiteList),
    CustomerFeatures: get_db_type(CustomerFeatures),
    MessageGroupId: get_db_type(MessageGroupId),
    Attitude: get_db_type(Attitude),
    ServiceId: get_db_type(ServiceId),
    ServiceErrorId: get_db_type(ServiceErrorId),
    ServiceRejectionId: get_db_type(ServiceRejectionId),
    LogId: get_db_type(LogId),
    MessageDatetime: get_db_type(MessageDatetime),

    # Custom
    # TextType: TextType.DBType,
    # QueryIdType: QueryIdType.DBType,
    # MessageGroupIdType: MessageGroupIdType.DBType,
    # CustomerIdType: CustomerIdType.DBType,
    # BlackListType: BlackListType.DBType,
    # ClientIdType: ClientIdType.DBType,
    # AttitudeType: AttitudeType.DBType,
    # CorporateOfferFileType: CorporateOfferFileType.DBType,
    # ServiceIdType: ServiceIdType.DBType,
    # ServiceErrorIdType: ServiceErrorIdType.DBType,
    # ServiceRejectionIdType: ServiceRejectionIdType.DBType,
    # LogIdType: LogIdType.DBType,
    # str: String().with_variant(String(255), "mysql", "mariadb"),
    # bigint: BigInteger()
}
