from SoftSensor.SoftSensor_Admin.SoftSensorManager import SoftSensorManager


my_softsensor_manager = SoftSensorManager()
my_softsensor_manager.createSoftSensor("SQLExample")
my_softsensor_manager.createSoftSensor("MQTTExample")
my_softsensor_manager.createSoftSensor()
my_softsensor_manager.run()

