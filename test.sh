#!/bin/bash
# NOTE
# Every time, remember to change userToken to something different
curl 'https://vps.kodub.com/v6/leaderboard' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-GB,en;q=0.9,de;q=0.8' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Origin: https://app-polytrack.kodub.com' \
  -H 'Referer: https://app-polytrack.kodub.com/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw 'version=0.6.2&userToken=4fd8f07049a4d5fbe32c40892e33cbf2403b8b2e5ea479f8edd90e0fc78de87&nickname=Anonymous&carStyle=AAAAAC13Fv___xMTE2ZmZg&trackId=95e4bf5c2a76b49ad1ce0f7fd9d6ca777a09aaf6492f9a7415afde3427a8ac66&frames=1&recording=eNpjYmD4zMuQyczAxMDwnpUhnIGBhQEEHBkYljEymDCAxBU5GezAggB8WwRG&onlyVerified=false'
