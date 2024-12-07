
# AXtendedKey

Hassle-free Accessibility (AX) permissions for Xcode builds.

## Quickstart Guide

**Summary**

Want to build an app in Xcode with accessibility (AX) permissions?

You have a problem. Xcode will ask you to approve permissions after _every_
build.

<img width="573" alt="ax-permission-prompt" src="https://github.com/user-attachments/assets/5db5d115-9aff-43de-80d8-b421c6356acb">

And your app still won't work.

This tool fixes that.

### Install via PyPI Package

Install AxtendedKey with your favorite PyPI installer.

```shell
pip install AxtendedKey
```

### Generate AX-Enabled Certificate

This tool works by self-signing a certificate, which grants `codesign` the ability to build with AX permissions.

```shell
axtended-key --verbose generate
```

The certificate is imported into the default macOS keychain.

### Undo

Remove the certificate at any time to completely undo anything this tool has done.

<img width="814" alt="keychain-certificate" src="https://github.com/user-attachments/assets/4e19a529-1632-43a7-ac4b-d969b668257c">



