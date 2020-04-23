from .exceptions import TDAAPIError
from .enums import DURATION
# from .enums import DURATION, ORDER_TYPE, COMPLEX_ORDER_STRATEGY_TYPE, LEG_TYPE


class OrderBuilder(object):
    def __init__(self,
                 quantity,
                 price,
                 duration='DAY',
                 orderType='MARKET',
                 orderStrategyType='SINGLE',
                 complexOrderStrategyType='NONE',
                 specialInstruction=None,
                 requestedDestination='AUTO',
                 childOrderStrategies=None,
                 priceLinkBasis=None,
                 priceLinkType=None,
                 stopPrice=0.0,
                 stopPriceLinkBasis=None,
                 stopPriceLinkType=None,
                 stopType=None,
                 taxLotMethod=None
                 ):
        if duration not in DURATION:
            raise TDAAPIError('Duration must be in {}'.format(duration))

        self._rep = {
            'duration': duration,
            'orderType': orderType,
            'complexOrderStrategyType': complexOrderStrategyType,
            'requestedDestination': requestedDestination,
            'stopPrice': 0,
            'stopPriceLinkBasis': stopPriceLinkBasis,
            'stopPriceLinkType': stopPriceLinkType,
            'stopPriceOffset': 0,
            'stopType': stopType,
            'priceLinkBasis': priceLinkBasis,
            'priceLinkType': priceLinkType,
            'price': price,
            'taxLotMethod': taxLotMethod,
            'orderLegCollection': [],
            'specialInstruction': specialInstruction,
            'orderStrategyType': orderStrategyType,
        }
        if childOrderStrategies is not None and orderStrategyType == 'TRIGGER':
            self._rep['childOrderStrategies'] = [{
                "orderStrategyType":"OCO",
                "childOrderStrategies": []
            }]

    def addOCOOrder(self, assetType, symbol, price, OCOQuantity, orderStrategyType='OCO', childOrderStrategyType='SINGLE', orderType="LIMIT", instruction="SELL", stopPrice=None):
        leg = self._rep['childOrderStrategies'][0]['childOrderStrategies']

        childLeg = {
            "orderStrategyType": childOrderStrategyType,
            "session":"NORMAL",
            "DURATION":self._rep['duration'],
            "orderType":orderType,
            "price":price,
            "orderLegCollection":[
                {
                    "instruction":"SELL",
                    "quantity":OCOQuantity,
                    "instrument":{
                        "assetType":assetType,
                        "symbol":symbol
                    }
                }
            ]
        }
        if stopPrice is not None:
            childLeg["stopPrice"] = stopPrice
        leg.append(childLeg)
        self._rep['childOrderStrategies'].append(leg)

    def addLeg(self, assetType, symbol, instruction, positionEffect, quantity, quantityType, type=None, putCall=None):
        leg = {
            'orderLegType': assetType,
            'instrument': {
                'assetType': assetType,
                'symbol': symbol,
            },
            'instruction': instruction,
            'positionEffect': positionEffect,
            'quantity': quantity,
            'quantityType': quantityType,
        }

        # if assetType == 'OPTION':
        #     leg['instrument']['type'] = type
        #     leg['instrument']['putCall'] = putCall
        # elif assetType == 'MUTUAL_FUND':
        #     leg['instrument']['type'] = type
        # elif assetType == 'CASH_EQUIVALENT':
        #     leg['instrument']['type'] = type
        # elif assetType == 'FIXED_INCOME':
        #     leg['instrument']['maturityDate'] = maturityDate
        #     leg['instrument']['variableRate'] = variableRate
        #     leg['instrument']['factor'] = factor
        self._rep['orderLegCollection'].append(leg)

    def to_json(self):
        return self._rep
