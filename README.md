# ProjectBackEndCC

## Project summary
### One-sentence description

This is the back end for Planner Planter, a web app to help you organize coursework, growing virtual trees as you complete tasks for an additional motivation boost.

The front end can be found at https://github.com/joiiewang/ProjectFrontendCC.

### Project overview

Students taking many courses need to organize infrormation for each one. There are todo list apps, calendar apps, and notes apps that can help with this, but this splits the information across multiple apps.

Planner Planter attempts to address this issue by letting you put all the information in one platform. For a motivation boost, it also shows a virtual tree that grows as you complete tasks.

## Installation
### Prerequisites

This project was developed on a CentOS 8 Docker instance. The following commands were used to install prerequisites:

yum -y install openssh-server sudo python3 zlib-devel bzip2 bzip2-devel readline readline-devel openssl-devel sqlite-devel which gcc libffi-devel passwd vim nano glibc-locale-source glibc-langpack-en npm

yum -y groupinstall "Development Tools"

mkdir -p -m 775 /usr/local/bin

export PATH=${PATH}:/usr/local/bin

export LANG=en_US.UTF-8

export LANGUAGE=en_US.UTF-8

alternatives --set python /usr/bin/python3

update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

python -m pip install --upgrade pip

python -m pip install virtualenv

### Installation steps

Clone this repository and run the following steps in the command line:

python -m venv venv/

source venv/bin/activate

python -m pip install --upgrade pip    

python -m pip install flask

python -m pip install gunicorn

export PORT=8118

python myapp.py

## Functionality and known issues

Users can create an account by submitting a username and password on the registration page. Once logged in, a user can add courses they are enrolled in. For each course, the user may add links, notes, and todos associated with that course. The user can also add links, notes, and todos not associated with any course. The user can view all links, notes, or todos from all courses on one page by clicking on its tab. Todo items are sorted by date. When an item is completed, the user may check it off to hide it. Completed items can be shown by clicking the Show Completed button. There is also a calendar tab that lets you conveniently see the tasks for each day and how much progress is made. A tree shown on the bottom right corner of the page grows as tasks are completed. When a tree is done growing, it is moved to a Forest tab.

A known issue is when the user switches between tabs too quickly, the frontend fails to fetch the required information from the backend and reports an error. However, the page still loads correctly.

## License

Copyright 2020 Ashley Bruce, Zachary Minshall, Charlie Wan, Joy Wang, Daniel Zhang

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

