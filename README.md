# Necessary Steps

Please run Redis in Docker before starting the server.
Please first install Docker (Latest).

https://docs.docker.com/engine/install/

Then run (Linux):

docker run --rm -p 6379:6379 redis:7

# Required Libraries

External software includes Redis Channel, which is needed to store the real-time rooms for the chat feature.
This requires both Docker and Redis to be running.
For the Redis layer to communicate with the client web sockets, we also need to install Django Channels (Latest).

Alternatively, pip install -r requirements.txt

pip install -U 'channels[daphne]'
pip install --upgrade openai
pip install Pillow
