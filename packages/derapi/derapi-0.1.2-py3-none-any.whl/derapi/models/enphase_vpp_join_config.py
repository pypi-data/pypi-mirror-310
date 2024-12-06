from typing import TYPE_CHECKING, Any, Dict, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.enphase_join_config_inline_credentials import EnphaseJoinConfigInlineCredentials
    from ..models.enphase_vpp_join_config_inline_credentials import EnphaseVPPJoinConfigInlineCredentials
    from ..models.stored_credentials_reference import StoredCredentialsReference


T = TypeVar("T", bound="EnphaseVPPJoinConfig")


@_attrs_define
class EnphaseVPPJoinConfig:
    """
    Attributes:
        vendor (Literal['enphasevpp']):  Default: 'enphasevpp'.
        credentials (Union['EnphaseVPPJoinConfigInlineCredentials', 'StoredCredentialsReference']):
        partner_app_credentials (Union['EnphaseJoinConfigInlineCredentials', 'StoredCredentialsReference']):
        program_id (str):
    """

    credentials: Union["EnphaseVPPJoinConfigInlineCredentials", "StoredCredentialsReference"]
    partner_app_credentials: Union["EnphaseJoinConfigInlineCredentials", "StoredCredentialsReference"]
    program_id: str
    vendor: Literal["enphasevpp"] = "enphasevpp"

    def to_dict(self) -> Dict[str, Any]:
        from ..models.enphase_join_config_inline_credentials import EnphaseJoinConfigInlineCredentials
        from ..models.enphase_vpp_join_config_inline_credentials import EnphaseVPPJoinConfigInlineCredentials

        vendor = self.vendor

        credentials: Dict[str, Any]
        if isinstance(self.credentials, EnphaseVPPJoinConfigInlineCredentials):
            credentials = self.credentials.to_dict()
        else:
            credentials = self.credentials.to_dict()

        partner_app_credentials: Dict[str, Any]
        if isinstance(self.partner_app_credentials, EnphaseJoinConfigInlineCredentials):
            partner_app_credentials = self.partner_app_credentials.to_dict()
        else:
            partner_app_credentials = self.partner_app_credentials.to_dict()

        program_id = self.program_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "vendor": vendor,
                "credentials": credentials,
                "partnerAppCredentials": partner_app_credentials,
                "programID": program_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.enphase_join_config_inline_credentials import EnphaseJoinConfigInlineCredentials
        from ..models.enphase_vpp_join_config_inline_credentials import EnphaseVPPJoinConfigInlineCredentials
        from ..models.stored_credentials_reference import StoredCredentialsReference

        d = src_dict.copy()
        vendor = cast(Literal["enphasevpp"], d.pop("vendor"))
        if vendor != "enphasevpp":
            raise ValueError(f"vendor must match const 'enphasevpp', got '{vendor}'")

        def _parse_credentials(
            data: object,
        ) -> Union["EnphaseVPPJoinConfigInlineCredentials", "StoredCredentialsReference"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                credentials_type_0 = EnphaseVPPJoinConfigInlineCredentials.from_dict(data)

                return credentials_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            credentials_type_1 = StoredCredentialsReference.from_dict(data)

            return credentials_type_1

        credentials = _parse_credentials(d.pop("credentials"))

        def _parse_partner_app_credentials(
            data: object,
        ) -> Union["EnphaseJoinConfigInlineCredentials", "StoredCredentialsReference"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_enphase_join_config_credentials_type_0 = EnphaseJoinConfigInlineCredentials.from_dict(
                    data
                )

                return componentsschemas_enphase_join_config_credentials_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_enphase_join_config_credentials_type_1 = StoredCredentialsReference.from_dict(data)

            return componentsschemas_enphase_join_config_credentials_type_1

        partner_app_credentials = _parse_partner_app_credentials(d.pop("partnerAppCredentials"))

        program_id = d.pop("programID")

        enphase_vpp_join_config = cls(
            vendor=vendor,
            credentials=credentials,
            partner_app_credentials=partner_app_credentials,
            program_id=program_id,
        )

        return enphase_vpp_join_config
