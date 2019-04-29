import logging
import requests
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
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


class InstallerJob(object):

    def install(self, **kwargs):
        self.url = properties.jenkinsInstaller.jenkins_url
        self.jobName = properties.jenkinsInstaller.jenkins_jobname

        requests.packages.urllib3.disable_warnings()

        logging.info("Talking to Jenkins now.")
        connectJenkin = Jenkins(self.url,
                                requester=CrumbRequester(baseurl=self.url, ssl_verify=False))
        job = connectJenkin[self.jobName]
        query = job.invoke(build_params=kwargs)
        logging.info("{} job has been successfully submitted.".format(query.get_job_name()))

        if query.is_queued() or query.is_running():
            query.block_until_complete(delay=30)

        build = query.get_build()

        if build.get_status() == 'SUCCESS':
            logging.info("{} job has been completed.".format(build))
            return 'SUCCESS'
        else:
            logging.info("{} job has been completed with result {}, for more details go at {}"
                         .format(build, build.get_status(), build.get_result_url()))
            return 'FAILURE'
