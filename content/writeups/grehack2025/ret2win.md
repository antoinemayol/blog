---
title: "Ret2win - Grehack 2025"
date: 2025-11-29
tags: ["pwn"]
categories: ["Writeups"]
image: /images/grehack2025.png
hidden: true
description: "This challenge is a simple blind ret2win."
---

## Introduction

This challenge was solved while participating to an annual cyber security event done in Grenoble ⛰️ in France 🇫🇷.

## Solving

First it was necessary to find the right offset that seem to crash the program.

Once find, the offset can be used to spray the return address and find an interesting address.

Here is the [script](/blog/files/grehack2025/ret2win/solve.py) that solved it.
