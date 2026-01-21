---
title: "VéritableMystère - Shutlock 2025"
date: 2025-06-30
categories: ["Challenges"]
description: "This is a reverse engineering challenge built around a heavily obfuscated Python script. Hidden inside is a compressed bytecode executed by a custom virtual machine (VM) that validates a secret input."
tags: ["reverse"]
---

## Introduction

I did this challenge for a school CTF project 📚. The goal of this challenge is to understand the VM and recover the flag.

## Main Technique
- **Decompression**: the real logic is hidden using **bzip2** compression.
- **Deobfuscation**: variable names and structure are intentionally scrambled.
- **VM Reverse Engineering**: the script implements its own instruction set, registers, and execution loop.
- **Bytecode Analysis**: reconstruct the instructions and translate them into readable pseudo-code.

## Your turn

To try this challenge download the [given files](/blog/files/Shutlock2025/Reverse/VéritableMystère/VéritableMystère.zip), and start the challenge with the file `source/VéritableMystère.py`.

If at any point you are stuck, feel free to look at the writeup at `solution/Solution.md`.
PS: It's written in French 🤓
