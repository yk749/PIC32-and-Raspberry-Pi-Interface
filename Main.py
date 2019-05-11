from multiprocessing import Process, Queue, Value, Lock, Array
from QR1 import qr1
from QR2 import qr2
from QR3 import qr3
from Master import master

if __name__ == '__main__':
	
	# run_flag indicates if processes are running or not
	# p_start_turn is the order of running processes, 1 is RedCircleDetection
	# 2 is GreenCircleDetection and 3 is BlueCircleDetection, 4 indicates a state
	# wating for all 3 processes to finish their current job
	# p_end_turn is the order of terminating processes, not used for now
	# Red_receive_queue is the queue for process 1 to tranmit its result to master process
	# Green_receive_queue and Blue_receive_queue are the same with Red_receive_queue
	
	run_flag = Value( 'i', 1 )
	p_start_turn = Value( 'i', 1 )
	p_end_turn = Value( 'i', 1 )
	qr1_receive_queue = Queue()
	qr2_receive_queue = Queue()
	qr3_receive_queue = Queue()
	frame_queue = Queue()
	
	# define one master processor and three worker processors, each worker processor 
	# process one color ball, and master processor collect all results and do all control
	
	p0 = Process( target = master, args= (run_flag,qr1_receive_queue,qr2_receive_queue,qr3_receive_queue,p_start_turn ,p_end_turn ,frame_queue,) )  
	p1 = Process( target = qr1, args = ( run_flag,qr1_receive_queue, p_start_turn, p_end_turn,frame_queue,) )
	p2 = Process( target = qr2, args = ( run_flag,qr2_receive_queue, p_start_turn, p_end_turn,frame_queue,) )
	p3 = Process( target = qr3, args = ( run_flag,qr3_receive_queue, p_start_turn, p_end_turn,frame_queue,) )
	
	# start all processes
	
	p0.start()
	p1.start()
	p2.start()
	p3.start()
	
	# merge all processes
	
	p0.join()
	p1.join()
	p2.join()
	p3.join()
