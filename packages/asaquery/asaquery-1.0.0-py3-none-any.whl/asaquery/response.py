from typing import NamedTuple, TypedDict


class AccessTokenResponse(TypedDict):
    access_token: str
    token_type: str
    expires_at: str
    features: list[str]
    organization_id: str
    product_id: str
    deployment_id: str
    expires_in: int


class SessionSettings(TypedDict):
    maxPublicPlayers: int
    allowInvites: bool
    shouldAdvertise: bool
    allowReadById: bool
    allowJoinViaPresence: bool
    allowJoinInProgress: bool
    allowConferenceRoom: bool
    checkSanctions: bool
    allowMigration: bool
    rejoinAfterKick: str
    platforms: None


class SessionAttributesBase(TypedDict):
    MINORBUILDID_s: str
    MODID_l: int
    CUSTOMSERVERNAME_s: str
    ADDRESSDEV_s: str
    ISPRIVATE_l: int
    SERVERPASSWORD_b: bool
    MATCHTIMEOUT_d: float
    DAYTIME_s: str
    SOTFMATCHSTARTED_b: bool
    STEELSHIELDENABLED_l: int
    SERVERUSESBATTLEYE_b: bool
    EOSSERVERPING_l: int
    ALLOWDOWNLOADCHARS_l: int
    OFFICIALSERVER_s: str
    GAMEMODE_s: str
    ADDRESS_s: str
    SEARCHKEYWORDS_s: str
    __EOS_BLISTENING_b: bool
    ALLOWDOWNLOADITEMS_l: int
    LEGACY_l: int
    ADDRESSBOUND_s: str
    SESSIONISPVE_l: int
    __EOS_BUSESPRESENCE_b: bool
    SESSIONNAMEUPPER_s: str
    SERVERPLATFORMTYPE_s: str
    MAPNAME_s: str
    BUILDID_s: str
    SESSIONNAME_s: str


class SessionAttributesOptional(TypedDict, total=False):
    ENABLEDMODSFILEIDS_s: str
    FRIENDLYMAPNAME_s: str
    CLUSTERID_s: str
    ENABLEDMODS_s: str


class SessionAttributes(SessionAttributesBase, SessionAttributesOptional):
    pass


class RawSession(TypedDict):
    deployment: str
    id: str
    bucket: str
    settings: SessionSettings
    totalPlayers: int
    openPublicPlayers: int
    publicPlayers: list
    started: bool
    lastUpdated: str | None
    attributes: SessionAttributes
    owner: str
    ownerPlatformId: str | None


class QueryResponse(TypedDict):
    sessions: list[RawSession]
    count: int


class Session(NamedTuple):
    name: str
    map: str
    password: bool
    numplayers: int
    maxplayers: int
    players: list[str]
    version: str
    raw: RawSession
