"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """        
        dummy_str = ("Total Cookies: " + str(self._total_cookies) +
        ", Current Cookies: " + str(self._cookies) +
        ", Time: " + str(self._time) +
        ", CPS: " + str(self._cps))        
        return dummy_str
    
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies
    
    def set_cookies(self, cookies):
        """
        Updates current number of cookies 
        (not total number of cookies)
        
        Returns nothing.
        """
        self._cookies = cookies 
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def set_cps(self, cps):
        """
        Set current CPS

        Returns nothing.
        """
        self._cps = cps        
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def set_time(self, time):
        """
        Set current time

        Returns nothing.
        """
        self._time = time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        dummy_history = self._history
        return dummy_history
    
    def set_history(self, event):
        """
        Adds new event to history.
        
        Retutns nothing.
        """
        self._history.append(event)
        
    def get_total_cookies(self):
        """
        Get total cookies.
        
        Should return a float.
        """
        return self._total_cookies
    
    def set_total_cookies(self, cookies):
        """
        Updates total cookies
        
        Returns nothing.
        """
        self._total_cookies = cookies

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies > self.get_cookies():
            return math.ceil((cookies-self.get_cookies())/self.get_cps())
        return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self.set_cookies(self.get_cookies()+self.get_cps()*time)
            self.set_total_cookies(self.get_total_cookies()+self.get_cps()*time)
            self.set_time(self.get_time()+time)
            return
        return
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self.get_cookies():
            self.set_cookies(self.get_cookies() - cost)
            self.set_cps(self.get_cps() + additional_cps)
            self.set_history((self.get_time(), item_name, cost, self.get_total_cookies()))
            return
        return
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    # clones build_info and creates ClickerState object (the game)
    build_info_clone = build_info.clone()
    game = ClickerState()
    
    # Checks if game time has not passed duration
    while game.get_time() <= duration:
        time_left = duration - game.get_time()
        
        print game
        # print "Time Left:", str(time_left)
        
        # Chooses next item to buy passed on strategy
        next_item = strategy(game.get_cookies(), game.get_cps(), game.get_history, time_left, build_info_clone)

        # Ends loop if no more items are avaliable	
        if next_item == None:
            game.wait(time_left)
            return game
            
        # Check whether we can have enough cookies to buy item without waiting
        if game.get_cookies() >= build_info_clone.get_cost(next_item):
            time_to_next_item = 0
        else:
            time_to_next_item = game.time_until(build_info_clone.get_cost(next_item))
            
        # Check whether we have enough time to wait to buy item            
        if time_to_next_item > (time_left):
            game.wait(time_left)
            break
        else:
            game.wait(time_to_next_item)
        
        # Buy item
        game.buy_item(next_item, build_info_clone.get_cost(next_item), build_info_clone.get_cps(next_item))
        build_info_clone.update_item(next_item)
    return game

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    
    # Find the cheapest item
    cheapest_name = ''
    cheapest_price = float("inf")    
    for item in build_info.build_items():
        if build_info.get_cost(item) < cheapest_price:
            cheapest_price = build_info.get_cost(item)
            cheapest_name = item

    # Return the cheapest item if you can afford in the time left       
    if (cookies+cps*time_left) < cheapest_price:         
        return None
    else:
        return cheapest_name

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    
    cookies_left = cookies+cps*time_left
    expensive_price = 0
    expensive_name = None
    
    for item in build_info.build_items():
        if build_info.get_cost(item) <= cookies_left:
            if expensive_price < build_info.get_cost(item):
                expensive_price = build_info.get_cost(item)
                expensive_name = item    
    
    return expensive_name

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    cookies_left = cookies+cps*time_left
    best_cookies = float("inf")
    best_name = None
    
    for item in build_info.build_items():
        if build_info.get_cost(item) <= cookies_left:
            if best_cookies > (build_info.get_cost(item)/build_info.get_cps(item)):
                best_cookies = build_info.get_cost(item)/build_info.get_cps(item)
                best_name = item          
    return best_name
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    # run_strategy("Cursor", 5000.0, strategy_none)    

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
#run()


# simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 5000.0, strategy_none) 