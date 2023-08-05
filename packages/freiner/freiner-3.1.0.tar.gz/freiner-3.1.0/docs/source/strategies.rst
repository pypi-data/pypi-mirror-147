.. _ratelimit-strategy:

========================
Rate Limiting Strategies
========================

.. _fixed-window:

Fixed Window
============

Implemented using :class:`freiner.strategies.fixed_window.FixedWindowRateLimiter`.

This is the most memory efficient strategy to use as it maintains one counter
per resource and rate limit. It does however have its drawbacks as it allows
bursts within each window - thus allowing an 'attacker' to bypass the limits.
The effects of these bursts can be partially circumvented by enforcing multiple
granularities of windows per resource.

For example, if you specify a rate limit of ``100/minute``, this strategy will
allow 100 hits in the last second of one window and a 100 more in the first
second of the next window. To ensure that such bursts are managed, you could
utilise a second rate limit of ``2/second``, hitting them both on every attempt
for access.

.. _fixed-window-elastic:

Fixed Window with Elastic Expiry
================================

Implemented using :class:`freiner.strategies.fixed_window_elastic.FixedWindowElasticExpiryRateLimiter`.

This strategy works almost identically to the Fixed Window strategy with the exception
that each hit results in the extension of the window. This strategy works well for
creating large penalties for breaching a rate limit.

For example, if you specify a rate limit of ``100/minute``, and it is being attacked
at the rate of 5 hits per second for 2 minutes - the attacker will be locked out of
the resource for an extra 60 seconds after the last hit. This strategy helps circumvent
bursts.

.. _moving-window:

Moving Window
=============

Implemented using :class:`freiner.strategies.moving_window.MovingWindowRateLimiter`.

.. note:: The moving window strategy is only implemented for the ``redis`` and ``in-memory``
    storage backends. The strategy requires using a list with fast random access which
    is not very convenient to implement with ``memcached``.

This strategy is the most effective for preventing bursts from by-passing the rate limit
as the window for each limit is not fixed at the start and end of each time unit (i.e.
``N/second`` for a moving window means ``N`` in the last 1000 milliseconds). There is
however a higher memory cost associated with this strategy as it requires ``N`` items to
be maintained in memory per resource and rate limit.
