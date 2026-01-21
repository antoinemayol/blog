---
title: "StrangeQuery - Shutlock 2025"
date: 2025-06-30
tags: ["web"]
categories: ["Challenges"]
description: "This is a web security challenge targeting a movie platform called Netflute. It combines a logic flaw with a subtle database vulnerability to ultimately leak sensitive data using SQLI 2nd order."
---

## Introduction

I created this challenge for a school CTF project 📚.
The goal is to exploit multiple vulnerabilities chained together to extract secrets from the database.

## Main Techniques
- **Privilege Escalation via Cookies**: a client-side cookie controls access to admin-only features.
- **Logic Flaw Abuse**: user verification can be triggered without proper authorization.
- **Second-Order Blind SQL Injection**: malicious input is stored first, then executed later in a different context.
- **Automated Exploitation**: the injection can be exploited using tools like `sqlmap`.

## Your turn

To try this challenge, download the [given files](/blog/files/Shutlock2025/Web/StrangeQuery/StrangeQuery.zip) and run the application locally.

Go in the directory source, and run `docker compose up`, once done the website will be available at `http://localhost:5000/`.

If you get stuck, a full writeup is available in `solution/Solution.md`.
PS: It’s written in French 🤓
