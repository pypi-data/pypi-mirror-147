# leetcron

A CLI tool for setting up a cron job that pushes recent leetcode submissions to a specified Github repo.

### 0.1.0 Updates
* Added support for the latest languages on Leetcode
* Added handling to prevent cron job failing from unrecognized language

## Installation
```
pip install leetcron
```

## Setup
```
leetcron setup
```
#### Options
`-g` Github setup
`-c` Leetcode cookie setup
`-j` Cronjob setup

#### Notes
* Obtain a Github Access Token through the steps [here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
* Make sure you are logged into Leetcode on Chrome or Firefox before running the setup.
* Try running `leetcron setup -c` to grab the newest Leetcode cookie if task fails.

## Push recent submissions to repo manually
```
leetcron run
```