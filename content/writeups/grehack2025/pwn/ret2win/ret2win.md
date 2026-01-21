# Ret2win - Grehack2025

## Introduction

This challenge was a simple blind ret2win.

## Solving

First it was necessary to find the right offset that seem to crash the program.

Once find, the offset can be used to spray the return address and find an interesting address.

Here is the [script](/blog/files/grehack2025/ret2win/solve.py) that solved it.
