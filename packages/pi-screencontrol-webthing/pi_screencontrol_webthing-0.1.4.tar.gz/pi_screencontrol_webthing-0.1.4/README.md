# pi_screencontrol_webthing
A web connected screen control of Raspberry Pi


The screen control package exposes a http webthing endpoint which supports activating the screen. E.g.
```
# webthing has been started on host 192.168.0.23

curl http://192.168.0.23:9122/properties 

{
"activated": true,
"log": "[2022-02-25T14:40:18]  XAUTHORITY=~pi/.Xauthority DISPLAY=:0 xset s 180\n
        [2022-02-25T14:40:18]  XAUTHORITY=~pi/.Xauthority DISPLAY=:0 xset dpms 180 180  180\n
        [2022-02-25T14:40:18]  XAUTHORITY=~pi/.Xauthority DISPLAY=:0 xset s 180\n
        [2022-02-25T14:40:18]  XAUTHORITY=~pi/.Xauthority DISPLAY=:0 xset dpms 180 180  180"
}
```


To install this software you may use [PIP](https://realpython.com/what-is-pip/) package manager such as shown below

```
sudo pip install pi_screencontrol_webthing
```

After this installation you may start the webthing http endpoint inside your python code or via command line using
```
sudo screen --command listen --port 9832
```
Here, the webthing API will be bind to the local port 9832

Alternatively to the *listen* command, you can use the *register* command to register and start the webthing service as systemd unit.
By doing this the webthing service will be started automatically on boot. Starting the server manually using the *listen* command is no longer necessary.
```
sudo screen --command register --port 9832
```  

