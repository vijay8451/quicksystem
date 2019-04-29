import click
import sender
from beakerclient import Client
from jenkinsjob import InstallerJob
from msg import echo_error, echo_normal, echo_success
from propertyreader import Properties

properties = Properties()


class Config(object):

    def __init__(self):
        self.host = properties.theSystem.host


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
def cli():
    """ CLI tool to reserve, provision a system and use Jenkins job for Satellite.
       """
    pass


@cli.command()
@click.option('--jenkins-job', default=False,
              help="to run installer job i.e. --jenkins-job=True")
@click.option('--content-host', default=False,
              help="to reserve and provision content hosts              "
                   "i.e. --content-host=True")
@pass_config
def random_System(config, jenkins_job, content_host):
    """Reserve and provision any random system."""

    try:
        Satellite=[]
        ContentHost=[]
        system = Client()
        jobid = system.randomSystem()
        joststatus = system.jobStatus(jobID=jobid)

        if joststatus[0] == 'Running':
            echo_normal('\n\t\t'+"System is reserved, Checking system connection..\n\n")
            status = system.systemConnect(hostname=joststatus[1])
            if status == "Up":
                echo_success('\n\t\t'+joststatus[1] + " successfully provisioned!!\n\n")
                Satellite.append('{}'.format(joststatus[1]))
            else:
                return echo_error('\n\t\t' + 'Something went wrong!!\n\n')

            if status == "Up" and jenkins_job:
                job = InstallerJob()
                jobstatus = job.install(SERVER_HOSTNAME=joststatus[1])
                if jobstatus == 'SUCCESS':
                    echo_success('\n\t\t'+"Satellite installed successfully!!\n\n")
                else:
                    return echo_error('\n\t\t'+'Something went wrong!!\n\n')

            if status == "Up" and content_host:
                system = Client()
                jobid = system.contentHost()
                joststatus = system.jobStatus(jobID=jobid)

                if joststatus[0] == 'Running':
                    echo_normal('\n\t\t' + "System is reserved, Checking system connection..\n\n")
                    status = system.systemConnect(hostname=joststatus[1])
                    if status == "Up":
                        echo_success('\n\t\t' + joststatus[1] + " successfully provisioned!!\n\n")
                        ContentHost.append('{}'.format(joststatus[1]))
                    else:
                        return echo_error('\n\t\t' + 'Something went wrong!!\n\n')

        echo_normal('\nSatellite hosts => ' + str(Satellite))
        echo_normal('  Content hosts => ' + str(ContentHost))
        sender.SendEmail(version=properties.jenkinsInstaller.satellite_version,
                         shost=Satellite,
                         chost=ContentHost)

    except Exception as exp:
        echo_error('\n\t\t'+'Something went wrong!!\n\n')
        echo_error(exp)


@cli.command()
@click.option('--jenkins-job', default=False,
              help="to run installer job i.e. --jenkins-job=True")
@pass_config
def theSystem(config, jenkins_job):
    """Provision a already reserved system."""

    try:
        system = Client()
        jobsubmit = system.theSystem(hostname=config.host,
                                     distrotree=properties.theSystem.distrotree)
        if jobsubmit == "Submitted":
            status = system.systemConnect(hostname=config.host)
            if status == "Up":
                echo_success('\n\t\t'+"System successfully provisioned!!\n\n")
            else:
                return echo_error('\n\t\t' + 'Something went wrong!!\n\n')

            if status == "Up" and jenkins_job:
                job = InstallerJob()
                jobstatus = job.install(
                    SERVER_HOSTNAME=config.host,
                    SATELLITE_DISTRIBUTION=properties.jenkinsInstaller.satellite_distribution,
                    SATELLITE_VERSION=properties.jenkinsInstaller.satellite_version,
                    SETUP_FAKE_MANIFEST_CERTIFICATE=properties.jenkinsInstaller.setup_fake_manifest_certificate,
                )
                if jobstatus == 'SUCCESS':
                    echo_success('\n\t\t'+"Satellite installed successfully!!\n\n")
                else:
                    return echo_error('\n\t\t'+'Something went wrong!!\n\n')

    except Exception as exp:
        echo_error('\n\t\t'+'Something went wrong!!\n\n')
        echo_error(exp)


@cli.command()
@pass_config
def setup_client(config):
    """ Setup beaker client. """
    try:
        echo_normal('\n\t\t'+"Started Beaker client configuration...\n\n")
        system = Client()
        setupclient = system.setupBkrClient()
        if setupclient == 1:
            echo_success('\n\t\t'+"Beaker client working!!\n\n")
        elif setupclient > 1:
            return echo_error('\n\t\t'+"Can not setup with non root user\n\n")

    except Exception as exp:
        echo_error('\n\t\t'+'Something went wrong!!\n\n')
        echo_error(exp)


@cli.command()
@click.option('--host', required=True,
              help="to install Satellite on a host i.e. --host=host.example.com")
@pass_config
def jenkins_installer(config, host):
    """ Install Satellite using Jenkins installer job. """
    try:
        job = InstallerJob()
        jobstatus = job.install(SERVER_HOSTNAME=host)
        if jobstatus == 'SUCCESS':
            echo_success('\n\t\t'+"Satellite installed successfully!!\n\n")
        else:
            echo_error('\n\t\t'+'Something went wrong!!\n\n')

    except Exception as exp:
        echo_error('\n\t\t'+'Something went wrong!!\n\n')
        echo_error(exp)

@cli.command()
@pass_config
def content_host(config):
    """Reserve and provision content host."""

    try:
        ContentHost=[]
        system = Client()
        jobid = system.contentHost()
        joststatus = system.jobStatus(jobID=jobid)

        if joststatus[0] == 'Running':
            echo_normal('\n\t\t' + "System is reserved, Checking system connection..\n\n")
            status = system.systemConnect(hostname=joststatus[1])
            if status == "Up":
                echo_success('\n\t\t' + joststatus[1] + " successfully provisioned!!\n\n")
                ContentHost.append('{}'.format(joststatus[1]))
        echo_normal('\n  Content hosts => ' + str(ContentHost))

    except Exception as exp:
        echo_error('\n\t\t'+'Something went wrong!!\n\n')
        echo_error(exp)
