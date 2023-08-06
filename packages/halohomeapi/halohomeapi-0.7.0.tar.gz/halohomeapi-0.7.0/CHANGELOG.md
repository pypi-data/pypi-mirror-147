# Changelog

## 0.5.0 2022-01-25

- Sort devices by RSSI before connecting to avoid unnecessary delay

## 0.4.0 2021-11-08

(BREAKING)

- Remove support for `user_id` (username/email is sufficient)
- Support offline loading of devices (e.g. in case of internet outage)

## 0.3.0 2021-10-25

- Read `user_id` to provide a permanent ID for the HALO Home account

## 0.2.1 2021-10-23

- Raise HaloHomeError when credentials are not valid

## 0.2.0 2021-10-21

- Support mesh communication (only need to connect to a single device
  to control all of them)
- Make network and bluetooth connections async

## 0.1.0 2021-10-17

- Initial release
