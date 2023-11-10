## Testing xAmbit API


  1. Check the code in `client` dir
  2. Set a callback URL in the constant `LOCAL_PROXY_URL` where you can receive xAmbit API callback.
     Use a tool like ngrok for this. You can run `ngrok http 8000` to setup a reverse proxy.
  3. Setup `XAMBIT_API_URL`, `X_HOST` and `X_KEY` parameters. You can get them from xAmbit admin panel.
     All such parameters are marked with `< >` in the code.
  4. run the client using `python3 xambit_client.py <path to a local pdf file>`. Note that ngrok reverse
     proxy must be setup before calling the client script.
  5. After 2-10 minutes depending on filetype, response from xAmbit API will be received on the callback URL

Note that the client intentionally uses only standard library (instead of requests/flask etc) to reduce
installation/setup overhead.
