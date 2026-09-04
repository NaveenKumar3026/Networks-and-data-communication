import asyncio
import ssl

from aioquic.asyncio.client import connect
from aioquic.h3.connection import H3Connection
from aioquic.h3.events import (
    HeadersReceived,
    DataReceived
)
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import ProtocolNegotiated


class HTTP3Client:

    def __init__(self):
        self.response_data = b""
        self.headers = []

    async def request(self, host, path="/"):

        configuration = QuicConfiguration(
            is_client=True,
            alpn_protocols=["h3"]
        )

        # Enable certificate verification
        configuration.verify_mode = ssl.CERT_REQUIRED

        async with connect(
            host,
            443,
            configuration=configuration
        ) as protocol:

            # Create HTTP/3 connection
            http = H3Connection(protocol._quic)

            # Allocate a stream
            stream_id = protocol._quic.get_next_available_stream_id()

            # Send HTTP/3 request headers
            headers = [
                (b":method", b"GET"),
                (b":scheme", b"https"),
                (b":authority", host.encode()),
                (b":path", path.encode()),
                (b"user-agent", b"Python HTTP/3 Client"),
            ]

            http.send_headers(
                stream_id=stream_id,
                headers=headers,
                end_stream=True
            )

            protocol.transmit()

            # Receive response
            while True:

                event = await protocol.wait_for_event()

                if event is None:
                    break

                if isinstance(event, HeadersReceived):

                    print("\nHTTP/3 Response Headers:")

                    for name, value in event.headers:
                        print(
                            name.decode(),
                            ":",
                            value.decode()
                        )

                elif isinstance(event, DataReceived):

                    self.response_data += event.data

                    if event.stream_ended:
                        break

        # Save webpage
        with open("downloaded_page.html", "wb") as file:
            file.write(self.response_data)

        print("\nWeb page downloaded successfully!")
        print("Saved as downloaded_page.html")


async def main():

    host = input(
        "Enter HTTP/3 website (example: cloudflare-quic.com): "
    )

    client = HTTP3Client()

    await client.request(host)


asyncio.run(main())