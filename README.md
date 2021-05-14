# CC-P2_GBV

This practice consists of developing a complete system for predicting temperature and humidity for a given location. For this development, it must cover all aspects of the
process, such as the collection of data, the processing, the storage or the publication of services among many others. With this, what is achieved is the deployment of a Cloud service Complete native from source code acquisition, to container execution and finally deploy the service that will finally deliver an API of type HTTP RESTful that for
the prediction of temperature and humidity.

For this final API you must have at least the following operations, separated into two versions, 1 and 2:

Service code version 1 (will go for containerized CI / CD)

HTTP GET
EndPoint 1 → / service / v1 / prediction / 24hours /

HTTP GET
EndPoint 2 → / service / v1 / prediction / 48hours /

HTTP GET
EndPoint 3 → / service / v1 / prediction / 72hours /

Service code version 2 (will go for containerized CI / CD)

HTTP GET
EndPoint 4 → / service / v2 / prediction / 24hours /

HTTP GET
EndPoint 5 → / service / v2 / prediction / 48hours /

HTTP GET
EndPoint 6 → / service / v2 / prediction / 72hours /

The functionality of each of the above EndPoints is to make a prediction of Humidity and Temperature for 3 intervals: 24, 48 and 72 hours. This functionality has been
implemented as a tool (or function in Python) to predict based on various input parameters and is available on the practice website link for temperature1
as for humidity for version 1, where ARIMA is used to predict 2 both for 24 following hours. For version 2 it will be necessary to use other prediction models, for example
using another algorithm such as neural networks, random forest, etc.

The input and output interface of this prediction tool receives 2 parameters:
a) the data set, and
b) the value of the hours (dataset, hours)
and returns a set of JSON predictions with the following data:

[Predictions every hour: 13:00 14:00,…. Instead of every 5 mins.]

[

{"Hour": 13:05, "temp": 32.20, "hum": 85.90},

{"Hour": 13:10, "temp": 31.20, "hum": 86.30},

...
]

This data returned by the prediction function is what must be sent from the API and the EndPoints to the user.
