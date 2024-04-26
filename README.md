# Bao&Bento Python App

Hello there! This repo is simply a backup and record of my A-Level programming project.

It's not very good and you shouldn't expect it to even work on your device without some finnicking.

If you do intend to use it for youself, here's some things you should know:
- Made in `Tkinter 8.6`, `Python 3.12.0`, `MySQL Server 8.0.35`, `pip 23.3.1`. Other versions are untested and may not work
- You'll need to set up a MySQL server instance using MySQL Workbench
- The logins for MySQL are hard-coded in `main.py`, so you may need to change them to suit your needs
- You'll need an email which you can log in to using Python with only an email and password
- You'll need a .env or you can hard-code your email logins. It's up to you
- An internet connection is required to send emails
- The owner login defaults to u:`pcheung` p:`MrBao123`. You can change this using MySQL Workbench if you want
- Libraries needed (some may need to be installed with pip*):
  - sys
  - os
  - tkinter 
  - mysql *mysql-connector 2.2.9
  - docx *python-docx 1.1.0
  - time
  - datetime
  - calendar
  - json
  - math
  - re
  - ssl
  - smtplib
  - dotenv *python-dotenv 1.0.1
  - email

\*Marks pip package name & version

When installing the needed packages, their dependencies should automatically be installed as well
