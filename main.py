import time
import sys
import traceback
import os

import requests
import dotenv

dotenv.load_dotenv()


def get_dns_info(zone_id: str, name: str) -> str:
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        'X-Auth-Key': f"{os.getenv('CLOUDFLARE_API_KEY')}",
        'X-Auth-Email': f"{os.getenv('CLOUDFLARE_EMAIL')}",
        'Content-Type': 'application/json',
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        dns_records = response.json()['result']
        for dns_record in dns_records:
            if dns_record['name'] == name:
                return dns_record
    except:
        print(traceback.format_exc())
    return None


def update_dns_record(zone_id, dns_record_name, ip):
    dns_record_info = get_dns_info(zone_id, dns_record_name)
    if dns_record_info is None:
        print(f"DNS record {dns_record_name} not found")
        return None

    if dns_record_info['content'] == ip:
        print(f"DNS record {dns_record_name} is already up-to-date")
        return None

    dns_record_id = dns_record_info['id']
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}'
    headers = {
        'X-Auth-Key': f"{os.getenv('CLOUDFLARE_API_KEY')}",
        'X-Auth-Email': f"{os.getenv('CLOUDFLARE_EMAIL')}",
        'Content-Type': 'application/json',
    }
    data = {
        'type': 'A',
        'name': dns_record_name,
        'content': ip,
    }
    try:
        response = requests.patch(url, headers=headers, json=data, timeout=30).json()
        return response
    except:
        print(traceback.format_exc())
        return None


def get_ip():
    while True:
        try:
            return requests.get('https://api.ipify.org', timeout=30).text
        except:
            print(traceback.format_exc())
            time.sleep(30)


def on_new_ip(interval_minute, callback):
    previous_ip = None
    while True:
        try:
            ip = get_ip()
            if ip is not None and ip != previous_ip:
                previous_ip = ip
                callback(ip)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print(traceback.format_exc())

        time.sleep(interval_minute * 60)


def on_new_ip_callback(ip):
    print(update_dns_record(os.getenv('ZONE_ID'), os.getenv('DNS_RECORD_NAME'), ip))


on_new_ip(5, on_new_ip_callback)
