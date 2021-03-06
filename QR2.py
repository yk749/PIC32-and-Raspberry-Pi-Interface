from pyzbar import pyzbar
import cv2
from datetime import datetime
import time

def qr2( run_flag, qr2_receive_queue, p_start_turn, p_end_turn, frame_queue ):
	while ( run_flag.value ):
		start = time.time()
		if ( p_start_turn.value == 2 and ( not frame_queue.empty() ) ) :
			#print ( 'this is qr2' )
			frame = frame_queue.get(True)
			p_start_turn.value = 3
			barcodes = pyzbar.decode( frame )
			if len(barcodes) > 0:
				barcode = barcodes[0]
				(x,y,w,h) = barcode.rect
				center = ( x+ w/2, y + h/2 )
				cv2.rectangle( frame, (x,y),(x+w,y+h),(0,0,255),2 )
				text = ' center:' + str(center[0]) + ',' + str(center[1])
				cv2.putText( frame, text, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
				cv2.imshow( "qr2",frame )
				cv2.waitKey(2)
				if x+ w/2 < 270:
					qr2_receive_queue.put( ["right",x+ w/2] ) 
				elif x+ w/2 > 370:
					qr2_receive_queue.put( ["left",x+ w/2] )
				else:
					qr2_receive_queue.put( ["center",x+ w/2] )
			else:
				qr2_receive_queue.put( ["miss",-1] )
			end = time.time()
			print ( "processor 2 processing time" + str( end - start ) )




