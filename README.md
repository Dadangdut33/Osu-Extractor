<p align="center">
    <img src="https://raw.github.com/Dadangdut33/Osu-Extractor/main/logo.png" width="250px" alt="Osu Extractor Logo">
</p>

<h1 align="center"> Osu Extractor - Extract/Copy song, images, videos, and more from installed Osu beatmaps </h1>
<p align="center">
    <a href="https://lgtm.com/projects/g/Dadangdut33/Osu-Extractor/alerts/"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/Dadangdut33/Osu-Extractor.svg?logo=lgtm&logoWidth=18"/></a>
    <a href="https://lgtm.com/projects/g/Dadangdut33/Osu-Extractor/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/Dadangdut33/Osu-Extractor.svg?logo=lgtm&logoWidth=18"/></a>
    <a href="https://github.com/Dadangdut33/Osu-Extractor/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/Dadangdut33/Osu-Extractor"></a>
    <a href="https://github.com/Dadangdut33/Osu-Extractor/pulls"><img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/Dadangdut33/Osu-Extractor"></a>
    <a href="https://github.com/Dadangdut33/Osu-Extractor/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Dadangdut33/Osu-Extractor?style=social"></a>
    <a href="https://github.com/Dadangdut33/Osu-Extractor/network/members"><img alt="GitHub forks" src="https://img.shields.io/github/forks/Dadangdut33/Osu-Extractor?style=social"></a>
</p>

Extract/copy song, images, videos, and more from installed Osu beatmaps. Made using python.

<h1>Jump to</h1>

- [Preview](#preview)
- [Downloads](#downloads)
- [How To Install](#how-to-install)
- [How To Uninstall](#how-to-uninstall)
- [How To Compile It To .exe Yourself](#how-to-compile-it-to-exe-yourself)
- [Disclaimer](#disclaimer)

---
<br>

# Preview
- OsuExtractor CLI
  <details open>
  <summary>Preview</summary>
  <p align="center">
  <img src="https://media.discordapp.net/attachments/653206818759376916/914395805840998460/unknown.png" width="700" alt="Main Menu">
  <img src="https://media.discordapp.net/attachments/653206818759376916/914409434187456522/unknown.png" width="700" alt="Extract Menu"><br>
  <b>You can use the new windows terminal to run the program with better look</b>
  <img src="https://media.discordapp.net/attachments/653206818759376916/914409496158298122/unknown.png" width="700" alt="Extract Menu - Via Windows terminal">
  <img src="https://media.discordapp.net/attachments/653206818759376916/914399313243832340/unknown.png" width="700" alt="Extract All - Via Windows terminal">
  <img src="https://media.discordapp.net/attachments/653206818759376916/914396946825871380/unknown.png" width="700" alt="About - Via Windows Terminal">
  <img src="https://media.discordapp.net/attachments/653206818759376916/914407734076641280/unknown.png" width="700" alt="First time setup - Via Windows Terminal">
  </p>
  </details>
- OsuExtractor GUI
  <details close>
  <summary>Preview</summary>
  <p align="center">
  <b>Work in progress</b>
  </p>
  </details>

# Downloads
- [OsuExtractor CLI](https://github.com/Dadangdut33/Osu-Extractor/releases/tag/V1.0_CLI)
- [OsuExtractor GUI]()

# How To Install
1. Download either the CLI or GUI version
2. Extract the rar file

# How To Uninstall
You only need to delete the folder.

# How To Compile It To .exe Yourself
1. Clone the repo
2. Setup virtualenviroment if needed then Install all the dependencies for the project.
```
# On source code directory
# Create a virtualenviroment with the name STL_Venv
python -m venv OsuExtractorVenv

# Activate the virtualenviroment
source OsuExtractorVenv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```
3. Run and test the source code
4. If everything works fine, then you can compile it to .exe by running the following command:
```
# The method below uses pyinstaller
# On Source Code Directory
# CLI Version
pyinstaller --paths OsuExtractorVenv/lib/site-packages OsuExtractor_CLI.spec

# GUI Version
# If you want to add console window, set console to true on the spec file
pyinstaller --paths OsuExtractorVenv/lib/site-packages OsuExtractor_GUI.spec
```
5. Done

# Disclaimer
I do not gain any money from this tool. I do not intend to support piracy of any kind. This tool is only made to help extracting/copying song/img/videos from a beatmap. You should support the creators of each song/images/videos you extract. I recommend tools such as [saucenao](https://saucenao.com/) and [tineye](https://tineye.com/) to find the original image and author. You should also support the original music artist by buying their songs/albums or by listening their song on official platform. 