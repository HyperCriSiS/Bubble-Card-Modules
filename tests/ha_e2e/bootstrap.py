#!/usr/bin/env python3
"""Bootstrap only an ephemeral localhost Home Assistant; never touches production."""
import argparse
import json
import os
from pathlib import Path
import secrets
import time
from urllib.parse import urlparse

import requests

def require_loopback(base):
    parsed=urlparse(base)
    if parsed.scheme!="http" or parsed.hostname not in {"127.0.0.1","localhost"} or not parsed.port:
        raise ValueError("HA E2E bootstrap requires an explicit loopback http port")
    return base.rstrip("/")

def call(session,method,base,path,token=None,**kwargs):
    headers=kwargs.pop("headers",{})
    if token: headers["Authorization"]="Bearer "+token
    result=session.request(method,base+path,headers=headers,timeout=25,**kwargs)
    if not result.ok:
        raise RuntimeError(f"Isolated HA {method} {path}: HTTP {result.status_code}")
    return result.json() if result.content else {}

def ready(session,base,deadline=300):
    end=time.monotonic()+deadline
    while time.monotonic()<end:
        try:
            r=session.get(base+"/api/onboarding",timeout=3)
            if r.ok and isinstance(r.json(),list): return r.json()
        except (requests.RequestException,ValueError): pass
        time.sleep(2)
    raise TimeoutError("Isolated HA failed to start onboarding")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--base",default="http://127.0.0.1:8123")
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    base=require_loopback(args.base)
    session=requests.Session()
    steps={row["step"]:row["done"] for row in ready(session,base)}
    if steps.get("user"): raise RuntimeError("Refusing onboarding of an existing Home Assistant user")
    client_id=base+"/"
    username="vsc_e2e_"+secrets.token_hex(5)
    password=secrets.token_urlsafe(30)
    response=call(session,"POST",base,"/api/onboarding/users",json={
        "name":"VSC CI","username":username,"password":password,
        "client_id":client_id,"language":"en"
    })
    if not response.get("auth_code"): raise RuntimeError("Missing onboarding auth_code")
    token=call(session,"POST",base,"/auth/token",data={
        "client_id":client_id,"grant_type":"authorization_code",
        "code":response["auth_code"]
    })
    if not token.get("access_token") or not token.get("refresh_token"):
        raise RuntimeError("OAuth code exchange was incomplete")
    for step,params in (("core_config",{}),("analytics",{}),
                        ("integration",{"client_id":client_id,"redirect_uri":client_id})):
        if not steps.get(step):
            call(session,"POST",base,"/api/onboarding/"+step,
                 token=token["access_token"],json=params)
    expected={"light.vsc_main","light.vsc_child","light.vsc_group"}
    deadline=time.monotonic()+150
    last=set()
    while time.monotonic()<deadline:
        try:
            states=call(session,"GET",base,"/api/states",token=token["access_token"])
            last={x["entity_id"] for x in states}
            if expected.issubset(last): break
        except (requests.RequestException,RuntimeError):
            pass
        time.sleep(2)
    else:
        raise RuntimeError("HA virtual fixture entities missing: "+str(sorted(expected-last)))
    auth={"hassUrl":base,"clientId":client_id,
          "expires":round(time.time()*1000)+int(token["expires_in"])*1000,
          "refresh_token":token["refresh_token"],"access_token":token["access_token"],
          "expires_in":token["expires_in"]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    fd=os.open(args.output,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as file:
        json.dump(auth,file)
    args.output.chmod(0o600)
    print("Isolated HA onboarding and real API fixture verified (3 virtual lights)")

if __name__=="__main__": main()
