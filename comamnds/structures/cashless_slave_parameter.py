from enum import Enum


class CashlessSlaveParameter(Enum):
    MDBAlwaysIdle = "mdb-always-idle" # 0 or 1 - When enabled, the Cashless Device supports
    # Always Idle(Selection First) operation. Note: even when enabled,
    # if the machine does not support this mode, it may still choose not to use it,
    # using Idle Mode (Authorization First) instead.
    MDBCurrencyCode = "mdb-currency-code" # 0x1<ISO 4217 numeric currency code> - Set cashless currency code (see appendix
    # A of the MDB specification ) in brief:
    # 1840 is USD, 1978 is Euro, 1756 is CHF, 1826 is GBP
    MDBFTLEnabled = "mdb-ftl-enabled" # 0 or 1 - Makes the Cashless Peripheral announce FTL Capability to the VMC
    MDBAddress = "mdb-address" # 0x10 or 0x60 - Cashless device address
    MDBDecimalPlaces = "mdb-decimal-places" # 0 to 3 - Set number of decimal digits (increase precision and decrease maximum limit)
    MDBScaleFactor = "mdb-scale-factor" # 1 to 100 - Multiplier to increase/decrease maximum value allowed
    # for transactions (used in undervalue currency)
    MDBTimeout = "mdb-timeout" # 1 to 10000000000 - MDB message timeout (seconds)
    MDBTimeoutIdle = "mdb-timeout-idle" # 0 to 10000000000 - Idle session timeout (seconds)
    MDBTimeoutVend = "mdb-timeout-vend" # 0 to 10000000000 - Vend confirm timeout (seconds)
    MDBCashSaleEnabled = "mdb-cashsale-enabled" # 0 or 1 - Indicate to the VMC that it should inform the cashless implementation about Cash sales
    MDBRestoreFunds = "mdb-restore-funds" # 0 or 1 - Tells the VMC that the Cashless Device is able to restore funds to the Cards or not
    MDBDisplayTime = "mdb-display-time" # Positive Integer - Allows configuration of the time which the messages displayed with the Display Request command will be presented in the VMC screen.





