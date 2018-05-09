import pandas as pd
import os,sys,re,random,logging,argparse
"""
BeginHeader													
   UnknownEvent/Classic	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	                              EventGuid	 Type	 Level	 Version	 MofLength				
   InvalidEvent/Classic	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	                              EventGuid	 Type	 Level	 Version	 MofLength				
   UnknownEvent/Crimson	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	                             ProviderId	     Id	   Task	 Opcode	 Version	 Channel	 Level	            Keyword	 UserDataLength
   InvalidEvent/Crimson	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	                             ProviderId	     Id	   Task	 Opcode	 Version	 Channel	 Level	            Keyword	 UserDataLength
FirstReliableEventTimeStamp	 TimeStamp												
                P-Start	  TimeStamp	     Process Name ( PID)	  ParentPID	  SessionID	  UniqueKey	 UserSid	 Command Line						
                  P-End	  TimeStamp	     Process Name ( PID)	  ParentPID	  SessionID	  UniqueKey	     Status	 UserSid	 Command Line					
              P-DCStart	  TimeStamp	     Process Name ( PID)	  ParentPID	  SessionID	  UniqueKey	 UserSid	 Command Line						
                P-DCEnd	  TimeStamp	     Process Name ( PID)	  ParentPID	  SessionID	  UniqueKey	 UserSid	 Command Line						
               P-Zombie	  TimeStamp	     Process Name ( PID)	  ParentPID	  SessionID	  UniqueKey	 UserSid	 Command Line						
                T-Start	  TimeStamp	     Process Name ( PID)	   ThreadID	  StackBase	 StackLimit	 UsrStkBase	  UsrStkLmt	    TebBase	 SubProcessTag	            Image!Function			
                  T-End	  TimeStamp	     Process Name ( PID)	   ThreadID	  StackBase	 StackLimit	 UsrStkBase	  UsrStkLmt	    TebBase	 SubProcessTag	            Image!Function			
              T-DCStart	  TimeStamp	     Process Name ( PID)	   ThreadID	  StackBase	 StackLimit	 UsrStkBase	  UsrStkLmt	    TebBase	 SubProcessTag	            Image!Function			
                T-DCEnd	  TimeStamp	     Process Name ( PID)	   ThreadID	  StackBase	 StackLimit	 UsrStkBase	  UsrStkLmt	    TebBase	 SubProcessTag	            Image!Function			
                I-Start	  TimeStamp	     Process Name ( PID)	   BaseAddr	    EndAddr	   Checksum	 TimeDateStamp	DefaultBase	 FileName					
                  I-End	  TimeStamp	     Process Name ( PID)	   BaseAddr	    EndAddr	   Checksum	 TimeDateStamp	DefaultBase	 FileName					
              I-DCStart	  TimeStamp	     Process Name ( PID)	   BaseAddr	    EndAddr	   Checksum	 TimeDateStamp	DefaultBase	 FileName					
                I-DCEnd	  TimeStamp	     Process Name ( PID)	   BaseAddr	    EndAddr	   Checksum	 TimeDateStamp	DefaultBase	 FileName					
           VirtualAlloc	  TimeStamp	     Process Name ( PID)	   BaseAddr	    EndAddr	 Flags								
            VirtualFree	  TimeStamp	     Process Name ( PID)	   BaseAddr	    EndAddr	 Flags								
          SessionCreate	  TimeStamp	  SessionID	  UniqueKey										
        GrowKernelStack	  TimeStamp	     Process Name ( PID)	   ThreadID	  StackBase	 StackLimit								
                  T-GUI	  TimeStamp	     Process Name ( PID)	   ThreadID	  StackBase	 StackLimit								
       HeapRangeRundown	  TimeStamp	     Process Name ( PID)	 HeapHandle	      Flags									
        HeapCreateRange	  TimeStamp	     Process Name ( PID)	   ThreadID	 HeapHandle	       Size	      Flags							
       HeapRangeReserve	  TimeStamp	     Process Name ( PID)	   ThreadID	 HeapHandle	VirtualAddr	       Size							
       HeapRangeRelease	  TimeStamp	     Process Name ( PID)	   ThreadID	 HeapHandle	VirtualAddr	       Size							
       HeapRangeDestroy	  TimeStamp	     Process Name ( PID)	   ThreadID	 HeapHandle									
      HeapCreateRundown	  TimeStamp	     Process Name ( PID)	 HeapHandle	   BaseAddr	       Size								
         ProcessPerfCtr	  TimeStamp	     Process Name ( PID)	    Peak WS	    Peak VM	    Peak PF	    Peak PP	   Peak NPP						
  ProcessPerfCtrRundown	  TimeStamp	     Process Name ( PID)	    Peak WS	    Peak VM	    Peak PF	    Peak PP	   Peak NPP	     End WS	     End VM	     End PF	     End PP	    End NPP	  # Handles
     PageRemovedByColor	  TimeStamp	        Pfn	 Pri	          List	 UseDescription	        Detailed Usage	  VA/Offset	 Process/File Name					
            PageRemoved	  TimeStamp	        Pfn	 Pri	          List	 UseDescription	        Detailed Usage	  VA/Offset	 Process/File Name					
               InMemory	  TimeStamp	        Pfn	 Pri	          List	 UseDescription	        Detailed Usage	  VA/Offset	 Process/File Name					
           InsertInFree	  TimeStamp	        Pfn	 Pri	          List	 UseDescription	        Detailed Usage	  VA/Offset	 Process/File Name					
       InsertInModified	  TimeStamp	        Pfn	 Pri	          List	 UseDescription	        Detailed Usage	  VA/Offset	 Process/File Name					
           ZeroShareCnt	  TimeStamp	        Pfn											
            MemSnapLite	  TimeStamp	        Pfn											
  PageFileMappedSection	  TimeStamp	     Process Name ( PID)	 Range Base	  Range End	 Rundown								
                MemInfo	  TimeStamp	 FreePages	 Standby7	 Standby6	 Standby5	 Standby4	 Standby3	 Standby2	 Standby1	 Standby0	 TotalStandby	 ModifiedPages	 InUsePages
         PagefileBacked	  TimeStamp	 DeviceChars	 FileChars	  Flags	 ActiveDataRef	 DeviceEjectable	 FileObject	 FileName					
              PageFault	  TimeStamp	     Process Name ( PID)	   ThreadID	VirtualAddr	   PrgrmCtr	        Type	            Image!Function						
              HardFault	  TimeStamp	     Process Name ( PID)	   ThreadID	VirtualAddr	   ByteOffset	     IOSize	 ElapsedTime	 FileObject	 FileName	 Hardfaulted Address Information			
             DriverCall	  TimeStamp	     IrpPtr	   UniqueId	            MajorFunction	  MinorFunc	 FileObject	 FileName	            Image!Function					
           DriverReturn	  TimeStamp	     IrpPtr	   UniqueId										
         DriverComplete	  TimeStamp	     IrpPtr	   UniqueId	            Image!Function									
   DriverCompleteReturn	  TimeStamp	     IrpPtr	   UniqueId										
DriverCompletionRoutine	  TimeStamp	     IrpPtr	   UniqueId	            Image!Function									
               DiskRead	  TimeStamp	     Process Name ( PID)	   ThreadID	     IrpPtr	   ByteOffset	     IOSize	 ElapsedTime	  DiskNum	 IrpFlags	 DiskSvcTime	 I/O Pri	  VolSnap	 FileObject
              DiskWrite	  TimeStamp	     Process Name ( PID)	   ThreadID	     IrpPtr	   ByteOffset	     IOSize	 ElapsedTime	  DiskNum	 IrpFlags	 DiskSvcTime	 I/O Pri	  VolSnap	 FileObject
           DiskReadInit	  TimeStamp	     Process Name ( PID)	   ThreadID	     IrpPtr									
          DiskWriteInit	  TimeStamp	     Process Name ( PID)	   ThreadID	     IrpPtr									
              DiskFlush	  TimeStamp	     Process Name ( PID)	   ThreadID	     IrpPtr	                           ElapsedTime	  DiskNum	 IrpFlags	 DiskSvcTime	 I/O Pri				
          DiskFlushInit	  TimeStamp	     Process Name ( PID)	   ThreadID	     IrpPtr									
           FileIoCreate	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	    Options	 Attributes	ShareAccess	 FileName	 ParsedOptions	 ParsedAttributes	 ParsedShareAccess
          FileIoCleanup	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	 FileName						
            FileIoClose	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	 FileName						
            FileIoFlush	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	 FileName						
             FileIoRead	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	   ByteOffset	       Size	      Flags	 Priority	 FileName	 ParsedFlags	
            FileIoWrite	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	   ByteOffset	       Size	      Flags	 Priority	 FileName	 ParsedFlags	
          FileIoSetInfo	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	  ExtraInfo	  InfoClass	 FileName				
        FileIoQueryInfo	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	  ExtraInfo	  InfoClass	 FileName				
            FileIoFSCTL	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	  ExtraInfo	  InfoClass	 FileName				
           FileIoDelete	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	  ExtraInfo	  InfoClass	 FileName				
           FileIoRename	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	  ExtraInfo	  InfoClass	 FileName				
          FileIoDirEnum	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	  FileIndex	       Size	  InfoClass	 FileName	 FileName		
        FileIoDirNotify	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	  FileIndex	       Size	  InfoClass	 FileName	 FileName		
            FileIoOpEnd	  TimeStamp	     Process Name ( PID)	   ThreadID	 CPU	     IrpPtr	 FileObject	 ElapsedTime	     Status	  ExtraInfo	 Type	 FileName		
         FileNameCreate	  TimeStamp	 FileObject	 FileName										
         FileNameDelete	  TimeStamp	 FileObject	 FileName										
        FileNameRundown	  TimeStamp	 FileObject	 FileName										
EndHeader													

# first we can create new files with only DiskRead and DiskWrite

               DiskRead	  TimeStamp	     Process Name ( PID)	   ThreadID	     IrpPtr	   ByteOffset	     IOSize	 ElapsedTime	  DiskNum	 IrpFlags	 DiskSvcTime	 I/O Pri	  VolSnap	 FileObject
              DiskWrite	  TimeStamp	     Process Name ( PID)	   ThreadID	     IrpPtr	   ByteOffset	     IOSize	 ElapsedTime	  DiskNum	 IrpFlags	 DiskSvcTime	 I/O Pri	  VolSnap	 FileObject
"""
class Reader(object):
	def __init__(self,folder = 'MSNStorageCFS',chunksize = 1000,rows = -1,fname = None,mode = None):
		self._folder = folder
		self._fileList = os.listdir(str(self._folder)+os.sep+'Traces')
		self.chunksize = chunksize
		self._fname = fname
		self.mode = mode
		if not fname:
			# if both filename and mode not specified, parse random csv
			self._fname = self._fileList[random.randint(0,len(self._fileList)-1)]
			
			if self.mode:
				# parse all files
				print("Mode specified, parsing all files")
			else:
				print("Mode not specified and filename not mentioned, parsing random file")
		elif self.mode and self.fname:
			print("Mode specified and file name given, parsing all files")
		elif not self.mode and self.fname:
			print("Parsing {}".format(self.fname))
		if rows != -1 and rows < chunksize:
			raise ValueError('rows: {} < chunksize {}'.format(rows,chunksize))
		self._rows = rows if rows != -1 else None

	def drawProgressBar(self,percent, barLen = 50):
		sys.stdout.write("\r")
		progress = ""
		for i in range(barLen):
			if i<int(barLen * percent):
				progress += "="
			else:
				progress += " "
		sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
		sys.stdout.flush()

	def load_chunks(self,mode = None):
		# DiskRead,TimeStamp,Process Name ( PID),ThreadID,IrpPtr,ByteOffset,IOSize,ElapsedTime,DiskNum,IrpFlags,DiskSvcTime,I/O Pri,VolSnap,FileObject
		mode = self.mode
		chunks = []
		fname = str(self._fname)
		print('Working on {}\n'.format(fname))
		def write_csv(fname):
			temp = fname.split(os.sep)[-1].split('.')[:-2]
			temp.insert(0,'parsed')
			save_name = '.'.join([i for i in temp])
			save_name = ('.'+os.sep+str(self._folder)+os.sep+'Parsed Traces'+os.sep+save_name+'.csv')
			df = pd.read_csv(fname,error_bad_lines = False, low_memory = False,skiprows = 73, sep = ',')
			df.columns = ['Disk Operation','TimeStamp','Process Name ( PID)','ThreadID','IrpPtr','ByteOffset','IOSize',\
				'ElapsedTime','DiskNum','IrpFlags','DiskSvcTime','I/O Pri','VolSnap','FileObject','FileName']
			df = df.drop(['VolSnap'],axis = 1)
			df = df.loc[df['Disk Operation'].isin(['              DiskWrite','               DiskRead'])]					
			#print('Writing with name: {}'.format(save_name))
			df.to_csv(path_or_buf = save_name ,index_label = False,chunksize = 100,index = False)
		def without_rows():
			if not self.mode:
				iterator = None
				print("parsing {}".format(fname))
				write_csv(fname)
				#df = pd.read_csv(fname,error_bad_lines = False, low_memory = False,skiprows = 73, sep = ',')
			elif self.mode:
				iterator = None
				# parse all csvs in current folder
				print("parsing all files:\n")
				total_files = len(fname)
				for f in range(len(fname)):
					write_csv(fname[f])
					self.drawProgressBar((f+1)/total_files)
		def with_rows():
			# creating an iterator to read in chunks, not functional atm
			iterator = pd.read_csv(fname,error_bad_lines = False, chunksize = self.chunksize, low_memory = False,skiprows = 73, sep = ',')			
			iterator.columns = ['Disk Operation','TimeStamp','Process Name ( PID)','ThreadID','IrpPtr','ByteOffset','IOSize',\
				'ElapsedTime','DiskNum','IrpFlags','DiskSvcTime','I/O Pri','VolSnap','FileObject','FileName']

		if fname not in self._fileList:
			raise ValueError('{} not found'.format(fname))

		else:
				
			if not self.mode:
				fname = ('.'+os.sep+str(self._folder)+os.sep+'Traces'+os.sep+str(self._fname))
				temp = fname.split(os.sep)[-1].split('.')[:-2]

			elif self.mode:
				# mode specified, parse all files
				# regardless of filename given
				fname = []
				for file in self._fileList:
					fname.append(('.'+os.sep+str(self._folder)+os.sep+'Traces'+os.sep+str(file)))
			if not self._rows:
				without_rows()
			if self._rows:
				with_rows()
		return None
	

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--folder', type=str, default= 'MSNStorageCFS',
					   help='Folder where subfolder Traces is found')
	parser.add_argument('--mode', type=str, default= None,
					   help='mode = all for recursive parsing of all csvs')	
	parser.add_argument('--chunksize', type=int, default=1000,
					   help='specifies iterator size for reading csvs')
	parser.add_argument('--rows',type=int, default = -1,
						help = '-1 for all rows or specify how many. Must be >= chunksize'	)
	parser.add_argument('--file', type = str, default = None,
						help = 'specify filname to work on, defaults to parsing all')
	args = parser.parse_args()	
	#data_object = Reader(args.folder,args.chunksize//5,args.rows,args.file)
	data_object = Reader(args.folder,args.chunksize,args.rows,args.file,args.mode)
	data_object.load_chunks(args.mode)
if __name__ == '__main__':
	main()