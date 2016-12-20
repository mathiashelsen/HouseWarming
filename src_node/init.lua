require('ds18b20')

function sendTemperature()
	t1=ds18b20.read()
	print("Temperature :"..t1.."\n")
	url = <ADD URL FOR ADDING TEMP TO DB HERE>

	http.get(url, nil, function(code, data)
		if (code < 0 ) then
			print("HTTP request failed!\n")
			node.dsleep(60*1000000)
		else
			print("Going to sleep...")
			node.dsleep(60*1000000)
		end
	end)
end

pin = 4 --GPIO2
ds18b20.setup(pin)
t=ds18b20.read()
t=ds18b20.read()
print("Initialized DS18B20\n")
print("Temp:"..t.."\n")

wifi.setmode(wifi.STATION)
wifi.sta.eventMonReg(wifi.STA_GOTIP, sendTemperature)
wifi.sta.eventMonStart()
wifi.sta.config(<SSID>,<PASSWORD>)
wifi.sta.connect()
