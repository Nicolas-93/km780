from enum import IntEnum

class Key(IntEnum):
    # Macros
    G1=0
    G2=1
    G3=2
    G4=3
    G5=4
    G6=5

    # Modes
    MR=6
    M1=7
    M2=8

    # AZERTY
    ESC=9
    TILDE=10
    TAB=11
    CAPS_LOCK=12
    LEFT_SHIFT=13
    LEFT_CTRL=14
    ONE=15
    LT_GT=16
    SUPER=17
    F1=18
    TWO=19
    A=20
    Q=21
    W=22
    LEFT_ALT=23
    # 24
    Z=25
    X=26
    F2=27
    THREE=28
    E=29
    S=30
    C=31
    # 32
    F3=33
    D=34
    # 35
    F4=36
    FOUR=37
    R=38
    F=39
    V=40
    FIVE=41

    # Utils
    BLOCK_WINKEY=42
    LUMINOSITY=43
    TIMER=44

    F5=45
    SIX=46
    T=47
    G=48
    B=49
    SPACE=50
    SEVEN=51
    Y=52
    H=53
    F6=54
    EIGHT=55
    U=56
    J=57
    N=58
    F7=59
    I=60
    K=61
    COMMA=62
    F8=63
    NINE=64
    O=65
    L=66
    SEMICOLON=67
    # 68
    F9=69
    ZERO=70
    # ZERO=71 // QWERTY ?
    CIRCUMFLEX=72
    RIGHT_PARENTHESIS=73
    P=74
    M=75
    TWO_POINTS=76
    ALT_GR=77
    EXCLAMATION_POINT=78
    RIGHT_SUPER=79
    # 80
    F11=81
    EQUAL=82
    F10=83
    U_GRAVE=84
    # 85
    MENU=86
    DOLLAR=87
    ASTERISK=88
    RIGHT_CTRL=89
    F12=90
    # 91
    # BACKSLASH=92 // QWERTY ?
    ENTER=93
    RIGHT_SHIFT=94
    LEFT_ARROW=95
    BACKSPACE=96
    UP_ARROW=97
    DOWN_ARROW=98
    PRINT_SCR=99
    INSERT=100
    DEL=101
    SCR_LOCK=102
    HOME=103
    END=104
    
    # Multimedia 1
    AUDIO_STOP=105
    AUDIO_PREV=106
    VOL_PAUSE=107

    PAUSE_BRK=108
    PAGE_UP=109
    PAGE_DOWN=110
    KP_4=111
    KP_1=112
    NUM_LOCK=113
    KP_7=114
    
    # Multimedia 2
    AUDIO_NEXT=115
    AUDIO_MUTE=116

    KP_SLASH=117
    KP_ASTERISK=118
    KP_8=119
    KP_5=120
    KP_2=121
    KP_0=122
    KP_9=123
    KP_6=124
    RIGHT_ARROW=125
    KP_ENTER=126
    KP_MINUS=127
    KP_PLUS=128
    KP_3=130
    KP_PERIOD=131

Key.MAX_INDEX = Key.KP_PERIOD
Key.LEN = Key.MAX_INDEX + 1