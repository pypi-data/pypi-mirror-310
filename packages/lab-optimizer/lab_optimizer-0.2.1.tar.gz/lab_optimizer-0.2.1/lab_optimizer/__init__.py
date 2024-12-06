from .local_optimize import local_optimize
from .mloop_optimize import mloop_optimize
from .torch_optimize import torch_optimize
from .global_optimize import global_optimize
from .optimize_base import *

"""
``func`` should be a callable match the optimizer
and func should return a dict {"cost":cost,"uncer":uncer,"bad":bad}

cost : float -> cost value
uncer : float -> uncertainty of the cost
bad : bool -> whether the run is bad (bad = True represent bad run)

you are suggested to calculate uncer and bad, but they are required only in mloop_optimize,
and uncer and bad will not be used in other optimizers 

call th optimization algorithm ``XXX_optimize``

    `` XXX_optimize(func,paras_init,args,bounds,extra_dict,kwargs) ``

Args
--------
fun : callable
    The objective function to be minimized.

        ``fun(x, *args) -> dict : {'cost':float, 'uncer':float, 'bad':bool}``
        
    where ``cost`` is the value to minimize, ``uncer`` is uncertainty,
    ``bad`` is the judge whether this value is bad (bad = True) for this cost

    ``x`` is a 1-D array with shape (n,) and ``args``
    is a tuple of the fixed parameters needed to completely
    specify the function.

paras_init : ndarray, shape (n,)
    Initial guess. Array of real elements of size (n,),
    where ``n`` is the number of independent variables.

args : tuple, optional
    Extra arguments passed to the objective function which will not
    change during optimization
    
bounds : sequence or `Bounds`, optional
    Bounds on variables
        should be Sequence of ``(min, max)`` pairs for each element in `x`. None is used to specify no bound.

kwArgs
---------
method : string
    optimization algorithm to use 

extra_dict : dict
    used to transfer specific arguments for optimization algorithm
    
opt_inherit : class 
    inherit ``optimization results``, ``parameters`` and ``logs``
    defeault is None (not use inherit) 

delay : float 
    delay of each iteration, default is 0.1s

max_run : int 
    maxmun times of running optimization, default = 10 

msg : Bool
    whether to output massages in every iterarion, default is True
    
log : Bool
    whether to generate a log file in labopt_logs
    
logfile : str
    log file name , defeault is "optimization__ + <timestamp>__ + <method>__.txt"

"""

def multi_optimize(func,paras_init,args:tuple,optimizer_list:list,extra_dict_list:list,
                   method_list:list,max_run_list:list,bounds_list:list,**kwargs):
    """combine multi optimization algorithms
        Args
        --------
        fun : callable
            The objective function to be minimized.

                ``fun(x, *args) -> dict : {'cost':float, 'uncer':float, 'bad':bool}``
                
            where ``cost`` is the value to minimize, ``uncer`` is uncertainty,
            ``bad`` is the judge whether this value is bad (bad = True) for this cost

            ``x`` is a 1-D array with shape (n,) and ``args``
            is a tuple of the fixed parameters needed to completely
            specify the function.

        paras_init : ndarray, shape (n,)
            Initial guess. Array of real elements of size (n,),
            where ``n`` is the number of independent variables.

        args : tuple, optional
            Extra arguments passed to the objective function which will not
            change during optimization
            
        optimizer_list : list
            a ordered lists, in which are optimizers to be used 

        method_list : list
            a list, whose elements are ordered 
            optimization algorithm to use 

        extra_dict_list : list
            a list whose elements are ordered extra_dicts for optimizers,
            extra_dicts are used to transfer specific arguments for optimization algorithm
            
        bounds_list : list
            a list, whose elements are tuples,
            should be Sequence of ``(min, max)`` pairs for each element in `x`. None is used to specify no bound.
            
            >>> [((1,2),(1,2)),((1,2),(1,2)),((1,2),(1,2))]
            
            if len(bounds_list) != len(optimizers)
            
            will always use bounds_list[0]

        max_run_list : list
            a list, whose elements are ordered 
            maxmun times of running optimization, default = 10 

        kwArgs
        ---------
        delay : float 
            delay of each iteration, default is 0.1s
        
        msg : Bool
            whether to output massages in every iterarion, default is True
            
        log : Bool
            whether to generate a log file in labopt_logs
            
        logfile : str
            log file name , defeault is "optimization__ + <timestamp>__ + <method>__.txt"
            level lower than inherited logfile
    """
    import time
    num_opt = len(optimizer_list)
    num_extra_dict = len(extra_dict_list)
    num_method = len(method_list)
    num_run = len(max_run_list)
    
    ## log name
    special_str = "["
    for opt_cls, str_method in zip(optimizer_list,method_list):
        special_str = special_str + opt_cls._doc() + "-" + str(str_method) + ";"
    special_str = special_str + "]"
    
    log = kwargs.get("log",None)
    kwargs["log"] = "alkaid"
    log_name = "cascated_opt__" + time.strftime("%Y-%m-%d-%H-%M",time.gmtime(local_time())) + "__" + special_str + "__" + ".txt"
    
    ## first run
    if num_opt != num_extra_dict or num_opt != num_method or num_opt != num_run:
        OptimizateException("all lists except bounds_list should have equal lens")
    
    optimizer = optimizer_list[0]
    try:
        opt_operator = optimizer(func,paras_init,args = args,bounds = bounds_list[0],**(extra_dict_list[0]),max_run = max_run_list[0],method = method_list[0],**kwargs,logfile = log_name)
    except:
        opt_operator = optimizer(func,paras_init,args = args,bounds = bounds_list[0],**(extra_dict_list[0]),max_run = max_run_list[0],method = method_list[0],**kwargs,logfile = log_name)
    
    paras_init = opt_operator.optimization()
    
    ## then
    for i in range(1,num_opt):
        ## add log in the last time
        if i == num_opt - 1:
            kwargs["log"] = log
        ## define opt class
        optimizer = optimizer_list[i]
        try:
            opt_operator = optimizer(func,paras_init,args = args,bounds = bounds_list[i],**(extra_dict_list[i]),
                                     method = method_list[i],max_run = max_run_list[i],
                                     **kwargs,opt_inherit = opt_operator)
        except:
            opt_operator = optimizer(func,paras_init,args = args,bounds = bounds_list[0],**(extra_dict_list[i]),
                                     method = method_list[i],max_run = max_run_list[i],
                                     **kwargs,opt_inherit = opt_operator)
        
        paras_init = opt_operator.optimization()

    ## visualization
    opt_plot(opt_operator._flist,opt_operator._x_vec,method_list)
    
def _main():
    import numpy as np
    def func(x,a,b,c,d):
        vec = np.array([a,b,c,d])
        f = np.sum((x - vec)**2,axis = None) + 5*np.sum(np.cos(x-a) + np.cos(x-b) + np.sin(x-c) + np.sin(x-d)) + a*b*c*d
        uncer = 0.1
        bad = None
        return_dict = {'cost':f,'uncer':uncer,'bad':bad}
        return return_dict
    
    init = np.array([3,0,4,2])
    a = 6
    b = 8
    c = 1
    d = 2
    bounds = ((-10,10),(-10,10),(-10,10),(-10,10))
    method_list =  ["dual","simplex"]
    optimizer_list = [global_optimize,local_optimize]
    multi_optimize(func,init,args = (a,b,c,d,),optimizer_list=optimizer_list,bounds_list = [bounds],
                   max_run_list = [1,20],delay = 0.03,method_list = method_list,extra_dict_list=[{},{}],val_only = True,msg = False,log = True)
     
if __name__ == "__main__":
    _main()
