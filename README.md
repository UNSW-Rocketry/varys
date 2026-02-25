# Project Varys

Project Varys is the live telemetry project which will stream real-time flight data from the rocket to the ground station. We are aiming to provide compatibility for 3 transmitters which will be Featherweight, BigRedBee and Telemega.

## Featherweight

We use the Featherweight ground station to receive a signal from the featherweight transmitter and when we connect it to a computer, we get access to the packets sent from the receiver through the serial port.

Currently, the grafana and questdb are run locally in docker.

In `featherweight_reader.py`, we receive the data from the serial port and then filter out the GPS_STAT packets, which can then either be printed out or logged in a file.

In `parse_gps_data.py`, we retrieve these packets as text form the reader script and then convert these into standardized json objects.

In `send_to_questdb.py`, we retrieve the json objects and send it into a QuestDB database.

To run varys,
1. Connect the ground station to your computer
2. Run `featherweight_reader.py`, `parse_gps_data.py` and `send_to_questdb.py` concurrently on 3 separate terminals
   
   (Make sure the that `featherweight_reader.py` is on the right port, for windows: COM3 or COM4.)

   (DISCLAIMER: 'featherweight_reader' will not work on WSL)
3. Run the docker compose file
4. Set up QuestDB as a datasource on Grafana
5. You're all set to make graphs and visualisations on Grafana!
