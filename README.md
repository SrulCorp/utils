# Utility Scripts by Acolyte

A collection of AI-generated or homemade scripts.

---

## Setup

You will need to complete the following steps once on a given computer to use these scripts. (Currently, detailed instructions are only available for Windows. If you're using a different operating system, ask someone with knowledge of Python and PowerShell.)

### 1. Install Python

1. Go to the [official Python website](https://www.python.org/) and download Python for Windows.
![image showing the button on the python website](docs/images/python-download.png)
2. Open the installer and follow the on-screen instructions. The default options should work fine for most users.

### 2. Download This Repository

1. On this GitHub page, look near the top for a green button labeled **Code** with a down arrow.
2. Click on it, then select **Download ZIP**.
![Image showing downloading the zip](docs/images/download-zip.png)
3. A zipped folder will download to your computer. Move it to a convenient location for easy access.

### 3. Opening the Repository

1. Locate the zipped folder in your file explorer, right-click on it, and select **Extract All**.
![Image showing the 'extract all' option](docs/images/extract1.png)
2. When the dialog box appears, click **Extract** (no changes are necessary).
3. Once extraction is complete, you'll see both a zipped folder and an unzipped folder with the same name. You can delete the zipped folder.
4. Open the unzipped folder, likely named **utils-main**.


## Running Scripts

You can run a script by double-clicking the file. If prompted to choose how to open it:
- Select the **Python** app for `.py` files.
- Select **PowerShell** for `.ps1` or `.ps` files.

(Advanced) You can also set up the python scripts to run via command prompt (on windows). Go to `C:/Users/<Your User>`, and create a file named `utils.cmd`. Open the file with notepad and paste the following into it:
`@echo off`
`python "<Path/To/Utils/Directory>" %*`
Replace `<Path/To/Utils/Directory>` with the path you extracted utils to.

Now, you can run a script by typing `./utils/<filename>`, with `<filename>` being the name of the script.


### Script Descriptions

TODO