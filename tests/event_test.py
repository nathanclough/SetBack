from setback import BidUpdateEvent,GameStartedEvent
import json

def to_json(event):
    return json.loads(json.dumps(event, default=lambda o: o.__dict__, sort_keys=True, indent=4))

def test_convert_bid_update():
    event = GameStartedEvent()
    event.current_bidder= "31151235"

    json_event = to_json(event)
    converted = GameStartedEvent.from_json(json_event)

    assert converted.current_bidder == event.current_bidder
    assert converted.player_id == event.player_id


    