[![PyPI version](https://badge.fury.io/py/lfnt.svg)](https://badge.fury.io/py/lfnt)

# Elephant (lfnt)

`lfnt` eats development environments.

## What??

Setting up a development environment is a lot like eating an elephant—you have to take it one bite at a time.
Whether you're such a noob that you don't even know what a noob is or you're such a vet that you already have opinions about this project, you know that starting from scratch is daunting.
Meanwhile, we all keep eating, and re-eating, the same elephant!

In my humble opinion, that's just stupid.

But I'm not alone.
Developers are now commonly adding their config files and installation scripts to their own code repos.
Yet even that is still a pain in the ass to manage, especially when it comes down to every little detail.

That's where `lfnt` comes in useful—it handles all of the grunt-work for you.
`lfnt` eases the pain of managing your development environment by:

* Maintaining your configuration repository
* Keeping track of what packages have been installed and how
* Restoring your whole setup to a new machine from your configuration repository
* Providing a platform for environment sharing and test-driving others'

So just install this package and let `lfnt` do the rest!

## How??

`lfnt` is written in Python3, which means that most workstations are already equipped to use it.
It allows you to interact with your environment from a command-line and/or visually from a local web app.
You can use it to create a new configuration repository or sync with an existing one—and even perform automatic backups.

All you need to do is start up a terminal and run:

`pip install lfnt`

After the installation is complete, run `lfnt` with no arguments for a synopsis.
For example:

```
$ lfnt
Usage: lfnt [OPTIONS] COMMAND [ARGS]...

  For eating development-environment elephants.

Options:
  --help  Show this message and exit.

Commands:
  browse    Run in a web browser.
  dump      Take a config dump.
  eat       Ingest packages and applications.
  init      Initialize a configuration.
  poop      Eliminate packages and applications.
  remember  Save and commit environment.
```
