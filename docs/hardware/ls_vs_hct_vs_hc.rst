LS vs. HCT vs HC
================

SN54/74HCT CMOS Logic Family Applications and Restrictions
https://www.ti.com/lit/an/scla011/scla011.pdf


Noise and interference
----------------------

.. note::
    To summarize, inherent noise remains below the critical limits within a pure
    TTL or HC system. When HCT devices are used, the maximum line length should
    not exceed 10 cm to maintain crosstalk below critical values. Because the
    logical application of HCT devices is interfacing between HC and TTL circuits,
    and line lengths are normally shorter, this requirement presents no serious
    restriction.


HCT only for interfacing
-------------------------

.. note::
    Thus, the HCT family offers an ideal, simple, and cost-effective solution
    for mixing systems using both TTL and HC devices. However, employing HCT
    instead of HC devices in pure CMOS systems cannot be recommended.