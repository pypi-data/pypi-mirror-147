import os
import re
import string
from configparser import ConfigParser
from pathlib import Path
from typing import Optional
import json
import time

import click
from git import Repo, InvalidGitRepositoryError, NoSuchPathError, GitCommandError
import gitlab

repo = None

try:

    repo = Repo(Path(Path.home(), "wcc"))

    project_name_with_namespace = repo.git.execute(['git', 'remote', 'get-url', 'origin'])
    project_name_with_namespace = re.findall(r'git@gitlab\.com:(.+)\.git', project_name_with_namespace)[0]
    assert project_name_with_namespace
    project_name = project_name_with_namespace.split("/")[-1]
    assert project_name
except GitCommandError as err:
    click.secho("Failed to parse repository name, aborting", fg='red')
    click.echo(err)

gl = gitlab.Gitlab('https://gitlab.com/', private_token='EA7v3zT8oW84HX2BYz96')
gl.auth()

project = gl.projects.get(project_name_with_namespace)

pipelines_json = open('pipelines.json', 'a+')

page = 1

while True:

    pipelines = project.pipelines.list(page=page, per_page=50, order_by='updated_at', sort='asc', status='success')

    if pipelines:

        print(f"PAGE {page}")

        for pipeline in pipelines:
            p = project.pipelines.get(pipeline.id)
            print(p)
            pipelines_json.write(json.dumps(p.attributes, indent = 4))
            time.sleep(0.5)

        page += 1

    else:

        pipelines_json.close()
        break