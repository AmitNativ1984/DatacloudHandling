#!/bin/#!/usr/bin/env bash
python AWS/S3/copy_between_buckets.py --source-bucket c4i-datasets --prefix ben_shemen/14-01-2020/drive2-day/drive_cam0  --n-samples 1500
python AWS/S3/copy_between_buckets.py --source-bucket c4i-datasets --prefix ben_shemen/14-01-2020/drive3-day/drive_cam0  --n-samples 1500
python AWS/S3/copy_between_buckets.py --source-bucket c4i-datasets --prefix ben_shemen/14-01-2020/drive4-night/drive_cam3  --n-samples 1500
python AWS/S3/copy_between_buckets.py --source-bucket c4i-datasets --prefix ben_shemen/14-01-2020/drive5-night/drive_cam3  --n-samples 1500
