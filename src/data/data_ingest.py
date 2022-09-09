import asyncio
import time
from azure_composants import *
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from data_collect import (
    collect_pollution_data,
    location_from_coordinates,
)


"""
    parse the a tuple of a data set so that a Stream Analytics job can study it
"""
def json_tuple(dataset, loc, i):
    return (
        ("{'loc': \"" + loc + '", ')
        + (str((dataset[i])["main"]) + str((dataset[i])["components"]))
        .replace("{", "")
        .replace("}", ", ", 2)
        + ("'dt': \"" + str((dataset[i])["dt"]) + '"}')
    ).replace("'", '"')

"""
    fill a batch with parsing collected data in order to send it to an event hub
"""
async def fill_batch(producer, data_list):
    event_data_batch = await producer.create_batch()
    for loc_i in range(len(data_list)):
        loc_data = data_list[loc_i]
        coordonates = loc_data["coord"]
        data = loc_data["list"]
        loc = location_from_coordinates(coordonates)

        for i in range(len(data)):
            tuple = json_tuple(data, loc, i)
            print(tuple)
            event_data_batch.add(EventData(tuple))
    return event_data_batch

"""
    Verify if new data has been added on sources since {update_time} seconds
    If yes, send it to an event hub to be processed
"""
async def send_recent_data(connect_str=CONN_STR, eventhub="", update_time=1):
    delta = update_time / 3600 / 24  # delta in days
    while True:
        await asyncio.sleep(update_time)
        recent_data = collect_pollution_data(delta)
        if (str((recent_data[0])["list"]) != "[]"): # if new real data has been added on OpenWeather
            print("new data incoming")
            await send_data(connect_str, eventhub, delta)

"""
    Create a producer and use it to fill a batch to send to an event hub
"""
async def send_data(connect_str=CONN_STR, eventhub="", delta=7):
    # Create a producer client to produce and publish events to the event hub.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=connect_str, eventhub_name=eventhub
    )

    collected_data = collect_pollution_data(delta)
    async with producer:
        event_data_batch = await fill_batch(producer, collected_data)
        await producer.send_batch(event_data_batch)
        # Send the batch of events to the event hub.

"""
    Reunite the last 2 functions by specifying how long it took to collect and send data to the hub
"""
async def send_all_data(connect_str=CONN_STR, eventhub="", update_time=1):
    start_time = time.time()
    await send_data(connect_str, eventhub)
    print("Send data in {} seconds.".format(time.time() - start_time))
    await send_recent_data(connect_str, eventhub, update_time)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(send_all_data(eventhub="datahub", update_time=60))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()
