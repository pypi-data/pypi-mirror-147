# Introduction

Pygeon makes it super easy to send yourself custom push notifications

## Install Pygeon

```
pip install pygeon-notifications
```

## Usage with Python (>= 3.3)
Install and open the Pygeon app on your mobile (iOS only) and sign-in. After signing in you will recieve a private key. Use the private key to instantiate a Pygeon object that you can use to send push notifications anywhere in your scripts

#### example
```
from pygeon import Pygeon
my_pygeon = Pygeon("YOUR_PRIVATE_KEY")

my_pygeon.send("Cool Title", "Even cooler description")
```

## Usage with POST requests

The Pygeon python package under the hood is a simple program that sends a POST request to Pygeon servers. Hence you can send notifications using a simple POST request to `https://pygeon.io/api/sendnotification` with your private key, title and description in the body of the request.

### curl example

```
curl -X POST "https://pygeon.io/api/sendnotification" -H 'Content-Type: application/json' -d '{"ppk":"YOUR_PRIVATE_KEY","title":"Cool Title", "desc": "Cool Body"}'

```

### node example

```
const axios = require('axios')

axios.post('https://pygeon.io/api/sendnotification', {
    ppk: 'YOUR_PRIVATE_KEY',
    title: 'Cool Title',
    desc: 'Even cooler description'
  })
  .then(res => {
    console.log(`statusCode: ${res.status}`)
    console.log(res)
  })
  .catch(error => {
    console.error(error)
  })
```

