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

A cron job running periodically executes a python script which polls the repository, checks for the presence of new metadata, downloads the relevant asset(s) (the metadata is a pointer to the actual location of the asset housed in Artifactory) and writes the contents to the shared drive, now accessible by the NFS clients (the GPU based in house servers).

The following security measures were implemented:

1) SSH based authentication prior to performing the git clone
2) Artifactory credentials stored securely in the server (just one of the servers suffices) only accessible by the root user. 

## 5 - Write

Finally, as the name implies, the downloaded asset is written to the intended location, provided the asset is not already present of course.

## Summary

From an end user perspective, proviced both the asset is to be uploaded to artifactory and the corresponding pull request is merged, the asset should be present in the server shortly thereafter. Note, we can remove Git (it is essentially acting as a "middle man" here) and directly query artifactory. That said, using Git as the source of truth would likely negate any auditing and compliance concerns.

## Extensions

Right now, to troubleshoot any runtime errors (very unlikely to occur due to the nature of this task), one must inspect crond runtime logs in the server (/var/log/cron; don't quote me on this). This is probably not a dealbreaker, as this is expected to run smoothly. That said, if advanced reporting was required, extra work must be done (Eg, parsing and forwarding the cron logs to a group of users via, say, SMTP).

Finally, I am using a simple python client (nothing wrong with that for a POC). A fully-fledged production solution may emply automation agents such as Ansible. Error checking, custom retry policies, ensuring idemponecy, debugging and logging are provided out of the box. 
