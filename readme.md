## How it works :construction_worker: .

First of all, there is a Thread which is checking the value of the Pin number 8 of Raspberry Pi and when it detected a low sign, it'll take a picture with PiCamera module, so it'll sent it to the endpoint that is defined at API_SERVER_HOST. Also, it has a endpoint which allow you to take a picture using the same PiCamera module

## Docs.

Please go to localhost:PORT/docs and you'll get the swagger info

### Run 

Make sure to give it privileges by using the flag -privileged by the time you run it 



