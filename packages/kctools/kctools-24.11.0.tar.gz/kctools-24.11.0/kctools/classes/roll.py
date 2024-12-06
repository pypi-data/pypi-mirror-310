import inspect
import numpy as np
import pandas as pd

from .cache import cached
from ..kctools import invert

####################################

_CARDS = 'akqj09'
_NORM  = len(_CARDS)**2

_ORDER = [
    'aa', 'a0', 'a9', 'ak', 'aq', 'aj',
    'kk', 'qq', 'jj', 'kq' ,'qj', 'kj',
    'k0', 'j9', 'q0', 'q9', 'j0', 'k9',
    '00', '09', '99'
]

_WINS = [
    'aa', 'a0', 'a9'
]

_UPSETS = {
    'j9': ['kk'],
    'j0': ['qq'],
    'k0': ['jj'],
    'q9': ['kq'],
    'k9': ['qj'],
    'q0': ['kj']
}

_REVERSE = invert(_UPSETS)

########################################################################

def dist_norm(data):
    to = max( x._exp() for x in data )
    return [ x.scale(to=to) for x in data ]

def dist_aggr(data, counts = None):
    if counts is None:
        counts = R.MULTS
    assert len(counts) == len(data)
    return sum( (x*y for x, y in zip(counts, data)) , start = WinDist() )

####################################

class WinDist():

    def __init__(self, roll = None, target = None):
        
        self.norm = 0
        self.wins = 0
        self.outs = np.zeros(len(_ORDER), dtype=int)
        self.tars = np.zeros(len(_ORDER), dtype=int)
        
        if roll or target:
            assert roll and target
            roll = R(roll)
            target = R(target)
            self.norm += 1
            self.wins += int(roll > target)
            self.outs[roll.rank] += 1
            self.tars[target.rank] += 1
            
    def __repr__(self):
        return f"{self.wins/self.norm:>6f} -- NORM: {self.norm:>7} : WINS: {self.wins:>7} : outs: [{', '.join(f'{x:>5}' for x in self.outs)} ] : tars: [{', '.join(f'{x:>5}' for x in self.tars)} ]"
    
    ################################
    
    def _copy(self):
        copy = WinDist()
        copy.norm = self.norm
        copy.wins = self.wins
        copy.outs = self.outs.copy()
        copy.tars = self.tars.copy()
        return copy
    
    def _dict(self):
        return {
            'norm': self.norm,
            'wins': self.wins,
            'outs': self.outs.tolist(),
            'tars': self.tars.tolist(),
        }
    
    def roll(self):
        if np.count_nonzero(self.outs) == 1:
            rank = np.where(self.outs)[0][0]
            return R(_ORDER[rank])
        return '--'
    
    def validate(self):
        try:
            assert self.wins <= self.norm
            assert self.outs.sum() == self.norm
            assert self.tars.sum() == self.norm
            assert isinstance(self._exp(), int)
        except:
            print('VALIDATION ERROR:', self._dict())
            raise
        return self
    
    ################################
    
    def _key(self):
        a = self.wins / self.norm
        b = (-self.outs * np.arange(len(_ORDER))).sum()
        return (a, b)
    
    def __gt__(self, other):
        return self._key() > other._key()
    
    def __lt__(self, other):
        return self._key() < other._key()
    
    def __ge__(self, other):
        return self._key() >= other._key()
    
    def __le__(self, other):
        return self._key() <= other._key()
    
    def __eq__(self, other):
        return self._key() == other._key()
        
    def __ne__(self, other):
        return self._key() != other._key()
    
    ################################
    
    def __add__(self, other):
        copy = self._copy()
        copy.norm += other.norm
        copy.wins += other.wins
        copy.outs += other.outs
        copy.tars += other.tars
        return copy
    
    def __sub__(self, other):
        copy = self._copy()
        copy.norm += other.norm
        copy.wins += other.norm - other.wins
        copy.outs += other.tars
        copy.tars += other.outs
        return copy
    
    def __neg__(self):
        return WinDist() - self._copy()
    
    def __mul__(self, y):
        copy = self._copy()
        copy.norm *= y
        copy.wins *= y
        copy.outs *= y
        copy.tars *= y
        return copy
    
    def __rmul__(self, y):
        return self.__mul__(y)
    
    def __div__(self, y):
        return self.__mul__(1/y)
    
    def __rdiv__(self, y):
        return self.__mul__(1/y)

    ################################
    
    def _exp(self):
        if self.norm:
            e = 0
            while e < 8:
                if self.norm == _NORM ** e:
                    return e
                e += 1
            return np.log(self.norm) / np.log(_NORM)

    def scale(self, by = 0, to = None):
        if to is not None:
            by += to - self._exp()
        s = _NORM ** by
        s = int(s) if s == int(s) else s
        self *= s
        return self

########################################################################

class R(str):

    def __new__(cls, x = 'aa'): # __new__ not __init__ because we're subclassing str
        if isinstance(x, R):
            return x
        assert len(x) == 2
        x = x.lower()
        assert all(i in _CARDS for i in list(x))
        x = ''.join(sorted(list(x), key = lambda x: _CARDS.index(x)))
        assert x in _ORDER
        obj = str.__new__(cls, x)
        obj.mult = 1 + (x[0] != x[1])
        obj.rank = _ORDER.index(x)
        return obj

    ################################

    ###  self  >  target 
    
    def __gt__(self, target):
        target_rank = _ORDER.index(str(target))
        if self.rank == target_rank:
            return self.lower() in _WINS # (x < b ) != (b > x)
        else:
            if str(self) in _UPSETS:
                if str(target) in _UPSETS[str(self)]:
                    return True
            return self.rank < target_rank
    
    def __lt__(self, target):
        return not self.__gt__(target)
    
    def __ge__(self, target):
        return self.__gt__(target)
    
    def __le__(self, target):
        return self.__lt__(target)
    
    def __eq__(self, target):
        return False
        
    def __ne__(self, target):
        return True
    
    def __hash__(self):
        return str.__hash__(self) 
    
    ################################

    @cached
    def options(self, *, highest = False, naive = False, target = None, semi = None):
        options = [ 'keep' ]
        if set(self).intersection('kqj'):
            options.append('roll')
            if not (highest or naive or target):
                options.append('delay')
        return options

    @cached
    def replacements(self, other):
        orig = set(self).intersection('kqj')
        if not orig:
            return [self]
        reps = set(other).intersection('kqj')
        reps = reps or set(other).intersection('09')
        reps = reps or set(other)
        reps = list(set([ R(i+j) for i in orig for j in reps ]))
        return reps

    ################################
    
    @cached
    def wins(self, *, highest = False, naive = False, target = None, semi = None):
        if highest:
            wins = WinDist()
            wins.norm = 1
            wins.wins = - self.rank
            wins.outs[self.rank] += 1
            return wins
        if naive:
            wins = []
            for roll in map(R, _ORDER):
                vals = self.wins(target=roll)
                wins.append(vals)
            wins = dist_norm(wins)
            wins = dist_aggr(wins)
        elif target:
            wins = WinDist(self, target)
        elif semi:
            wins = - semi.roll_wins(target=self)  
        else:
            wins = - self.chances(target=self)
        return wins
    
    ################################

    @cached
    def choose(self, other, *, highest = False, naive = False, target = None, semi = None):
        if highest:
            roll = max(self.replacements(other))
            wins = roll.wins(highest=highest)
            return wins
        else:
            data = []
            for roll in self.replacements(other):
                wins = roll.wins(naive=naive, target=target, semi=semi)
                data.append(wins)
            return sorted(data)[-1]

    ################################
    
    @cached
    def roll_wins(self, *, highest = False, naive = False, target = None, semi = None):
        wins = []
        for roll in map(R, _ORDER):
            vals = self.choose(roll, highest=highest, naive=naive, target=target, semi=semi)
            wins.append(vals)
        wins = dist_norm(wins)
        wins = dist_aggr(wins)
        return wins

    @cached
    def option_wins(self, opt, *, highest = False, naive = False, target = None, semi = None):
        if opt == 'keep':
            wins = self.wins(highest=highest, naive=naive, target=target, semi=semi)
        elif opt == 'roll':
            wins = self.roll_wins(highest=highest, naive=naive, target=target, semi=semi)
        elif opt == 'delay':
            if not semi:
                wins = - R().chances(highest=highest, naive=naive, target=target, semi=self)
            else:
                wins = - semi.roll_wins(highest=highest, naive=naive, target=target, semi=self)
        wins.opt = opt
        return wins

    @cached
    def optimal(self, *, highest = False, naive = False, target = None, semi = None):
        data = []
        for opt in self.options(highest=highest, naive=naive, target=target, semi=semi):
            wins = self.option_wins(opt, highest=highest, naive=naive, target=target, semi=semi)
            data.append(wins)
        return sorted(data)[-1]  

    ################################

    @cached
    def chances(self, *, highest = False, naive = False, target = None, semi = None):
        wins = []
        for roll in map(R, _ORDER):
            vals = roll.optimal(highest=highest, naive=naive, target=target, semi=semi)
            wins.append(vals)
        wins = dist_norm(wins)
        wins = dist_aggr(wins)
        return wins

########################################################################

# adds constants to (exposed) class

R.CARDS   = _CARDS
R.NORM    = _NORM
R.WINS    = list(map(R, _WINS))
R.ORDER   = list(map(R, _ORDER))
R.MULTS   = [ x.mult for x in R.ORDER ]
R.UPSETS  = { R(k): [ R(v) for v in vals ] for k, vals in _UPSETS.items() }
R.REVERSE = invert(R.UPSETS)

########################################################################

# caches everything

R().chances(highest=True)
R().chances(naive=True)
R().chances()

########################################################################
