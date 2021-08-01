from enum import IntEnum


class Rank(IntEnum):
    T = 10
    jo = 11
    JO = 12
    ja =13
    JA = 14
    Q = 15
    K = 16
    A = 17
    
normal_ranks = [2,3,4,5,6,7,8,9,Rank.T,Rank.JA,Rank.Q,Rank.K,Rank.A]

     