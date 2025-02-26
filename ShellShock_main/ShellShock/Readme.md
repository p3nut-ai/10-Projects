# Chrome Extension: ShellShock

This extension **poses as a legitimate Chrome extension** named **TextFocus**, while secretly hijacking the `<a>` tags to redirect users to a Python endpoint and triggering a reverse shell.


## Features

- **Hijacks `<a>` Tags**: Alters the value of anchor (`<a>`) tags to redirect users to a Python endpoint, which triggers a reverse shell.
- **Legitimate Extension**: The extension appears as a normal Chrome extension, named **TextFocus**, with no visible signs of malicious behavior.
- **Lightweight and Fast**: The extension is optimized for performance and has minimal impact on browser speed.

## Installation

1. Clone or download this repository to your local machine.
2. Open Google Chrome and navigate to `chrome://extensions/`.
3. Enable **Developer mode** in the top right corner.
4. Click on the **Load unpacked** button.
5. Select the folder containing the extension files.
6. The extension will now appear in your extensions list as **TextFocus**.


## Chrome Extension
![alt text](https://media.discordapp.net/attachments/1305451657357819926/1318642990562021376/image.png?ex=6763117c&is=6761bffc&hm=1e2c9808eabaf87c7e947248e99628c02f95c52eb7b9ae1780b82befb83a0ac3&=&format=webp&quality=lossless)

## Usage

1. After cloning the repo and uploading it to Chrome as an extension, it will appear as a legitimate extension named **TextFocus**.
2. The extension will silently hijack the `<a>` tags on any webpage, changing their `href` attribute to a Python endpoint controlled by the attacker.
3. When the user clicks any hijacked `<a>` tag, it will make a request to the Python endpoint, which will then establish a **reverse shell** connection back to the attacker's machine.

## Files

- **manifest.json**: Configuration file for the Chrome extension.
- **content.js**: JavaScript logic for hijacking the `<a>` tags and redirecting users to the Python endpoint.

## How It Works

1. **Redirect Hijacking**: The extension scans all the `<a>` tags (`<a href="...">`) in the webpage. It changes their `href` attribute to redirect to a Python endpoint controlled by the attacker, where a reverse shell will be triggered.

2. **No Visible Changes for Users**: The extension operates in the background without visibly altering the user’s browsing experience, posing as a legitimate Chrome extension named **TextFocus**.

3. **Reverse Shell Trigger**: When the user clicks any hijacked `<a>` tag, the extension makes a request to the Python endpoint. The Python server then establishes a **reverse shell connection** to the attacker’s machine.

4. **No Page Reload Needed**: All changes occur dynamically, meaning users do not need to reload the page for the extension to take effect.

---

**Important Note:** This project is for **educational purposes only**. **Do not** use it for malicious activities. Ensure you have permission before testing on any system. Misuse of this tool can have serious legal consequences.
