import logging
import os
import time
import warnings
from fabric import Connection
from invoke import run as local_run
from wait_for import wait_for
from propertyreader import Properties


properties = Properties()


if properties.logslevel.level == 'INFO':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)s - %(levelname)s - %(message)s')

if properties.logslevel.level == 'DEBUG':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)s - %(levelname)s - %(message)s')

warnings.filterwarnings('ignore')


class Client(object):

    def __init__(self, host=None):
        self.host = host
        self.username = properties.beaker.username
        self.password = properties.beaker.password
        self.hub = properties.beaker.hub
        self.logger = logging.getLogger('system')
        self.connection = Connection(
            host=properties.beaker.env_host_string,
            user=properties.beaker.env_username,
            connect_kwargs={"password": properties.beaker.env_password}
        )
        self.hide_output = properties.logslevel.level != 'DEBUG'

    def setupBkrClient(self):
        command = "/usr/bin/bkr whoami;date"
        job = self.connection.run(command, hide=self.hide_output)

        if job.stdout.count("username") == 1:
            logging.info("Beaker client already configured!")
            return job.stdout.count("username")
        else:
            myid = self.connection.run("id -u", hide=self.hide_output)
            if int(myid.stdout) == 0:
                self.connection.run("echo -e '"
                    "[beaker]\n"
                    "name=Beaker\n"
                    "baseurl='http://download.eng.bos.redhat.com/beakerrepos/client"
                    "/RedHatEnterpriseLinux7Client'\n"
                    "enabled=1\n"
                    "gpgcheck=0'>/etc/yum.repos.d/beaker_client.repo",
                    hide=self.hide_output)

                config_auth = 'AUTH_METHOD="password"'
                config_username = 'USERNAME="{}"'.format(self.username)
                config_password = 'PASSWORD="{}"'.format(self.password)
                config_hub = 'HUB_URL="{}"'.format(self.hub)
                self.connection.run("mkdir ~/.beaker_client; echo -e '{}\n{}\n{}\n{}\n'> ~/.beaker_client/config"
                    .format(config_hub, config_auth, config_username, config_password),
                    hide=self.hide_output)

                self.connection.run("subscription-manager repos --enable=rhel-7-server-optional-rpms &&"
                    "yum clean all && yum install -y rhts-devel beaker{,lib}-redhat nmap-ncat",
                    hide=self.hide_output)

                job = self.connection.run(command, hide=self.hide_output)
                if job.stdout.count("username") == 1:
                    logging.info("Beaker client has been configured!")
                    return job.stdout.count("username")
                else:
                    logging.error(
                        "Beaker client setup failed!, please check manually or try again.")
            else:
                return int(myid.stdout)

    def randomSystem(self):

        filepath = os.getcwd()+'/files/system.xml'
        job = self.connection.run("/usr/bin/bkr job-submit --xml {}".format(filepath), hide=self.hide_output)
        location = job.stdout.find('Submitted')

        if job.ok:
            logging.info("Job {} has been submitted".format(job.stdout[location::].rsplit()[1][2:-2]))
            return job.stdout[location::].rsplit()[1][2:-2]

    def theSystem(self, hostname, distrotree):

        job = self.connection.run("/usr/bin/bkr system-provision --distro-tree={} {} "
                  .format(distrotree, hostname), hide=self.hide_output)

        if job.ok:
            logging.info("Provision job has been submitted to beaker.")

            return "Submitted"

    def _checkSSH(self, hostname):

        job = self.connection.run("echo 'QUIT'| nc -v {} 22 -w 5;date".format(hostname), hide=self.hide_output)
        count = job.stdout.count('Connected to')
        logging.info("Still awaiting to reachable on SSH Port.")
        return count

    def systemConnect(self, hostname):

        logging.info("Awaiting {} to reachable on SSH port!".format(hostname))
        time.sleep(60)
        wait_for(
            lambda: self._checkSSH(hostname=hostname) == 1,
            timeout=1000,
            delay=60,
            logger=self.logger
        )

        if self._checkSSH(hostname=hostname) == 1:
            logging.info("{} is reachable on SSH port".format(hostname))
            return "Up"
        else:
            logging.error("{} is not reachable on SSH port, Please check.".format(hostname))

    def _cstatus(self, jobID):
        rstatus = None
        hostname = None
        jobcheck = self.connection.run("/usr/bin/bkr job-results {}".format(jobID), hide=self.hide_output)
        logging.info("This may take sometime, awaiting system to build ..")

        if 'system value=' in jobcheck.stdout:
            istart = jobcheck.stdout.find('system value=')
            iend = jobcheck.stdout.find('/></role></roles><repos/><distroRequires>')
            hostname = jobcheck.stdout[istart:iend].split('=')[1].split('"')[1]

        for status in ['Cancelled', 'Running']:
            if status in jobcheck.stdout:
                rstatus = status

        return [rstatus, hostname]

    def jobStatus(self, jobID):

        wait_for(
            lambda: self._cstatus(jobID=jobID)[0] == 'Running',
            timeout=6000,
            delay=60,
            logger=self.logger
        )
        status = self._cstatus(jobID=jobID)
        logging.info(status)
        return status

    def contentHost(self):

        filepath = os.getcwd()+'/files/contenthost.xml'
        job = self.connection.run("/usr/bin/bkr job-submit --xml {}".format(filepath), hide=self.hide_output)
        location = job.stdout.find('Submitted')

        if job.ok:
            logging.info("Job {} has been submitted".format(job.stdout[location::].rsplit()[1][2:-2]))
            return job.stdout[location::].rsplit()[1][2:-2]
