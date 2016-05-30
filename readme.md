# PythonGO

PythonGo is a parallize framework to python, co-opting the spirit of goroutine in Golang.

## Note

I am fresh in Python, with wish of you helping me.

## Q & A

Q: Why not use multi-thread?
A: Because most Python use GIL, its thread cannot run in different cores of CPU.

Q: Why not use multiprocessing.Process directly?
A: 1.If you start a process whenever you have a job to do and stop it when it finish, there will be many times that
 process switches, burning many CPU times because of the large context of a process. 2.If you use the process pool 
to optimize the problem before, when a process finished its all jobs, it dosn't know if there will be a job to do soon,
 so it will spinning in vain.
 
Q: What can I do using this framework?
A: The scene designed is below: First, you should initialize the runtime, delicating a main function to it to descripe 
the entrance of this program; Then, you can use runtime.go(func, args) in your functions/goroutines to start a new gor
outine; End, you can report your experience and commit bugs to me, thanks!