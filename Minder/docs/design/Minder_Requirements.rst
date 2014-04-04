Requirements
============

Date 2014/03/25

Author Harlan AuBuchon


Minder
======

Description
-----------

Minder is a DVCS Semi-automatic-syncing File System and Organization Application designed to simplify the synchronization of files between multiple devices.

Minder wants to ensure only one particular file exists in the system and tracks changes made to that file.  The file system tree is maintained by User and may be synchronized to a central repository if needed.  Certain file types (e.g, Pictures, PDFs) may be configured to be moved to a particular folder location automatically.

Minder sounds like git-annex or other DVCS-Autosync programs but the differences are distinct in two ways:

* Minder is manual – it wants you to choose which files you want on your devices by selecting folders and which you don't want anymore.
* Minder wants to help you stay organized by cleaning up after you, renaming files so they have future context, and putting things in the right place.


In Scope for Analysis
---------------------

Linux and Android Operating systems

USB Drive


Assumptions
-----------

File system change notification mechanisms should be similar in Android, Linux, Unix and possibly iOS.  If not, a third party Python library will need to be sourced for this purpose or make file versioning a manual process.

Some type of Distributed Version Control System such as GIT (python-git) will be used as the base interface for versions, branches and "checking in/out" files.

An SSH library is needed to manage secure connections in Python.  Perhaps paramiko or pexpect.



Requirements
------------

1. **Versioning**
    1. Track File changes and store a version associated with each change.
    
2. **Organizer**
    1. Automatically move files into configurable folders by mime-type/file extension.
    2. Ensure that only one copy of a file exists within a configured folder location.
    
3. **User Interface**
    1. Provide a User Interface via a secure localhost webapp.
    2. Start a “Minder Session” which will prompt for a name and create a branch of tracked changes in the working file tree.
    3. Synchronize the File Tree.
    4. Organize the files into the tree.
    5. Manage configuration.
    6. Choose which files will be pulled onto the device.
    7. Provide ability to choose which version is used as the current file.
    
4. **Remotes**
    1. Provide the ability to configure a secure remote Minder Repository and synchronize it with the device.
    
5. **Security**
    1. Encryption
        1. SSH2 (Busybox/Python) will be used to create keypairs for all local and remote connections.
    

Optional
--------

5. Discovery
   Provide a server and client mechanism that is aware of other Minder Nodes on the LAN.


Dependencies
------------

Risks
-----

QA Test Plan
------------