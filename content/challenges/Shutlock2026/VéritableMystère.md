---
title: "VéritableMystère - Shutlock 2025"
date: 2025-06-30
tags: ["reverse", "shutlock", "vm"]
---

This is a reverse engineering challenge built around a heavily obfuscated Python script.
Hidden inside is a compressed bytecode executed by a custom **virtual machine (VM)** that validates a secret input.

<!--more-->

## Introduction

I did this challenge for a school CTF project. The goal of this challenge is to understand the VM and recover the flag.

## Main Technique
- **Decompression**: the real logic is hidden using **bzip2** compression.
- **Deobfuscation**: variable names and structure are intentionally scrambled.
- **VM Reverse Engineering**: the script implements its own instruction set, registers, and execution loop.
- **Bytecode Analysis**: reconstruct the instructions and translate them into readable pseudo-code.
