from configparser import ConfigParser, NoOptionError

from sydent.config._base import BaseConfig


class HTTPConfig(BaseConfig):
    def parse_config(self, cfg: ConfigParser):
        """
        Parse the http section of the config

        Args:
            cfg (ConfigParser): the configuration to be parsed
        """
        self.client_bind_address = cfg.get("http", "clientapi.http.bind_address")
        self.client_port = cfg.getint("http", "clientapi.http.port")

        # internal port is allowed to be set to an empty string
        self.internal_port = cfg.get("http", "internalapi.http.port")
        if self.internal_port:
            self.internal_port = int(self.internal_port)
            try:
                self.internal_bind_address = cfg.get(
                    "http", "internalapi.http.bind_address"
                )
            except NoOptionError:
                self.internal_bind_address = "::1"

        self.cert_file = cfg.get("http", "replication.https.certfile")
        self.ca_cert_File = cfg.get("http", "replication.https.cacert")

        self.replication_bind_address = cfg.get(
            "http", "replication.https.bind_address"
        )
        self.replication_port = cfg.getint("http", "replication.https.port")

        self.obey_x_forwarded_for = cfg.get("http", "obey_x_forwarded_for")

        self.verify_federation_certs = cfg.getboolean("http", "federation.verifycerts")

        self.verify_response_template = None
        if cfg.has_option("http", "verify_response_template"):
            self.verify_response_template = cfg.get("http", "verify_response_template")

        self.server_http_url_base = cfg.get("http", "client_http_base")

        self.base_replication_urls = {}

        for section in cfg.sections():
            if section.startswith("peer."):
                # peer name is all the characters after 'peer.'
                peer = section[5:]
                if cfg.has_option(section, "base_replication_url"):
                    base_url = cfg.get(section, "base_replication_url")
                    self.base_replication_urls[peer] = base_url