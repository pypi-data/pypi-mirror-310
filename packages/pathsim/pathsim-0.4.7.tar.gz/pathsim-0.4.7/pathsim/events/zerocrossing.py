#########################################################################################
##
##                                  ZERO CROSSING EVENTS
##                                (events/zerocrossing.py)
##
##                                   Milan Rother 2024
##
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np

from ._event import Event


# EVENT MANAGER CLASS ===================================================================

class ZeroCrossing(Event):
    """
    Subclass of base 'Event' that triggers if the event function crosses zero. 
    This is a bidirectional zero-crossing detector. 
    
    Monitors states of solvers of stateful blocks and block outputs by evaluating an 
    event function (g) with scalar output and testing for zero crossings (sign changes). 

        g(outputs, states, time) -> event?

    If an event is detected, some action (f) is performed on the states of the blocks.

        g(outputs, states, time) == 0 -> event -> states = f(outputs, states, time)

    If a callback function (h) is defined, it is called with the states as args.

        g(outputs, states, time) == 0 -> event -> h(outputs, states, time)

    INPUTS : 
        blocks    : (list[block]) list of stateful blocks to monitor
        func_evt  : (callable: outputs, states, time -> float) event function, where zeros are events
        func_act  : (callable: outputs, states, time -> states) state transform function to apply for event resolution 
        func_cbk  : (callable: outputs, states, time -> None) general callaback function at event resolution
        tolerance : (float) tolerance to check if detection is close to actual event
    """

    def detect(self, t):
        """
        Evaluate the event function and check for zero-crossings
        """

        #evaluate event function
        result = self._evaluate(t)
            
        #unpack history
        _result, _t = self._history

        #check for zero crossing (sign change)
        is_event = np.sign(_result) != np.sign(result)

        #definitely no event detected -> quit early
        if not is_event:
            return False, False, 1.0
        
        #linear interpolation to find event time ratio (secant crosses x-axis)
        ratio = abs(_result) / np.clip(abs(_result - result), 1e-18, None)
        
        #are we close to the actual event?
        close = abs(result) <= self.tolerance

        return True, close, float(ratio)


class ZeroCrossingUp(Event):
    """
    Modification of standard 'ZeroCrossing' event where events are only triggered 
    if the event function changes sign from negative to positive (up). Also called
    unidirectional zero-crossing.
    """

    def detect(self, t):
        """
        Evaluate the event function and check for zero-crossings
        """
            
        #evaluate event function
        result = self._evaluate(t)
            
        #unpack history
        _result, _t = self._history

        #check for zero crossing (sign change)
        is_event = np.sign(_result) != np.sign(result)

        #no event detected or wrong direction -> quit early
        if not is_event or _result >= 0:
            return False, False, 1.0
        
        #linear interpolation to find event time ratio (secant crosses x-axis)
        ratio = abs(_result) / np.clip(abs(_result - result), 1e-18, None)
        
        #are we close to the actual event?
        close = abs(result) <= self.tolerance

        return True, close, float(ratio)


class ZeroCrossingDown(Event):
    """
    Modification of standard 'ZeroCrossing' event where events are only triggered 
    if the event function changes sign from positive to negative (down). Also called
    unidirectional zero-crossing.
    """

    def detect(self, t):
        """
        Evaluate the event function and check for zero-crossings
        """
        
        #evaluate event function
        result = self._evaluate(t)
            
        #unpack history
        _result, _t = self._history

        #check for zero crossing (sign change)
        is_event = np.sign(_result) != np.sign(result)

        #no event detected or wrong direction -> quit early
        if not is_event or _result <= 0:
            return False, False, 1.0
        
        #linear interpolation to find event time ratio (secant crosses x-axis)
        ratio = abs(_result) / np.clip(abs(_result - result), 1e-18, None)
        
        #are we close to the actual event?
        close = abs(result) <= self.tolerance

        return True, close, float(ratio)