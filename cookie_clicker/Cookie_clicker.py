"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(50)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 1000.0 

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        "Initializing local Variables"
        self._total_cookies_produced = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        
        # Initiating list of history containing time, item bought at time, 
        # cost of the item, total number of coockies produced
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        state = "\n"
        state += ("Total coockies produced :" + str(self._total_cookies_produced) + "\n")
        state += ("Current coockies :" + str(self._current_cookies) + "\n")
        state += ("Current time : " + str(self._current_time) + "\n")
        state += ("Current cps : " + str(self._current_cps) + "\n")
                  
        return state
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        waiting_time = 0.0
        # if already have enough cookies
        if cookies <= self._current_cookies:
            waiting_time = 0.0
        
        # time to get given cookies
        else:
            waiting_time_in_fraction = (cookies - self._current_cookies) / float(self._current_cps)
            waiting_time = float(math.ceil(waiting_time_in_fraction))
        
        return waiting_time
            
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        
        else:
            self._current_time += time
            self._current_cookies += (self._current_cps * time)
            self._total_cookies_produced += (self._current_cps * time)
            
                
                           
        
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        # adjust current_cookie, modified cps and history 
        if self._current_cookies < cost:
            return
        else:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, 
                                 cost, self._total_cookies_produced))
            
        
        
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    clone_build_info = build_info.clone()
    clicker_state = ClickerState()
    
    while clicker_state.get_time() <= duration:
        item = strategy(clicker_state.get_cookies(), clicker_state.get_cps(), 
                        clicker_state.get_history(), (duration - clicker_state.get_time()),
                        clone_build_info)
        if item == None:
            break
        
        needed_cookie = clone_build_info.get_cost(item) 
        if needed_cookie > 0:
            wait_time = clicker_state.time_until(needed_cookie)
            if (clicker_state.get_time() + wait_time) > duration:
                break
            clicker_state.wait(wait_time)
        clicker_state.buy_item(item, clone_build_info.get_cost(item), 
                               clone_build_info.get_cps(item))
        clone_build_info.update_item(item)
        
    if clicker_state.get_time() < duration:
        clicker_state.wait(duration - clicker_state.get_time())
    
    return clicker_state



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
    cheapest_cost = float('inf')
    cheapest_item = ""
    item_list = build_info.build_items()
    for item in item_list:
        if build_info.get_cost(item) < cheapest_cost:
            cheapest_cost = build_info.get_cost(item)
            cheapest_item = item
    if (cookies + cps * time_left) < cheapest_cost:
        return None
    else:
        return cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    max_afford = cookies + cps * time_left
    expensive_cost = float('-inf')
    expensive_item = ""
    item_list = build_info.build_items()
    for item in item_list:
        if ((build_info.get_cost(item) > expensive_cost) 
            and (build_info.get_cost(item) <= max_afford)):
            expensive_cost = build_info.get_cost(item)
            expensive_item = item 
    # return None if no item is affordable
    if expensive_cost < 0:
        return None
    else:
        return expensive_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    if strategy_cheap(cookies, cps, history, time_left, build_info) == None:
        return None
    
    best_item = ""
    best_production = 0
    item_list = build_info.build_items()
    affordable_cost = cps * time_left
    affordable_list = []
    for item in item_list:
        if build_info.get_cost(item) < affordable_cost:
            affordable_list.append(item)
    for item in affordable_list:
        total_production = cookies
        current_cps = cps
        time_remain = time_left
        item_cost = build_info.get_cost(item)
        while (affordable_cost >= item_cost) or ((item_cost / current_cps) < time_remain):
            total_production += item_cost
            time_remain -= (item_cost / current_cps)
            affordable_cost = (current_cps * time_remain)            
            item_cost *= 1.15
            current_cps += build_info.get_cps(item)
        if time_remain > 0 :
            total_production += (time_remain * current_cps)
        if total_production > best_production:
            best_production = total_production
            best_item = item
    return best_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    
    
#x = ClickerState()
#print x
#x.wait(10.0)
#print x
#x.buy_item('item', 1.0, 3.5)
#print x
#print x.get_history()
#dic = {'Cursor': [15.0, 0.10000000000000001], 'Grandma': [100.0, 0.5]}

#print simulate_clicker(provided.BuildInfo(dic, 1.15), 300.0, strategy_cheap)

