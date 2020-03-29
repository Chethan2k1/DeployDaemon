import os
from app.apache.proxyPass import ProxyPass
from app.apache import apache, apache_ssl


class node:
    db_name = ""
    db_username = ""
    db_password = ""
    db_host = "localhost"

    def __init__(self, db_name, db_username, db_password, db_host, httpd_path):
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.db_host = db_host
        self.httpd_path = httpd_path

    def serve(self):
        os.system("npm init")
        os.system("touch .env")
        content = """
        DB_NAME={0}
        DB_USERNAME={1}
        DB_PASSWORD={2}
        DB_HOST={3}
        HTTPD_PATH={4}
        """
        f = open(".env", "w")
        f.write(
            content.format(
                self.db_name,
                self.db_username,
                self.db_password,
                self.db_host,
                self.httpd_path,
            )
        )
        f.close()
        os.system("npm install apache --save")
        os.system("mv server_example.js server.js")
        os.system("node server.js")

    def host(
        self,
        ssh,
        confname,
        port,
        serverName,
        serverAlias,
        documentRoot,
        route,
        urlToMap,
    ):
        if ssh is False:
            ape = apache.Apache()
            ape.create_vhost(confname, port, serverName, serverAlias, documentRoot)
            prox = ProxyPass()
            prox.addProxyPass(confname, route, urlToMap, priority=True)
            os.system("a2ensite {0}".format(ape.httpd_path + confname))
            os.system("service apache2 reload")
        else:
            ape_ssl = apache_ssl.Apache_ssl()
            os.system("mkdir {0}".format(ape.httpd_path + confname))
            os.system(
                "sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout {0}ssl/server.key -out {0}ssl/server.crt".format(
                    ape.httpd_path
                )
            )
            ape_ssl.create_vhost(
                confname,
                port,
                serverName,
                serverAlias,
                documentRoot,
                ape_ssl.httpd_path + "ssh/server.crt",
                ape_ssl.httpd_path + "ssh/server.key",
            )
            prox = ProxyPass()
            prox.addProxyPass(confname, route, urlToMap, priority=True)
            os.system("a2ensite {0}".format(ape.httpd_path + confname))
            os.system("service apache2 reload")


if __name__ == "__main__":
    node_obj = node("site", "root", "Pingpong@123", "localhost", "/etc/apache2/")
    node_obj.host(
        True,
        "server.conf",
        8000,
        "Knockoff",
        "Knockoffalias",
        "/git_workspace/DeployDaemon/app/node",
        "/",
        urlToMap="https://example:8000",
    )
    node_obj.serve()
