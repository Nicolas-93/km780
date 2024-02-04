# Protocol

The first several bytes, probably eight, identify the purpose of the packet. Usually only the first few bytes are significant. Trailing zeros are elided for simplicity.

When the software talks to the keyboard, it does so in what I'll call a transaction. The transaction is introduced by 0x070d00, and committed by 0x070d01. Intermediate settings changes appear to take effect immediately, but it seems that they have to be committed to be saved to NVRAM.

## Packet ``07 02 {#mode}`` Seems to be common, and contains various settings
Third byte seems to be the mode number (0x01, 0x02, 0x03).
The software send this packet twice : while editing mode X, it will send a configuration packet for the first time, and later in the transaction, all of the three mode configuration, even though they did not change.

|Byte index | Dec Index | Description |
|----------:|:----------|:------------|
|5? * 0x00  | 0         | Padding |
|0x08       | 8         | Polling Rate (0x08=125Hz, 0x04=250Hz, 0x02=500Hz 0x01=1000Hz) |
|0x0b       | 11        | Brightness from lighting tab (0x00, 0x01, 0x02, 0x03, 0x04) |
|0x6a       | 106       | Disable lighting (0x01=disable, 0x00=enable) |
|0x77       | 119       | Volume (On : 0x00, Off : 0x01) |
|// 0x62    |           | Timer Key Wait value |
|// 0x66    |           | LED Sleep Wait value |


## Packets ``07 0A {#mode} *``
Third byte seems to be the mode number (M1=0x1B, M2=0x1C, M3=0x1D).

### Packet ``07 0A {#mode} 09`` :

### Packet ``07 0A {#mode} 0A`` :

| Byte Index | Description |
|-----------:|:------------|
| 4? * 0x00 | Padding ? |
| 0x08 | ? |
| 0x09 | ? |
| 0x0A | ? |
| 0x0B | ? |
| 0x0C | Repeat Delay (1x = 0x00, 2x = 0x01, 4x = 0x02, 8x = 0x03) |

## Setting static colors to the keys
* 0702{#mode} @6a = 0 to disable effect
* 0709{#mode}{color} (0-2=R,G,B) Maps of red, green, and blue values for the keys.

## Setting the Wave effect
* ``070a1b00`` @08 Wave Effect name
* ``070a1b01`` @08 Wave Effect notes (Oddly, the Windows software does not allow spaces here)
* ``070a1b02`` @08 Wave Effect parameters
  * @00 Unknown
  * @01 Duration
  * @02 Direction (up=0, down=1, left=2, right=3)
  * @03 Number of colors in the gradient
  * @04 Array of gradient entries in the form of 3 bytes of  color as RRGGBB, one byte brightness (0-64), one byte for the gradient position (0-64?) 
