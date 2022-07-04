from fastapi import FastAPI, Path, Query 
import datetime as dt
from typing import Optional
from pydantic import BaseModel, Field
app = FastAPI()
trades = {
    1: {
        "assetClass": "BOND",
        "counterparty": "dell",
        "instrumentId": "TSLA",
        "instrumentName": "tesla",
        "tradeDateTime": "2022-07-02T10:57:07.948Z",
        "tradeDetails": {
        "buySellIndicator": "buy",
        "price": 20,
        "quantity": 50
        },
        "tradeId": "1",
        "trader": "Malika"
}
}
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")

@app.get("/")
def index():
    return {"Message" : "here are the end points for this project"}
    return {"name" : "First API"}
# getting trade using tradeid
@app.get("/get-trade/{trade_id}")
def get_trade(trade_id : int = Path(None, description="enter The Id you want to view.",)):
    if trade_id not in trades:
        return {"error": "trade doesnot exists"}
    return trades[trade_id]

@app.post("/create-trade/{trade_id}")
def create_trade(*, trade_id: int = Path(None, description="create a trade with id:"), trade: Trade):
    if trade_id in trade:
        return {"Error" : "trade exists"}

    trades[trade_id] = trade
    return trades[trade_id]

@app.get("/find-trade")
def find_trade(search: str):
    for trade_id in trades:
        if trades[trade_id]["counterparty"] == search:
            return trades[trade_id]
        elif trades[trade_id]["instrumentId"] == search:
            return trades[trade_id]
        elif trades[trade_id]["instrumentName"] == search:
            return trades[trade_id]
        elif trades[trade_id]["trader"] == search:
            return trades[trade_id]
        return {"Data" : "Not found"}

