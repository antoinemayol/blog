---
title: "Ret2win — Grehack 2025"
date: 2025-11-29
tags: ["pwn", "grehack", "ret2win", "blind"]
---

This challenge was a simple blinf re2win

<!--more-->

## Introduction

This challenge was a simple blind ret2win.

## Solving

First it was necessary to find the right offset that seem to crash the program.

Once find, the offset can be used to spray the return address and find an interesting address.

Here is the [script](/blog/files/grehack2025/ret2win/solve.py) that solved it.
