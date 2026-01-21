---
title: "Chifoumi - Grehack 2025"
date: 2025-11-29
tags: ["pwn"]
categories: ["Writeups"]
image: /images/grehack2025.png
description: "This challenge is a small game where you must beat a bot multiple times to reach a vulnerable password prompt."
---

## Introduction

This challenge was solved while participating to an annual cyber security event done in Grenoble ⛰️ in France 🇫🇷.

The password input of this challenge is vulnerable to a stack-based buffer overflow, which allows code execution.

The difficulty is not the overflow itself, but reliably **winning the game**, since the bot’s moves are generated using `rand()`.

We are given:
- `game_patched`
- `libc.so.6`
- `ld-linux-x86-64.so.2`

You can download those files [here](/blog/files/grehack2025/Chifoumi/challpwn.tar.gz).

---

## Game Logic

Each round, the bot chooses its move with:

```c
bot_move = rand() % 3;
```

If we win 31 rounds, the program prints:

Password :

The winning move is simply:

(my_move = (bot_move + 1) % 3)

So if we can predict rand(), we win every round.
Predicting the Bot (PRNG Abuse)
Leaking the Seed

The menu has an option that prints logs. Inside those logs, a value called token is printed:

```
token: <number>
```

This value is used to seed the PRNG.

By selecting the log option and parsing the output, we can recover the exact seed.
Reproducing rand() Locally

The binary uses glibc’s rand().
We can reproduce the exact same random sequence locally using ctypes:

```
libc2 = ctypes.CDLL("libc.so.6")
libc2.srand(seed)
libc2.rand()  # sync
```

After that, every call to libc2.rand() matches the bot’s moves.
Auto-Winning the Game

```
for i in range(31):
    bot_move = libc2.rand() % 3
    my_move = (bot_move + 1) % 3
    send(my_move)
```

This reliably brings us to the password prompt.

### Buffer Overflow

The password is read into a fixed-size stack buffer without bounds checking.

By sending 200+ bytes, we overwrite the saved return address and gain control of execution.

However, ASLR is enabled, so we need a libc leak first.
### Stage 1 – Leaking libc

We build a small ROP chain to call puts on its own GOT entry:

puts(puts@GOT)
return to main

This leaks the runtime address of puts.

From that, we compute the libc base:

libc_base = leaked_puts - libc.symbols["puts"]

### Stage 2 – Getting Back to the Password

After leaking libc, the program returns to the menu.
The PRNG seed changes, so we simply:

- Read logs again
- Extract the new seed
- Re-sync rand()
- Win the game again

Now we reach the password prompt with libc fully resolved.

### Stage 3 – ret2libc

With the libc base known, we prepare the final payload:

[pop rdi] [/bin/sh] [system]

A single ret gadget is added before pop rdi to keep the stack 16-byte aligned.

This results in:

```
system("/bin/sh");
```

## Result

We get a shell and can read the flag:

```
$ cat flag
flag{...}
```

You can look at the [solve.py](/blog/files/grehack2025/Chifoumi/solve.py).
