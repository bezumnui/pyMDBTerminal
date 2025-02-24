from enum import Enum


class CashlessMasterParameter(Enum):
    VMCSlaveAddress = "vmc-slave-address"  # 0x10 or 0x60 - Sets the address of the cashless device
    VMCFeatureLevel = "vmc-feature-level"  # 2 or 3 - Sets the feature level of the VMC
    VMCMinPrice = "vmc-min-price"  # 0x0000 to 0xFFFF - Sets the minimum price of the VMC
    VMCMaxPrice = "vmc-max-price"  # 0x0000 to 0xFFFF - Sets the maximum price of the VMC
    VMCDisplayColumns = "vmc-display-columns"  # 0 to 255 - Tells the reader how many columns are on the VMC's display
    VMCDisplayRows = "vmc-display-rows"  # 0 to 255 - Tells the reader how many rows are on the VMC's display
