# The idea behind the server

## Connection

The connection between the client and the server are made through the
`socket` library in single thread mode (the server
can only have 1 client at a time).\
<br>
The client must send a json format string to the server.
This string should look like `{'url': '/<url>', ...}`. Which
the server will parse in the `tools/server_tools.py parse_package` function
and return a dict.\
<br>
The server should return a json format string in response.
This string should look like `{'code': <code: int>, ...}`.

## Server routing function

The server routing function is needed to process the incoming packet,
and call the wrapper function of a specific URL.
The URL is stored under the key `'url'` in the package

## Client authorization

Client authorization is a mandatory function when connecting.
It returns a token, without which it is impossible to
access other server urls. _If I'm not too lazy, all transmitted data will be
encrypted with this key._ The key consists
of a **string** of the dict format, which consists of the client's ip address,
the client's hostname and the current
time of the server, the string hashed with the sha256 algorithm.

#### Token example

Input data:

```json
{
  "ip": "127.0.0.1",
  "hostname": "hacknet-fedoralinux",
  "time_stamp": "2022-08-26 12:09:22.563332"
}
```

Output data:

```json
{
  "code": 200,
  "token": "df57ab35b16d7cec24d0440e1e151407cacddc269166ba9b8592d02aae22f39d"
}
```

## Storing the current connection

The connection token is stored in the file `app/data/connection/TOKEN`

<br>
<br>

### List of error codes:

| **Code** | **Decryption**                                  |
|----------|-------------------------------------------------|
| 200      | Success                                         |
| 400      | Error in package which server got(mb wrong url) |
| 500      | Error on server side                            |

___

Author: [Konstantin-create](https://github.com/Konstantin-create)
\
Licence: [GNU General Public License v3.0](/LICENSE)
