# Python standard libraries
import json
import os
import sqlite3
import redis

import dash
import requests
from dash import html
import dash_enterprise_auth


# Third party libraries
from flask import Flask, redirect, request, url_for, session
from flask_session import Session
from oauthlib.oauth2 import WebApplicationClient
import redis
import requests
import flask
import google_auth_oauthlib.flow
import googleapiclient.discovery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from googleapiclient.discovery import build
from models import engine, User

Sessionmaker = sessionmaker(bind=engine)


def register_auth_routes(server, app, session):
    # Configuration
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
    CLIENT_SECRETS_FILE = "megaphone_client_secret.json"

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send",
    ]

    def credentials_to_dict(credentials):
        return {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }

    # @server.route("/login")
    # def login():
    #     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    #         CLIENT_SECRETS_FILE, scopes=SCOPES
    #     )
    #     flow.redirect_uri = url_for("callback", _external=True)

    #     authorization_url, state = flow.authorization_url(
    #         access_type="offline",
    #         include_granted_scopes="true",
    #     )

    #     # Store the state so the callback can verify the auth server response.
    #     session["state"] = state
    #     print(session.values)
    #     print("state set")
    #     print(session["state"])

    #     return redirect(authorization_url)

    @server.route("/login/callback")
    def callback():
        # print(session.keys())
        # try:
        #     state = session["state"]
        # except:
        #     return redirect(url_for("login"))

        # 1. get email
        # 2. check if exists in db
        # exists = session.query(User.id).filter_by(email=email).first() is not None
        # 3. if exists, set credentials in db under existing user and authenticated=True
        # 4. else, create new user

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES, state=session["state"]
        )
        flow.redirect_uri = url_for("callback", _external=True)

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = flask.request.url
        flow.fetch_token(authorization_response=authorization_response)

        # TODO store credentials in db

        credentials = flow.credentials
        with Sessionmaker() as db_session:
            db_session.query(User).filter_by(
                de_username=dash_enterprise_auth.get_username()
            ).update(
                {
                    "google_refresh_token": credentials.refresh_token,
                    "recent_token": credentials.token,
                }
            )
            db_session.commit()
            db_session.close()
            print("updated user record with refresh token and token")

        session["credentials"] = credentials_to_dict(credentials)
        print(credentials_to_dict(credentials))

        print("credentials added to session")
        return redirect(url_for("index"))

    @server.route("/logout")
    def logout():
        if "credentials" in session:
            del session["credentials"]
        return redirect(app.get_relative_path("/"))

    def get_google_provider_cfg():
        return requests.get(GOOGLE_DISCOVERY_URL).json()

    return
