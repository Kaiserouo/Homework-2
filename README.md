# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

The complete information is provided below, the input token and output token is written as an alphabet and the amount is written in a parenthesis.

```
B(5) -> A(5.655321988655322)
A(5.655321988655322) -> D(2.4587813170979333)
D(2.4587813170979333) -> C(5.0889272933015155)
C(5.0889272933015155) -> B(20.129888944077443)
path: tokenB->tokenA->tokenD->tokenC->tokenB, tokenB balance=20.129888944077443
```

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

Slippage is a phenomenon that the actual price of the token is different from your expected price. This is most prevalent when the pool has not enough liquidity, and you trade so much tokens that your action would make the price fluctuate a lot.

Slippage is unavoidable, so the best Uniswap can do is to provide a revert mechanism when the actual token count you receive deviates too much from the token count you expected to get.

For example, `UniswapV2Router01::swapExactTokensForTokens` provides `amountOutMin`. If the actual token received is less than this amount, the transaction will revert.:
```solidity
function swapExactTokensForTokens(
    uint amountIn,
    uint amountOutMin,
    address[] calldata path,
    address to,
    uint deadline
) external override ensure(deadline) returns (uint[] memory amounts)
```

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

ref. https://ethereum.stackexchange.com/questions/132491/why-minimum-liquidity-is-used-in-dex-like-uniswap

This is to prevent the value of liquidity share to increase so much that almost no one else can provide liquidity to the pool anymore.

For example, if one person make a pool with 1 WEI and 2,000,000 USDT to make a ETH/USDT pool, and get 1 LP token as share. If anyone else want to provide 1 WEI worth of liquidity, they have to also provide 2,000,000 USDT into the liquidity pool, since there's only 1 LP token in there. i.e., one LP token is worth so much that almost no new liquidy provider can afford them. This can also be accomplished if someone donate a lot of USDT, per say.

But Uniswap's mechanism locks 1,000 LP token in the pool (by directly burning them), so in order to increase the liquidity share value by $1, you need to donate at least $1,000 into the pool. This makes the attack way harder than if there's only 1 LP tokens total.

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

The formula is:
```solidity
liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
```

First, if we consider `amount0 / _reserve0 == amount1 / _reserve1`, the formula can make sure that if the liquidity is added to the pool, the rest (previous minted) liquidity's value is unchanged.

> Assume we have tokenA x 1000 and tokenB x 2000 in the pool, and the total liquidity is 100 (so 1 LP token should worth tokenA x 10 + tokenB x 20), if we add tokenA x 100 and tokenB x 200 into the pool, we can get 10 LP token. Now we have tokenA x 1100 and tokenB x 2200 in the pool, and the total liquidity is 110. Note that 1 LP token is still worth tokenA x 10 + tokenB x 20.

Second, if we consider `amount0 / _reserve0 > amount1 / _reserve1` (vice versa in the opposite direction), then we effectively treat the additional `amount0` as donation. You can say it's an incentive to make people supply liquidity with `amount0 / _reserve0 == amount1 / _reserve1` (i.e., without changing the ratio), or say this constraint is to just avoid people getting more liquidity than they should.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

A sandwich attack is the kind of attack in which the attacker try to slip inside the window between the time when a user places a transaction and the time when the transaction is actually performed on the blockchain.

For example, assume Alice wants to buy tokenA at price 10, but Bob notices this transaction, and buys a lot of tokenA before Alice's transaction is processed. Now the price of tokenA is at price 15, and Alice's transaction is performed. This pushed the price of tokenA further to 20. Now Bob can sell the tokenA at price 20, profitting from the situation.
