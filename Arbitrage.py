import copy
from typing import *

original_liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

# the global liquidity that can be changed
liquidity = copy.deepcopy(original_liquidity)

def getLiquidity(token_1, token_2) -> Tuple[float, float]:
    """
        get the liquidity of the 2 tokens, in order
    """
    if ord(token_1[-1]) > ord(token_2[-1]):
        a, b = liquidity[(token_2, token_1)]
        return (b, a)
    return liquidity[(token_1, token_2)]

def setLiquidity(token_1, token_2, amount_1, amount_2):
    """
        directly set the liquidity of the 2 tokens' pair, in order
    """
    if ord(token_1[-1]) > ord(token_2[-1]):
        liquidity[(token_2, token_1)] = (amount_2, amount_1)
    else:
        liquidity[(token_1, token_2)] = (amount_1, amount_2)
    
def getAmountOut(from_token, to_token, amount_in) -> float:
    """
        given input from_token count, return output to_token count
    """
    dx = amount_in
    x, y = getLiquidity(from_token, to_token)
    return 997 * dx * y / (1000 * x + 997 * dx)

def trade(from_token, to_token, amount_in):
    """
        perform trading from from_token to to_token
        will modify global variable liquidity
        
    """
    if from_token == to_token:
        # no-op
        return amount_in
    dx = amount_in
    x, y = getLiquidity(from_token, to_token)
    dy = getAmountOut(from_token, to_token, amount_in)
    setLiquidity(from_token, to_token, x+dx, y-dy)
    return dy

def getK(token_1, token_2):
    """
        get the K value for the 2 token.
    """
    a, b = getLiquidity(token_1, token_2)
    return a * b

def tradeByChain(chain, amount_in, do_print=False):
    """
        trade the token by chain
        e.g., chain = "BACB" -> the chain is 
        the chain should start and end with the same alphabet
    """
    for from_token, to_token in zip(chain, chain[1:]):
        orig_amount_in = amount_in
        amount_in = trade("token" + from_token, "token" + to_token, amount_in)
        if do_print:
            print(f"{from_token}({orig_amount_in}) -> {to_token}({amount_in})")
    return amount_in

def resetLiquidity():
    """
        reset the global liquidity to initial value,
        should be called when you wanna try a new chain
    """
    global liquidity
    liquidity = copy.deepcopy(original_liquidity)

if __name__ == '__main__':
    import itertools

    max_amount = 0
    max_chain = ""

    repeat = 3
    for ls in itertools.product(["A", "B", "C", "D"], repeat=repeat):
        resetLiquidity()
        chain = "B" + "".join(ls) + "B"
        amount = tradeByChain(chain, 5)
        # print(chain, amount)
        if amount > max_amount:
            max_amount = amount
            max_chain = chain

    # experiment found out that by simply iterating all 4**3 possibilities we can found a path of >20 tokenB
    # path: tokenB->tokenA->tokenD->tokenC->tokenB, tokenB balance=20.129888944077443
    print(f'path: {"->".join(["token" + token for token in max_chain])}, tokenB balance={max_amount}')