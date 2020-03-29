import os
from dotenv import load_dotenv

load_dotenv()


class Apache:
    httpd_path = ""

    def __init__(self):
        self.httpd_path = os.getenv("HTTPD_PATH")

    # create a vhost file from the template
    def create_vhost(self, confName, port, serverName,
                     serverAlias, documentRoot):
        template = open("base_template.txt", 'r')
        required = template.read().format(
            port=port,
            serverName=serverName,
            serverAlias=serverAlias,
            documentRoot=documentRoot)
        targetFile = open(self.httpd_path + confName, 'w')
        targetFile.write(required)
        targetFile.close()
        template.close()

    # Edit a given vhost config file
    # ISSUE : Better Parsing ideas are welcome
    def edit_vhost(self, confName, port=None, serverName=None,
                   serverAlias=None, documentRoot=None):
        targetFile = open(self.httpd_path + confName, 'r+')
        lines = targetFile.readlines()
        for i, line in enumerate(lines):
            if "serverName_Flag" in line:
                line_array = lines[i + 1].split()
                line_array[1] = serverName + "\n"
                lines[i + 1] = "\t" + " ".join(line_array)

            if "serverAlias" in line:
                line_array = lines[i + 1].split()
                line_array[1] = serverAlias + "\n"
                lines[i + 1] = "\t" + " ".join(line_array)

            if "documentRoot" in line:
                line_array = lines[i + 1].split()
                line_array[1] = documentRoot + "\n"
                lines[i + 1] = "\t" + " ".join(line_array)

        targetFile.seek(0)
        targetFile.writelines(lines)
        targetFile.truncate()
        targetFile.close()

    # Delete the config
    def delete_vhost(self, confName):
        os.remove(self.httpd_path + confName)


# To test current module
if __name__ == '__main__':
    apache = Apache()
    apache.create_vhost("8080", "test.com.conf", "sensors",
                        "/etc/apache2", "test.com.conf")
    apache.edit_vhost("test.conf.com", serverName="test.in")
    # apache.delete_vhost("test.conf.com")
