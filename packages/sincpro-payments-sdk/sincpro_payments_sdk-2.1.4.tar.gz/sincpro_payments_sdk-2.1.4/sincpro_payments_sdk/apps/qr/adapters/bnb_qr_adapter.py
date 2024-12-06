"""Res api adapter."""

from enum import StrEnum

from sincpro_payments_sdk.shared.client_api import ClientAPI


class QRRoutes(StrEnum):
    """BNB QR API routes."""

    GENERATE_QR = "/main/getQRWithImageAsync"
    LIST_GENERATED_QR = "/main/getQRByGenerationDateAsync"
    GET_QR_STATUS = "/main/getQRStatusAsync"
    CANCEL_QR = "/main/CancelQRByIdAsync"


class QRBNBApiAdapter(ClientAPI):

    def __init__(self):
        self.ssl = "http://"
        self.host = "test.bnb.com.bo/QRSimple.API/api/v1"
        super().__init__(self.base_url)

    @property
    def base_url(self) -> str:
        """Get the base URL for the CyberSource API."""
        return f"{self.ssl}{self.host}"
