# Ufile.io [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fgautamajay52%2Fufile.io&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://github.com/gautamajay52/ufile.io)

> Asynchronous Python Wrapper for the Ufile API (Unofficial).

### Installation :
```bash
pip3 install ufile.io
```

### Usage :
```python
>> from ufile import Ufile

>> ufile = Ufile(api_key='<YOUR API KEY>') # <YOUR API KEY> is your ufile api key

# or

>> ufile = Ufile() # as a guest

# to upload
>> data = await ufile.upload_file(file='/path/to/text.bin')
>> print(data)
{'id': 9111424, 'url': 'https://ufile.io/2j9mqrug', 'destination': 'https://ufile.io/2j9mqrug', 'name': 'test.bin', 'filename': '2j9mqrug-1g3er.bin', 'slug': '2j9mqrug', 'size': '10.0 MB', 'type': 'other', 'expiry': '&infin;', 'location': '6'}

>> file_url = data['url']

>> direct_url = await ufile.download_file(url='https://ufile.io/2j9mqrug')
>> print(direct_url)
https://cdn-eu-hz-1.ufile.io/get/2j9mqxug?token=MDY2NzA4NDU4MzE0MGQwYmJmNWY2MjAyMjU5ZDI0ZDI2NGI3OWVhMTEwOGNiYzZkMzA0YjY0M2FiMTY1YWM2NzJmMjAwYzI2MjFjM2U4NGUwZGE2YmYzNTc1MmU0NzljN2JhZTQ3NDZmNmZjNjM2NTk0NTkwY2YwMGQ1OTliYTJxcmtxOTNKbXdRS3N3L1Y2aWZ6ZTNza2gwU1BQS2huayt2ckNwaFV2K2V6L01wR1ZaREtNalFmeG93T0Q4elBIcHFXOVZVemhRWDd5UUR4UmF4d0VlK2lXQ0ZkMllUYjNuT0RWQ0xtMlU1elBYjF1WG9Xbjg5Qll0Mm90ZVdheUlVeUVJMWkrRWcwUUxSUkVHK1lKaEdlV1RyeVhvcGZjYUR0MTM1ZjBvMVBrOXRhSW53WTdtMjFZTTk1dmpObXZHT3ZaZFc0Ukl2U2VDeDdRPT0=

>> await ufile.delete_file(file_id=9111424)
```
### Credits: ⚡
* [GautamKumar(me)](https://github.com/gautamajay52) for [Nothing](https://github.com/gautamajay52/ufile.io)