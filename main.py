import time
import sys
import traceback
import os

import requests

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    print("Note: Not using .env file.")
    pass


def get_list_dns_info(zone_id: str, name: str, type_filter: list) -> list:
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        'X-Auth-Key': f"{os.getenv('CLOUDFLARE_API_KEY')}",
        'X-Auth-Email': f"{os.getenv('CLOUDFLARE_EMAIL')}",
        'Content-Type': 'application/json',
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        dns_records = response.json()['result']

        dns_records_found = []
        for dns_record in dns_records:
            if dns_record['name'] == name and dns_record['type'] in type_filter:
                dns_records_found.append(dns_record)

        return dns_records_found
    except:
        print(traceback.format_exc())
    return None


def update_dns_record(zone_id, dns_record_name, ip, ipv6 = None):
    list_dns_info = get_list_dns_info(zone_id, dns_record_name, ['A', 'AAAA'])
    if list_dns_info is None:
        print(f"Failed to retrieve DNS records for {dns_record_name}")
        return None
    if len(list_dns_info) == 0:
        print(f"DNS record {dns_record_name} not found")
        return None

    if ipv6 is not None and len(list_dns_info) < 2:
        print(f"DNS {dns_record_name} does not have enough records for dual-stack.")
        print("Falling back to IPv4 only.")
        ipv6 = None

    list_dns_content = map(lambda x: x['content'], list_dns_info)
    ipv4_updated = False
    if ip in list_dns_content:
        print(f"DNS record {dns_record_name} for IPv4 is already up-to-date")
        ipv4_updated = True
    ipv6_updated = False
    if ipv6 is not None and ipv6 in list_dns_content:
        print(f"DNS record {dns_record_name} for IPv6 is already up-to-date")
        ipv6_updated = True

    if ipv4_updated and (ipv6 is None or ipv6_updated):
        print("No updates needed for DNS records.")
        return None

    headers = {
        'X-Auth-Key': f"{os.getenv('CLOUDFLARE_API_KEY')}",
        'X-Auth-Email': f"{os.getenv('CLOUDFLARE_EMAIL')}",
        'Content-Type': 'application/json',
    }
    dns_record_id = list_dns_info[0]['id']
    dns6_record_id = list_dns_info[1]['id'] if ipv6 is not None else None
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}'
    url6 = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns6_record_id}' if ipv6 is not None else None
    data = {
        'type': 'A',
        'name': dns_record_name,
        'content': ip,
        'proxied': True,
    }
    data6 = {
        'type': 'AAAA',
        'name': dns_record_name,
        'content': ipv6,
        'proxied': True,
    } if ipv6 is not None else None

    try:
        response = requests.patch(url, headers=headers, json=data, timeout=30).json()
        response6 = requests.patch(url6, headers=headers, json=data6, timeout=30).json() if ipv6 is not None else None
        return response, response6
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

def get_ipv6():
    while True:
        try:
            return requests.get('https://api6.ipify.org', timeout=30).text
        except requests.exceptions.ConnectionError:
            print("IPv6 not available.")
            return None
        except:
            print(traceback.format_exc())
            time.sleep(30)

def on_new_ip(interval_minute, callback):
    previous_ip = None
    previous_ipv6 = None
    while True:
        try:
            ip = get_ip()
            ipv6 = get_ipv6()
            if (ip is not None and ip != previous_ip) or (ipv6 is not None and ipv6 != previous_ipv6):
                print(f"New IP detected: IPv4: {ip}, IPv6: {ipv6}")
                previous_ip = ip
                previous_ipv6 = ipv6
                callback(ip, ipv6)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print(traceback.format_exc())

        time.sleep(interval_minute * 60)


def on_new_ip_callback(ip, ipv6=None):
    print(update_dns_record(os.getenv('ZONE_ID'), os.getenv('DNS_NAME'), ip, ipv6))


if __name__ == '__main__':
    on_new_ip(15, on_new_ip_callback)
