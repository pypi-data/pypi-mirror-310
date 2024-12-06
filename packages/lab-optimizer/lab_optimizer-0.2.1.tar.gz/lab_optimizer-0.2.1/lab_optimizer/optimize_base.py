import numpy as np
import torch as th
import time 
import os
import matplotlib.pyplot as plt

"""
optimization base class

1.tool functions: including plot, timing and log processing

2.optimize base: including parameters set, function decorating, optimization progress visualizing 

"""

def local_time(time_zone:int = 8) -> float:
    """get local time
    
        Args
        ---------
        time_zone : int
            local UTC time zone, defeault is 8

    """
    t = time.time() + time_zone*3600.
    return t

def opt_plot(flist,x_vec,method):
    N,M = x_vec.shape
    ## cost vs rounds
    plt.figure(1)
    timelist = np.arange(N)
    plt.plot(timelist,flist,label = "f value")
    plt.xlabel("rounds")
    plt.title("cost vs optimization rounds @ " + str(method))
    plt.legend()
    
    ## cost vs 
    plt.figure(2)
    for i in range(M):
        plot_vec = x_vec[:,i]
        normal = np.max(np.abs(plot_vec),axis = None)
        plot_vec = plot_vec/normal
        plt.scatter(timelist,plot_vec,label = f"times vs paras-{i} with amp = {normal:.4f}")
    plt.legend()
    plt.xlabel("rounds")
    plt.title("normalized parameters  @ " + str(method))
    
    plt.figure(3)
    for i in range(M):
        plot_vec = x_vec[:,i]
        plt.scatter(timelist,x_vec[:,i],label = f"times vs paras-{i}")
    plt.legend()
    plt.xlabel("rounds")
    plt.title("raw parameters @ " + str(method))
    
    plt.show()
    
def log_visiual(path:str):
    """view optimization results from log  

        Args
        ---------
        path : string
            log path of optimization log 
        
    """
    def converter(s):
        s = s[1:-2].decode('utf-8')
        # Split the string into individual numbers and convert them to floats
        return np.array([float(x) for x in s.split(',')])

    msgs = ["logs : \n"]
    head_numbers = 1
    #%%
    with open(path, 'r', encoding='utf-8') as file:
        for current_line, line in enumerate(file, start=1):  # count from line 1
            f_msgs = line.strip()
            msgs.append(f_msgs)
            if f_msgs == "##":
                break
            head_numbers += 1
    for i in msgs:
        print(i)
    
    data_list = np.loadtxt(path,skiprows = head_numbers,usecols=(2),converters = {2: converter},dtype = object)
    value_list = np.loadtxt(path,skiprows = head_numbers,usecols=(3))
    
    x_list = np.array([data_list[0]])
    for i in range(1,len(data_list)):
        x_list = np.vstack((x_list,data_list[i]))
    
    opt_plot(value_list,x_list,"from log")

class OptimizateException(Exception):
    def __init__(self,err):
        Exception.__init__(self,"optimize error : " + err)
    
    ## user define
    @staticmethod    
    def user_define(func):
        def wrapper(self,*args,**kwargs):
            func(self,*args,**kwargs)
            raise OptimizateException(func.__name__ + " not defined!")
        return wrapper

class optimize_base(OptimizateException):
    def __init__(self,func,paras_init:np.ndarray,args:tuple = (),bounds:tuple = None,**kwargs):
        print("optimization start")
        self._time_start = local_time()
        self._max_run = kwargs.get("max_run",100)
        self._val_only = kwargs.get('val_only',True)
        self._torch = kwargs.get("torch",False)
        
        self._target = kwargs.get("target",-np.infty)
        self._args = args
        self._bounds = bounds
        self._log = kwargs.get("log", True)

        self._func = self._decorate(func,delay = kwargs.get("delay",0.1),msg = kwargs.get("msg",True))
        opt_inherit = kwargs.get("opt_inherit",None)
        
        ## inherit
        if opt_inherit != None: # if we have inherit
            self._flist = opt_inherit._flist
            self._x_vec = opt_inherit._x_vec
            self._time_stamp = opt_inherit._time_stamp
            log_head_inhert = opt_inherit._log_head
            self._filename = opt_inherit._filename
            self._paras_init = opt_inherit.x_optimize
            self._run_count = opt_inherit._run_count
        else: # if no inherit
            self._paras_init = paras_init
            if self._torch == True:
                self._flist = th.tensor([(func(self._paras_init,*args).get("cost",0))])
                self._x_vec = self._paras_init.clone()
            else:   
                self._flist = np.array([(func(self._paras_init,*args).get("cost",0))])
                self._x_vec = np.array([self._paras_init])
            self._time_stamp = [time.strftime("%d:%H:%M:%S",time.gmtime(self._time_start))]
            log_head_inhert = ""
            self._filename = kwargs.get("logfile","optimization__" + time.strftime("%Y-%m-%d-%H-%M",time.gmtime(self._time_start)) + "__" + kwargs.get("method","None") + "__" + ".txt")
            self._run_count = 0
            
        ## create log head
        if self._log == True or self._log == "inherit":
            self._log_head = log_head_inhert + (
                "name : " + self._filename + "\n" + 
                "start_time : " + time.strftime("%Y_%m_%d_%H:%M:%S",time.gmtime(local_time())) + "\n" +
                "func : " + func.__repr__() + "\n" + 
                "method : " + kwargs.get("method","None") + "\n" +
                "args : " + self._args.__repr__() + "\n" +
                "paras_init : " + self._paras_init.__repr__() + "\n" +
                "bounds : " + self._bounds.__repr__() + "\n" + 
                "max_run : "  f"{self._max_run:.0f}" + "\n"
                "form : " + "rounds, time, parameters, cost " + "\n\n" 
            )
        
    def _logging(self):
        if self._log == True:
            ## folder
            os.makedirs("labopt_logs", exist_ok=True)
            sub_folder = os.path.join("labopt_logs","lab_opt_" + time.strftime("%Y_%m_%d",time.gmtime(self._time_start)) )
            os.makedirs(sub_folder, exist_ok=True)
            self._filename = os.path.join(sub_folder, self._filename)  # Store in a 'logs' directory

            ## head
            with open(self._filename, "w") as file:
                file.write(self._log_head)
                file.write("##\n")
            ## data
            if self._torch == True:
                _x_vec = self._x_vec.detach().numpy()
                _flist = self._flist.numpy()
            with open(self._filename, "a") as file:
                for i in range(np.size(_flist)):
                    file.write(f"{i}" + ", " +
                                self._time_stamp[i] 
                                + ", ")
                    file.write("[" + ",".join(map(str,_x_vec[i])) + "]")
                    file.write(", " + f"{_flist[i,0]}" + "\n")

    def _decorate(self,func,delay = 0.1,msg = True): # delay in s
        if self._torch == True:
            def func_decorate(x,*args,**kwargs):
                time.sleep(delay)
                f = func(x,*args,**kwargs)
                f_val = f.get("cost",0)
                if msg == True:
                    print(f"INFO RUN: {self._run_count}")
                    print(f"INFO cost {f_val:.6f}")
                    print(f"INFO parameters {x}" + "\n")
                self._run_count += 1
                ## build flist including f values
                ## and x_vec in which x_vec[:,i] include the 
                ## changing traj of a parameter
                self._flist = th.vstack((self._flist,th.tensor([f_val])))
                self._x_vec = th.vstack((self._x_vec,x))
                self._time_stamp = self._time_stamp + [ time.strftime("%d:%H:%M:%S",time.gmtime(local_time())) ]
                if self._val_only == True:
                    return f_val
                else:
                    return f
        else:
            def func_decorate(x,*args,**kwargs):
                time.sleep(delay)
                f = func(x,*args,**kwargs)
                f_val = f.get("cost",0)
                if msg == True:
                    print(f"INFO RUN: {self._run_count}")
                    print(f"INFO cost {f_val:.6f}")
                    print(f"INFO parameters {x}" + "\n")
                self._run_count += 1
                ## build flist including f values
                ## and x_vec in which x_vec[:,i] include the 
                ## changing traj of a parameter
                self._flist = np.vstack((self._flist,f_val))
                self._x_vec = np.vstack((self._x_vec,x))
                self._time_stamp = self._time_stamp + [ time.strftime("%d:%H:%M:%S",time.gmtime(local_time())) ]
                if self._val_only == True:
                    return f_val
                else:
                    return f
        return func_decorate

    @OptimizateException.user_define
    def optimization(self):
        """ you must define this method in XXX_optimize class
        """   
    
    def _visualization(self,flist,x_vec,method = "None"):
        self._time_end = local_time()
        delta_t = self._time_end - self._time_start
        f_delta_t = time.strftime("%H:%M:%S",time.gmtime(delta_t))
        print("\nthe optimization progress costs:")
        print(f"hh:mm:ss = {f_delta_t}\n")
        
        if self._torch == True:
            flist = flist.detach().numpy()
            x_vec = x_vec.detach().numpy()
        
        opt_plot(flist,x_vec,method)
        
if __name__ == "__main__":
    
    # visual logs
    path = "labopt_logs/lab_opt_2024_11_22/optimization__2024-11-22-15-11__simplex__.txt"
    log_visiual(path)
        
    # """