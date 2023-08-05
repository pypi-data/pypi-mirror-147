#!/usr/bin/env python
#************************************************************************
# Copyright 2022 O7 Conseils inc (Philippe Gosselin)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#************************************************************************
"""Module allows to view and access ECS Cluster, Services & Task"""


# How to bash into container
# https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/
# aws ecs --profile cw execute-command  `
#     --cluster dev-nlsb-service-ecs-cluster `
#     --region ca-central-1 `
#     --task 7f467e5b42d34d4cbfec6f6bb6a7b389 `
#     --container nlsb `
#     --command "/bin/bash" `
#     --interactive
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.execute_command

#--------------------------------
#
#--------------------------------
import pprint
import logging
import subprocess

import o7lib.util.input
import o7lib.util.displays
import o7lib.aws.base


logger=logging.getLogger(__name__)

#*************************************************
#
#*************************************************
class Ecs(o7lib.aws.base.Base):
    """Class for ECS for a Profile & Region"""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#client

    #*************************************************
    #
    #*************************************************
    def __init__(self, profile = None, region = None):
        super().__init__(profile=profile, region=region)
        self.ecs = self.session.client('ecs')



    #*************************************************
    #
    #*************************************************
    def LoadClusters(self):
        """Returns all Clusters """

        logger.info('LoadClusters')

        clusters = []
        param={}


        done=False
        while not done:


            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_clusters
            resp = self.ecs.list_clusters(**param)
            #pprint.pprint(resp)
            logger.info(f'LoadClusters: Number of Clusters {len(resp["clusterArns"])}')

            if 'nextToken' in resp:
                param['nextToken'] = resp['nextToken']
            else:
                done = True

            if len(resp["clusterArns"]) == 0:
                return clusters


            respDetails = self.ecs.describe_clusters(clusters=resp["clusterArns"])
            # pprint.pprint(respDetails)
            clusters += respDetails["clusters"]

        return clusters


    #*************************************************
    #
    #*************************************************
    def LoadServices(self, cluster : str):
        """Returns all Clusters """

        logger.info(f'LoadServices for cluster : {cluster}')

        services = []
        param={
            'cluster' : cluster
        }


        done=False
        while not done:


            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_clusters
            resp = self.ecs.list_services(**param)
            #pprint.pprint(resp)
            logger.info(f'LoadServices: Number of Services {len(resp["serviceArns"])}')

            if 'nextToken' in resp:
                param['nextToken'] = resp['nextToken']
            else:
                done = True

            if len(resp["serviceArns"]) == 0:
                return services

            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_services
            respDetails = self.ecs.describe_services(cluster = cluster, services=resp["serviceArns"])
            # pprint.pprint(respDetails)
            services += respDetails["services"]

        return services


    #*************************************************
    #
    #*************************************************
    def LoadTasks(self, cluster : str, service: str):
        """Returns all Tasks """

        logger.info(f'LoadTasks for cluster={cluster}  service={service}')

        tasks = []
        param={
            'cluster' : cluster,
            'serviceName' : service
        }


        done=False
        while not done:


            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_tasks
            resp = self.ecs.list_tasks(**param)
            #pprint.pprint(resp)
            logger.info(f'LoadServices: Number of Tasks {len(resp["taskArns"])}')

            if 'nextToken' in resp:
                param['nextToken'] = resp['nextToken']
            else:
                done = True

            if len(resp["taskArns"]) == 0:
                break

            respDetails = self.ecs.describe_tasks(cluster = cluster, tasks=resp["taskArns"])
            # pprint.pprint(respDetails)
            tasks += respDetails["tasks"]

        for task in tasks:
            task['taskId'] = task.get('taskArn',"").split('/')[-1]


        return tasks


    #*************************************************
    #
    #*************************************************
    def DisplayClusters(self, clusters):
        """Diplay Instances"""
        self.ConsoleTitle(left='ECS Clusters')
        print('')
        params = {
            'columns' : [
                {'title' : 'id',          'type': 'i',    'minWidth' : 4  },
                {'title' : 'Name',     'type': 'str',  'dataName': 'clusterName'},


                {'title' : 'Status', 'type': 'str',  'dataName': 'status', 'format' : 'aws-status'},
                {'title' : 'Running Task', 'type': 'int', 'dataName': 'runningTasksCount'},
                {'title' : 'Pending Task', 'type': 'int', 'dataName': 'pendingTasksCount'},

                {'title' : 'Registered Instance', 'type': 'int', 'dataName': 'registeredContainerInstancesCount'},

            ]
        }
        o7lib.util.displays.Table(params, clusters)

        # print('Help: aws ssm start-session --target <instanceId>')

    #*************************************************
    #
    #*************************************************
    def DisplayServices(self, cluster, services):
        """Diplay Instances"""
        self.ConsoleTitle(left=f'ECS Services for cluster: {cluster}')
        print('')
        params = {
            'columns' : [
                {'title' : 'id',          'type': 'i',    'minWidth' : 4  },
                {'title' : 'Name',     'type': 'str',  'dataName': 'serviceName'},
                {'title' : 'Status', 'type': 'str',  'dataName': 'status', 'format' : 'aws-status'},

                {'title' : 'Desired', 'type': 'int', 'dataName': 'desiredCount'},
                {'title' : 'Running', 'type': 'int', 'dataName': 'runningCount'},
                {'title' : 'Pending', 'type': 'int', 'dataName': 'pendingCount'},

                {'title' : 'Type', 'type': 'str', 'dataName': 'launchType'},


            ]
        }
        o7lib.util.displays.Table(params, services)

    #*************************************************
    #
    #*************************************************
    def DisplayTasks(self, cluster, service, tasks):
        """Diplay Instances"""
        self.ConsoleTitle(left=f'ECS Task for cluster={cluster} service={service}')
        print('')
        params = {
            'columns' : [
                {'title' : 'id',          'type': 'i',    'minWidth' : 4  },
                {'title' : 'Name',     'type': 'str',  'dataName': 'taskId'},
                {'title' : 'Status', 'type': 'str',  'dataName': 'lastStatus', 'format' : 'aws-status'},

                {'title' : 'CPU', 'type': 'int', 'dataName': 'cpu'},
                {'title' : 'Memory', 'type': 'int', 'dataName': 'memory'},
                {'title' : 'Statred', 'type': 'datetime', 'dataName': 'startedAt'},

                {'title' : 'Type', 'type': 'str', 'dataName': 'launchType'},


            ]
        }
        o7lib.util.displays.Table(params, tasks)


    #*************************************************
    #
    #*************************************************
    def ShellIn(self, taskDetails):
        """Start a Shell inside a task contatiner"""

        cluster = taskDetails["clusterArn"].split('/')[-1]

        print('List of containers is task')
        containers = taskDetails.get('containers', [])
        for i, container in enumerate(containers):
            print(f'{i} -> {container["name"]}')

        key = o7lib.util.input.InputInt('Select container id : ')

        if key is None or  key < 0 or key >= len(containers):
            return


        cmd = f'aws --profile {self.session.profile_name} --region {self.session.region_name} ecs execute-command '
        cmd +=f'--cluster {cluster} --task {taskDetails["taskId"]} --container {containers[key]["name"]} '
        cmd +='--command "/bin/bash" --interactive'
        print(f'Command: {cmd}')
        subprocess.call(cmd, shell = True)



    #*************************************************
    #
    #*************************************************
    def MenuClusters(self):
        """Instances view & edit menu"""

        while True :

            clusters = self.LoadClusters()
            self.DisplayClusters(clusters)
            keyType, key = o7lib.util.input.InputMulti('Option -> Back(b) Raw(r) Details(int): ')

            if keyType == 'str':
                if key.lower() == 'b':
                    break
                if key.lower() == 'r':
                    pprint.pprint(clusters)
                    o7lib.util.input.WaitInput()

            if keyType == 'int' and  0 < key <= len(clusters):
                self.MenuServices(cluster=clusters[key - 1]['clusterName'])




    #*************************************************
    #
    #*************************************************
    def MenuServices(self, cluster):
        """Instances view & edit menu"""

        while True :

            services = self.LoadServices(cluster=cluster)
            self.DisplayServices(cluster=cluster ,services=services)
            keyType, key = o7lib.util.input.InputMulti('Option -> Back(b) Raw(r) Details(int): ')

            if keyType == 'str':
                if key.lower() == 'b':
                    break
                if key.lower() == 'r':
                    pprint.pprint(services)
                    o7lib.util.input.WaitInput()


            if keyType == 'int' and  0 < key <= len(services):
                self.MenuTasks(cluster=cluster, service=services[key - 1]['serviceName'])


    #*************************************************
    #
    #*************************************************
    def MenuTasks(self, cluster : str, service: str):
        """Instances view & edit menu"""

        while True :

            tasks = self.LoadTasks(cluster=cluster, service=service)
            self.DisplayTasks(cluster=cluster ,service=service, tasks=tasks)
            keyType, key = o7lib.util.input.InputMulti('Option -> Back(b) Raw(r) Shell-In(s) Details(int): ')

            if keyType == 'str':
                if key.lower() == 'b':
                    break
                if key.lower() == 'r':
                    pprint.pprint(tasks)
                    o7lib.util.input.WaitInput()

                if key.lower() == 's':
                    iId = o7lib.util.input.InputInt('Enter Task Id:')
                    if iId and (0 < iId <= len(tasks)):
                        self.ShellIn(taskDetails=tasks[iId - 1])
                        o7lib.util.input.WaitInput()


            if keyType == 'int' and  0 < key <= len(tasks):
                print(f"Printing Raw for task id: {key}")
                pprint.pprint(tasks[key - 1])
                o7lib.util.input.WaitInput()

#*************************************************
#
#*************************************************
if __name__ == "__main__":

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    Ecs().MenuClusters()
