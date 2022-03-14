# Procedure

The proposed procedure is explained in the subsections to follow. I have, given my understanding, tried to replicate their environment to the best of my ability. 

Two virtual servers were deployed representing the watson machine learing GPU based instances deployed within their enviornment. I understand there were more than 2, but 2 should suffice for this proof of concept.

In addition, an artificatory instance was deployed.

Note, both our mock GPU based instances and artificatory are deployed in IBM Cloud in the same VPN and Subnet. Abiding by the principles of least privilege, the VM's can only talk to one another and artifactory. Only admins (me in this case) are allowed to SSH in the respective instances.

I am referencing the image given below.

![Alt text](./wmla-v1-poc-anz.png?raw=true "Title")

## 1 - Upload Asset

This was designed with security in mind. As such, only users with sufficient prviileges are allowed to upload the assets to the internal artifactory (By assets, I mean Machine Learning related files for training/validation/testing purposes).

## 2 - Submit PR

By the same token, only authenticated users (this could be the same or a different user) are then able to submit a PR to the repository. This PR contains metadata in relation to the uploaded asset. The administrator can then accept the PR provided the asset is indeed required and the metadata can be parsed correctly by the script (The script checks for this anyhow and guards against this)

## 3 - Approve PR

As stated above, provided the constraints are satisifed. The PR will be merged. The new asset metadata is now present in the repository.

## 4 - Poll Repository Periodically

A cron job running periodically executes a python script which polls the repository, checks for the presence of new metadata, downloads the relevant asset(s) (the metadata is a pointer to the actual location of the asset housed in Artifactory) and writes the contents to the shared drive, now accessible by the NFS clients.
