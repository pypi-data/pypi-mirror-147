===========
Codechecker
===========
---------------------------------------
Facilities to manage coding challenges.
---------------------------------------

.. image:: https://img.shields.io/pypi/pyversions/cc-codechecker
    :target: https://pypi.org/project/cc-codechecker/
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/v/cc-codechecker
    :target: https://pypi.org/project/cc-codechecker/
    :alt: PyPI

.. image:: https://img.shields.io/pypi/dm/cc-codechecker
    :target: https://pypi.org/project/cc-codechecker/
    :alt: PyPI - Downloads

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit

.. image:: https://results.pre-commit.ci/badge/github/Daniele-Tentoni/cc-codechecker/main.svg
    :target: https://results.pre-commit.ci/latest/github/Daniele-Tentoni/cc-codechecker/main
    :alt: pre-commit.ci status

.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/

.. image:: https://api.codacy.com/project/badge/Grade/cd570d18e58e45ea832a8031388d112d
   :alt: Codacy Badge
   :target: https://app.codacy.com/gh/Daniele-Tentoni/cc-codechecker?utm_source=github.com&utm_medium=referral&utm_content=Daniele-Tentoni/cc-codechecker&utm_campaign=Badge_Grade_Settings

.. image:: https://api.reuse.software/badge/github.com/Daniele-Tentoni/cc-codechecker
   :alt: REUSE status
   :target: https://api.reuse.software/info/github.com/Daniele-Tentoni/cc-codechecker

**Table of Contents**:

A. `Purpose`__

B. `Install`__

C. `Usage`__

   1. `Basic example`__

   2. `Advanced example`__

D. `Contributing`__

E. `Complete configuration reference`__

   1. `First level`__
   2. `Project reference`__
   3. `Challenge reference`__

__ `Purpose`_
__ `Install`_
__ `Usage`_
__ `Basic example`_
__ `Advanced example`_
__ `Contributing`__
__ `Complete configuration reference`_
__ `First level`_
__ `Project reference`_
__ `Challenge reference`_

Purpose
=======

Use **codechecker** to manage coding challenge hosted entirely on Github. This have as advantage that every one can apply to the challenge easily, we can use the already implemented Github social coding suites like issues, pull requests, pages and actions and users are invited to populate their Github profiles with repository that shows their skills.

In 2022, coding challenges are even used to determine what kind of employee companies might hire. Being able to create coding challenges and make them easy to access could mean more potentially developers to admit to a more advanced interview.

Other repository hosting sites are not supported at the moment. Return here in the future or start contributing_.

Install
=======

You can install codechecker using **pip**::

  pip install cc_codechecker

Usage
=====

Using codechecker for a coding challenge is very simple.

Init a new challenge inside your current repository using the facility::

  cc_codechecker init

This command will create a new ``.codechecker.yml`` file inside your root directory. Obv, you can create that file by your own. Then, specify what programming languages you support and how you support them! You can declare, for example:

1. What version of specified language you support (not implemented)
2. What dialect of specified language you support (not implemented)
3. How many points you assign for each problem solved (not implemented)

More features will be added. Return here in the future or start contributing_.

> We enforce the use of ``.`` preceding codechecker files inside challenge repository to make it hidden by default on many know system, to let users focus more and better on the challenge.

Warning! Running init command in a repository that already hold a configuration file return an ``EX_CANTCREATE(73)`` error. To overwrite current configuration, run with the option ``--overwrite-yml``.

Basic example
~~~~~~~~~~~~~

The following code can be considered the minimum configuration for a challenge.

For the simplest example of codechecker use this short configuration::

  challenge: base
  project: bash

This represent the following folder structure::

  - <challenge-name>/
      - bash/
          - program.sh
      - .codechecker.yml
      - README.md

This basic example shows how to prepare a challenge that supports only **bash** language with only one challenge called **base**. Executing a score keeping command, like `cc_codechecker run`, inside this repo will means:

1. Start collecting points for the challenge *base*
2. Try to run *bash* program inside *bash* folder without any argument without expecting any output
3. Give no points to users, commenting only if the challenge was completed or not

> You can use codechecker in tandem with the related Github Action to collect that score file and create a Github Pages landing page for your challenge.

Advanced example
~~~~~~~~~~~~~~~~

The following code is used for a challenge supporting many languages and assigning more points for more difficult challenges.

For the simplest example of codechecker inside the yaml file write this code::

  # Project definitions (for any challenge declared)
  projects:
    # Project with custom folder name
    - language: 'bash'
      folder: 'for-shell-lovers'

    # Simple project
    - language: csharp

  # Challenges definitions
  challenges:
    # Simple challenge (doesn't score points)
    - name: challenge1

    # Challenge with value (score points)
    - value: 1

    # Challenge that take input from file
    - name: challenge3
      argument: input_challenge3.txt
      result: result_challenge3.txt

    # Challenge that take input from array
    - name: challenge4
      arguments: [1, 1]
      results: [2]

    # Challenge with additional projects
    - value: 5
      argument: input_challenge5.txt
      result: result_challenge5.txt
      projects: [!csharp]

    # Challenge with additional complex projects
    - argument: input6.txt
      result: result6.txt
      projects: [csharp]

This configuration means the following folder structure::

  - <challenge-name>-solutions/
      - input_challenge3.txt
      - result_challenge3.txt
      - input_challenge4.txt
      - result_challenge4.txt
      - input5.txt
      - result5.txt

  - <challenge-name>/
      - for-shell-lovers/
          - script.sh
      - csharp/
          - csharp.csproj
          - program.cs
      - .codechecker.yml
      - readme

This is a really complex configuration that can be explained as following:

1. Compute the first challenge named challenge1
   a. Try to execute the project *for-shell-lovers* coded with bash language without any input, without collecting any results
   b. Try to execute the project *csharp* without any input, without collecting any result
2. Compute the second challenge that assign 1 points
   a. If *for-shell-lovers* exit with a successfully result, mark challenge as resolved
   b. If *csharp* exit with a successfully result, mark challenge as resolved
   c. If the challenge is marked as resolved, assign points
3. Compute the third challenge that doesn't assign any points
   a. Get the content of the file input_challenge3.txt and copy it in the same folder of the project *for-shell-lovers* as input.txt
   b. If *for-shell-lovers* exit with a successfully result giving as input the current relative path to the copied file, check it's content and if correspond to the contents of the file result_challenge3.txt, mark challenge as resolved
   c. If *csharp* exit with a successfully result giving as input the current relative path to the copied file, check it's content and if correspond to the contents of the file result_challenge3.txt, mark challenge as resolved
   d. If the challenge is marked as resolved, assign points
4. Compute the fourth challenge that doesn't assign any points. This challenge instead giving files as inputs, give data as arguments
5. Compute the fifth challenge that assign 5 points, without executing csharp project, permitting users to resolve this challenge using only bash language
6. Compute the sixth challenge that doesn't assign any points only for bash language

:!: The option for excluding or including projects is not implemented yet.

Contributing
============

Contributions are welcome! Check out `Contributing Guidelines`_.

.. _Contributing Guidelines: /CONTRIBUTING.rst

Complete configuration reference
================================

All features listed here are implemented. This is not a code documentation.

First level
~~~~~~~~~~~

challenges
  Define each step of the challenge, assigning to each of them. This is *required* in each configuration.

output
  Define the name of the output score file name.

projects
  Define the list of projects inside the repository. This is *required* in each configuration.
  See Project for option reference of this yaml section.

Project reference
-----------------

language
  Define the programming language for the project. This is *required* for each project.

  Supported programming languages are:

  * Bash, using ``bash`` (other sh dialect for small things work the same, but are not tested)
  * CSharp, using ``dotnet``

Challenge reference
-------------------

Define a step of the challenge.

It can assign points to score the attempt.

name
  Define the name of the challenge. Use in challenge run report.

value
  Points to assign completing the challenge. Don't give value if you don't wan't to evaluate that step.

argument
  Name of the file to give as input to the challenge. Giving input exclude inputs.

result
  Name of the file to give as result checker. Giving result exclude results.

arguments
  Array of items to give as input to the challenge. Giving inputs exclude input.

results
  Array of items to give as result checker.
