import configparser

config = configparser.ConfigParser()
config.read('quicksystem.properties')


class Properties(object):
    """quicksystem properties reader """

    def __init__(self):
        self.randomSystem = RandomSystem()
        self.beaker = Beaker()
        self.jenkinsInstaller = JenkinsInstaller()
        self.theSystem = TheSystem()
        self.contentHost = ContentHost()
        self.mymail = Mymail()
        self.logslevel = LogsLevel()


class RandomSystem(object):
    """random system reader"""
    def __init__(self):
        self.system_count = config.get('RandomSystem', 'system_count')


class Beaker(object):
    """beaker reader"""
    def __init__(self):
        self.username = config.get('Beaker', 'krb_username')
        self.password = config.get('Beaker', 'krb_password')
        self.hub = config.get('Beaker', 'beaker_url')
        self.env_host_string = config.get('Beaker', 'env_host_string')
        self.env_username = config.get('Beaker', 'env_username')
        self.env_password = config.get('Beaker', 'env_password')


class JenkinsInstaller(object):
    """Jenkins Installer reader"""
    def __init__(self):
        self.satellite_distribution = config.get('JenkinsInstaller', 'satellite_distribution')
        self.satellite_version = config.get('JenkinsInstaller', 'satellite_version')
        self.jenkins_url = config.get('JenkinsInstaller', 'jenkins_url')
        self.jenkins_jobname = config.get('JenkinsInstaller', 'jenkins_jobname')
        self.setup_fake_manifest_certificate = config.get('JenkinsInstaller',
                                                          'setup_fake_manifest_certificate')


class TheSystem(object):
    """theSystem reader"""
    def __init__(self):
        self.host = config.get('TheSystem', 'host')
        self.distrotree = config.get('TheSystem', 'distrotree')


class ContentHost(object):
    """content host reader"""
    def __init__(self):
        self.host_count = config.get('ContentHost', 'host_count')


class Mymail(object):
    """Email reader"""
    def __init__(self):
        self.login_mailid = config.get('Emails', 'login_mailid')
        self.login_password = config.get('Emails', 'login_password')
        self.to_mail = config.get('Emails', 'to_mail')


class LogsLevel(object):
    """Logs reader"""
    def __init__(self):
        self.level = config.get('Logs', 'level')
