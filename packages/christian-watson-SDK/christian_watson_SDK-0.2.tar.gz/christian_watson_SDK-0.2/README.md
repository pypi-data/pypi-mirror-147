# Lord of the Rings Python SDK

The Lord of the Rings Python SDK enables Python developers an easy way to access LOTR related info in their apps.

## Quickstart

`$ pip install christian_watson_SDK`

    from christian_watson_SDK import LOTRClient

    client = LOTRClient('YOUR_API_KEY_ENV_VARIABLE')

    movies = await client.movies()
