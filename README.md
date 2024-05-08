# WindowOpener
Living in a place without central ventilation, I still wanted to have automatically regulated room climate. Using 3D printing, I designed a system that could automatically open and close the window. Initially intended for my bedroom, the design proved too noisy. I repurposed the system for the bathroom, where it could automatically regulate the humidity. The window opener would open the bathroom window when taking a shower and close it again once the humid air was out. Such a system is not only convenient, but also saves energy by only opening the window as long as necessary.

Video: https://www.youtube.com/watch?v=BI4nM2m5Y50

## Hardware Design

While many commercial window opener systems use expensive linear actuators, I looked for a more cost-effective DIY solution. I opted for a continuous rotation RC servo motor for actuation, mounted on the window casement. This motor drives a large spur gear fixed to the window frame, with two end switches ensuring the motor stops when the window is fully opened or closed. Of course, the window can still be opened and closed manually.
I discovered the design limitation of this approach: the center of rotation of the stationary spur gear must align perfectly with the window hinge. While this approach works with my custom solution, such a requirement would not be feasible for commercial products.

## Software & Automation

The window opener is controlled by the popular ESP8266 microcontroller with built-in Wi-Fi. I programmed it using the ESPHome framework, which easily integrates with our Home Assistant home automation system. Additionally, I installed a Zigbee humidity sensor in the bathroom. I used pyscript on Home Assistant to automate the system, opening the window if the bathroom’s humidity exceeds the apartment’s average by a certain threshold and closing it once the humidity drops below a predefined level. For quick ventilation after using the toilet, one can press the IKEA TRADFRI Zigbee remote to open the window for 15 minutes. A long button press can also turn off the automatic opening, which is handy when taking a long bath.

