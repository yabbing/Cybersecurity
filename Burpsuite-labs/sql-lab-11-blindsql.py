import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http: 127.0.0.1:8080', 'https: 127.0.0.1:8080'}

def main():
   if len(sys.argv) != 2:
      print("(+)" Usage: %s <url>" % sys.argv[0])
      print("(+ )Example: %s http://target.com/vulnerable_endpoint" % sys.argv[0])

      If __name__ == "__main__":
        main()