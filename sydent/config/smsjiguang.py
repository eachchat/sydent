from configparser import ConfigParser
from typing import Dict, List

from sydent.config import SMSConfig
from sydent.config.exceptions import ConfigError


class JGSMSConfig(SMSConfig):
    def __init__(self):
        self.originators: Dict[str, List[Dict[str, str]]] = {}
        self.smsRules = {}
        self.appkey = None
        self.master_secret = None
        self.temp_id = None
        self.sign_id = None

    def parse_config(self, cfg: "ConfigParser") -> bool:
        self.appkey = cfg.get("sms", "jiguang.appkey").encode("UTF-8")
        self.master_secret = cfg.get("sms", "jiguang.master_secret").encode("UTF-8")
        self.temp_id = cfg.getint("sms", "jiguang.temp_id")
        self.sign_id = cfg.getint("sms", "jiguang.sign_id")
        self.body_template = cfg.get("sms", "body_template")

        for opt in cfg.options("sms"):
            if opt.startswith("originators."):
                country = opt.split(".")[1]
                rawVal = cfg.get("sms", opt)
                rawList = [i.strip() for i in rawVal.split(",")]

                self.originators[country] = []
                for origString in rawList:
                    parts = origString.split(":")
                    if len(parts) != 2:
                        raise ConfigError(
                            "Originators must be in form: long:<number>, short:<number> or alpha:<text>, separated by commas"
                        )
                    if parts[0] not in ["long", "short", "alpha"]:
                        raise ConfigError(
                            "Invalid originator type: valid types are long, short and alpha"
                        )
                    self.originators[country].append(
                        {
                            "type": parts[0],
                            "text": parts[1],
                        }
                    )
            elif opt.startswith("smsrule."):
                country = opt.split(".")[1]
                action = cfg.get("sms", opt)

                if action not in ["allow", "reject"]:
                    raise ConfigError(
                        "Invalid SMS rule action: %s, expecting 'allow' or 'reject'"
                        % action
                    )

                self.smsRules[country] = action

        return False
