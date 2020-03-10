#!/bin/#!/usr/bin/env bash
python AWS/S3/download_files.py --bucket c4i-datasets --prefix ben_shemen/13-02-2020/Shvil2/drive_cam1 --local-path /home/amit/Data/Probot_Recordings/BenShemen/13-02-2020/Shvil2/drive_cam1 --filter drive_cam1
python AWS/S3/download_files.py --bucket c4i-datasets --prefix ben_shemen/13-02-2020/Shvil2/drive_cam2 --local-path /home/amit/Data/Probot_Recordings/BenShemen/13-02-2020/Shvil2/drive_cam2 --filter drive_cam2
