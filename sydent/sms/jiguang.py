import logging
from base64 import b64encode
from typing import TYPE_CHECKING, Dict, Optional, cast

from twisted.web.http_headers import Headers

from sydent.http.httpclient import SimpleHttpClient
from sydent.sms.openmarket import OpenMarketSMS
from sydent.types import JsonDict

if TYPE_CHECKING:
    from sydent.sydent import Sydent

logger = logging.getLogger(__name__)

API_BASE_URL = "https://api.sms.jpush.cn/v1/messages"


class JGSMS(OpenMarketSMS):
    def __init__(self, sydent: "Sydent") -> None:
        self.sydent = sydent
        self.http_cli = SimpleHttpClient(sydent)
        self.auth = b64encode(b"%s:%s" % (sydent.config.sms.appkey, sydent.config.sms.master_secret))

    async def sendTextSMS(
            self, body: str, dest: str, source: Optional[Dict[str, str]] = None
    ) -> None:
        if dest.startswith("86"):
            dest = dest[2:]  # remove country code

        logger.info("Sending SMS notification to %s with code %s." % (dest, body))

        send_body = {
            "mobile": dest,
            "sign_id": self.sydent.config.sms.sign_id,
            "temp_id": self.sydent.config.sms.temp_id,
            "temp_para": {
                "code": body,
            }
        }

        req_headers = Headers(
            {
                b"Authorization": [b"Basic " + self.auth],
                b"Content-Type": [b"application/json"],
            }
        )

        resp, response_body = await self.http_cli.post_json_maybe_get_json(
            API_BASE_URL, cast(JsonDict, send_body), {"headers": req_headers}
        )

        if resp.code == 200:
            logger.info("Send SMS notification success, Jiguang push response: %s." % response_body)
        else:
            logger.error("Failed to send SMS notification, Jiguang push response: %s." % response_body)
            raise Exception(response_body["error"]["message"])
